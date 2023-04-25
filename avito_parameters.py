import proxy_connection as pc
import hashlib
from pymongo import MongoClient
import __set_datetime as sd
import aux_functions as af


class AvitoObject:

    name_data_base = 'data_base_avito_new'
    data_base = None
    check_id = None
    dom_ad = None
    title_text = None
    reference_ad = None
    unique_id = None
    offer_date_time = None
    address = None
    price = None
    type_technic = None
    model_exact = None
    year = None
    condition = None
    maker = None
    moto_hours = None
    documentation = None

    model_aux = None

    XPATH_PRICE = ".//div[@class='iva-item-priceStep-uq2CQ']//span[@class='price-text-_YGDY text-text-LurtD text-size-s-BxGpL']/text()"
    XPATH_HEADER = ".//div[@class='iva-item-titleStep-pdebR']//h3/text()"
    XPATH_REFERENCE = ".//div[@class='iva-item-titleStep-pdebR'']/a/@href"
    XPATH_ADDRESS = ".//span[@class='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL']/span/text()"
    XPATH_TITLE = "//span[@class='title-info-title-text']/text()"
    XPATH_OFFER_DATE = "//div[@class='title-info-metadata-item-redesign']/text()"
    XPATH_PARAMETERS = "//ul[@class='item-params-list']/li"


    def __init__(self, reference_ad, price, model_text_request, address):

        #
        self.price = price

        #
        self.address = address

        #
        self.reference_ad = reference_ad

        # Создание параметра, содержащего название модели в запросе
        self.model_text_request = model_text_request

        # Создание подключения с Mongod
        self.set_data_base()

        # Создание соединения
        self.set_dom_ad()

        # Получение параметров со страницы объявления
        self.get_parameters()

    def return_data(self):

        return self.check_id, self.title_text, self.unique_id, self.offer_date_time, self.model_exact, \
                    self.type_technic, self.year, self.condition, self.maker, self.moto_hours, self.documentation

    def set_dom_ad(self):

        """ Метод учитывает способ соединения и выдает DOM страницы с ответом """

        # self.research_dom = pc.connection_own_ip(self.reference_research)

        # через прокси
        mobile_proxy = pc.MobileProxy(self.reference_ad)
        self.dom_ad = mobile_proxy.get_dom()

    def set_data_base(self):

        """ Создание подключения к MongoDB """

        client = MongoClient('localhost', 27017)
        db = client[self.name_data_base]
        self.data_base = db.data_base

    def research_ad(self):

        """ Получение сведений об объекте """

        # Получение текст заголовка
        self.title_text = self.dom_ad.xpath(self.XPATH_TITLE)[0]

        # Получение дату объявления
        self.offer_date_time = sd.set_time_ad(self.dom_ad.xpath(self.XPATH_OFFER_DATE)[0])

        for page_ad in self.dom_ad.xpath(self.XPATH_PARAMETERS):

            if page_ad.xpath(".//span/text()")[0] == 'Тип техники: ':
                self.type_technic = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Год выпуска: ':
                self.year = int(page_ad.xpath("./text()")[1].lower())

            elif page_ad.xpath(".//span/text()")[0] == 'Состояние: ':
                self.condition = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Марка: ':
                self.maker = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Модель: ':
                self.model_exact = page_ad.xpath("./text()")[1].lower()

            elif page_ad.xpath(".//span/text()")[0] == 'Моточасы: ':
                self.moto_hours = int(self.del_letters_moto_hours(af.processing_text(page_ad.xpath("./text()")[1].split(' ')[0])))

            elif page_ad.xpath(".//span/text()")[0] == 'ПТС или ПСМ: ':
                self.documentation = page_ad.xpath("./text()")[1].lower()

        # make self.unique_id
        self.get_cript_id()

    def get_parameters(self):

        self.research_ad()

        # Проверка на наличие объекта в БД
        if self.model_exact is not None and self.model_text_request is not None:
            self.check_mongodb()

    def get_cript_id(self):

        """ Создание уникального специально хеш кода для проверки на наличие данного объекта в БД """

        if self.year is not None and self.model_exact is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.year}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.year is None and self.model_exact is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.model_exact is None and self.year is not None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.model_exact}{self.address}'
                                          .encode('utf-8')).hexdigest()

        elif self.model_exact is None and self.year is None:
            self.unique_id = hashlib.sha1(f'{self.price}{self.title_text}{self.address}'.encode('utf-8')).hexdigest()

    def check_mongodb(self):

        """ Проверка на наличие аналогичного объявления в БД """

        for n in self.data_base.find({'hex_id': self.unique_id}):
            self.check_id = 'stop'

    @staticmethod
    def del_letters_moto_hours(word):

        """ Method delete letters in word of attribute moto_hours """
        temp_word = ''
        for el in word:

            if el.isdigit():
                temp_word = temp_word + el

        return temp_word



# if __name__ == '__main__':
#
#     processing_page_technic('трактор')

