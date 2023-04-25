from proxy_connection import Proxy
from research_header import ResearchHeader
import aux_functions as af
import hashlib
from pymongo import MongoClient
from db_use import SqlAddDromTechnic, SqlDataBaseQuery
import time
import random
from research_header import ResearchHeader
import time
import datetime


class DromResearch():

    """ Парсинг предложений на сайте agroserver.ru """

    #
    last_id = None

    # Название бызы MongoDB
    name_data_base = 'data_base_drom'

    # Переменная содержит объект базы данных MongoDB
    data_base = None

    #
    check_id = None

    # Начальная страница с результатами поиска
    init_research_reference = 'https://www.drom.ru/spec/farm/tractor/?s=all&order=year'

    # Страница с результатами поиска
    research_reference = None

    # DOM поисковой страницы
    dom_research = None

    unique_id = None
    reference_ad = None
    type_technic = None
    technic_base = None
    maker_technic = None
    model_technic = None
    year_make = None
    power_engine = None
    condition_technic = None
    address = None
    moto_hours = None
    price = None
    price_unit = None
    header_ad = None
    document = None
    offer_datetime = None

    def __init__(self):

        pass

    def get_data(self):

        # Установить соединение с базой данных
        self.set_db_mongo()

        #
        self.get_last_id()

        # Установить dom запроса начальной поисковой страницы
        self.set_dom_init_research()

        self.get_data_research()

        # Сделать паузу перед парингом следующего объекта
        self.time_wait()

        while True:

            self.research_reference = self.dom_research.xpath("//a[@data-ftid='component_pagination-item-next']/@href")[0] # data-ftid="component_pagination-item-next"

            # Установить dom запроса поисковой страницы
            self.set_dom_research()

            self.get_data_research()

            # Сделать паузу перед парингом следующего объекта
            self.time_wait()


    def set_dom_init_research(self):

        """  """

        self.dom_research = self.get_dom(self.init_research_reference)

    def set_dom_research(self):

        """  """

        self.dom_research = self.get_dom(self.research_reference)


    def get_data_research(self):

        """  """

        for el in self.dom_research.xpath("//a[@class='css-1ctbluq ewrty961']"):
            self.research_ad(el)
            self.add_db()


    def research_ad(self, el):

        """  """

        self.reference_ad = el.xpath("./@href")[0]

        self.header_ad = el.xpath(".//span[@data-ftid='bull_title']/text()")[0]

        result = ResearchHeader(self.header_ad)
        self.maker_technic, self.model_technic, self.year_make = result.return_result()

        if len(self.maker_technic) > 30:
            self.maker_technic = self.maker_technic[0:29]

        self.type_technic = el.xpath(".//div[@class='css-15studg e3f4v4l0']/text()")[0]

        # Лошадиные силы и база
        if len(el.xpath(".//span[@class='css-159lyxl e162wx9x0']")) > 0:

            for j in el.xpath(".//span[@class='css-159lyxl e162wx9x0']"):

                if " л.с." in j.xpath("./text()")[0]:

                    temp = j.xpath("./text()")[0]

                    self.power_engine = float(temp[: temp.index(" л.с.")])

                elif "м/ч" in j.xpath("./text()")[0]:

                    temp = ''

                    for i in j.xpath("./text()")[0]:
                        if i.isdigit():
                            temp = temp + i

                    if temp != '':
                        self.moto_hours = float(temp)

                else:

                    self.technic_base = j.xpath("./text()")[0]

        self.price = af.get_digit(af.processing_text(el.xpath(".//span[@class='css-byj1dh e162wx9x0']/span/text()")[0]))

        if "₽" in el.xpath(".//span[@class='css-byj1dh e162wx9x0']/text()")[0]:
            self.price_unit = "рубль"

        if len(el.xpath(".//span[@class='css-1mj3yjd e162wx9x0']/text()")[0]) > 0:
            self.address = el.xpath(".//span[@class='css-1mj3yjd e162wx9x0']/text()")[0]

        temp = el.xpath(".//div[@data-ftid='bull_date']/text()")[0]
        try:
            self.offer_datetime = af.set_time_ad(temp)
        except Exception:
            self.offer_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)

        if len(el.xpath(".//div[@class='css-6tohdu ejipaoe0']")) > 0:
            self.condition_technic = el.xpath(".//div[@class='css-6tohdu ejipaoe0']/text()")[0]

        if len(el.xpath(".//div[@class='css-dgfad e9vb7pg0']")) > 0:
            self.document = 'отсутствуют'

    def add_db(self):

        """ """

        # Создать hex_code
        self.get_cript_id()

        # Передача полученных результатов в БД
        self.add_to_bd()

        # Показать результат
        self.print_result()

        # Обнулить сведения
        self.clean_result()



    def clean_result(self):

        # Обнуление сведений

        self.unique_id = None
        self.reference_ad = None
        self.type_technic = None
        self.technic_base = None
        self.maker_technic = None
        self.model_technic = None
        self.year_make = None
        self.power_engine = None
        self.condition_technic = None
        self.address = None
        self.price = None
        self.price_unit = None
        self.moto_hours = None
        self.header_ad = None
        self.offer_datetime = None
        self.document = None

    def print_result(self):

        """ Показать результат """

        print(f'reference_ad_: {self.reference_ad}')
        print(f'type_technic_: {self.type_technic}')
        print(f'technic_base_: {self.technic_base}')
        print(f'maker_technic: {self.maker_technic}')
        print(f'model_technic: {self.model_technic}')
        print(f'year_make____: {self.year_make}')
        print(f'power_engine_: {self.power_engine}')
        print(f'condition_technic: {self.condition_technic}')
        print(f'address______: {self.address}')
        print(f'price________: {self.price}')
        print(f'price_unit___: {self.price_unit}')
        print(f'moto_hours___: {self.moto_hours}')
        print(f'header_ad____: {self.header_ad}')
        print(f'offer_datetime: {self.offer_datetime}')
        print(f'document_____: {self.document}')

    @staticmethod
    def get_dom(reference_list):

        """ Получить dom """

        connect = Proxy(reference_list)
        # dom = connect.get_dom_own_ip()
        dom = connect.get_dom_proxy()
        return dom

    def set_db_mongo(self):

        """ Создание подключения к MongoDB """

        client = MongoClient('localhost', 27017)
        db = client[self.name_data_base]
        self.data_base = db.data_base

    def get_cript_id(self):

        """ Создание уникального специально хеш кода для проверки на наличие данного объекта в БД """

        self.unique_id = hashlib.sha1(f'{self.reference_ad}{self.offer_datetime}{self.header_ad}'.encode('utf-8')).hexdigest()

    def get_last_id(self):

        # Получить номер последнего ID
        sql_query = SqlDataBaseQuery()
        self.last_id = sql_query.query_last_id()

    def add_to_bd(self):

        """ Если данный объект в базе не присутствует, то добавление происходит """

        for n in self.data_base.find({'hex_id': self.unique_id}):
            self.check_id = 'stop'

        if self.check_id != 'stop':

            try:

                # # Получить номер последнего IP
                # sql_query = SqlDataBaseQuery()
                # last_id = sql_query.query_last_id()

                if self.last_id is None:
                    self.last_id = 1

                # Добавить коллекции значений в БД
                # self.add_object_sql(last_id)
                self.add_object_mongodb(self.last_id)

                self.last_id += 1

            except Exception as error:

                print(f'error: {error} --- {self.reference_ad}')

        else:
            print('ОБЪЕКТ В БД ИМЕЕТСЯ')

        self.check_id = None

    def add_object_sql(self, last_id):

        """ Добавить коллекцию значений в БД SQL """

        sql_add = SqlAddDromTechnic(id=last_id,
                                        hex_id=self.unique_id,
                                        reference_ad=self.reference_ad,
                                        header_ad=self.header_ad,
                                        type_technic=self.type_technic,
                                        price=self.price,
                                        price_unit=self.price_unit,
                                        offer_datetime=self.offer_datetime,
                                        address=self.address,
                                        model_technic=self.model_technic,
                                        year=self.year_make,
                                        condition=self.condition_technic,
                                        maker=self.maker_technic,
                                        moto_hours=self.moto_hours,
                                        power_engine=self.power_engine,
                                        technic_base=self.technic_base,
                                        document=self.document)

    def add_object_mongodb(self, last_id):

        """ Добавить коллекцию значений в БД MongoD """

        self.data_base.insert_one(
            {'_id': last_id, 'hex_id': self.unique_id, 'reference_ad': self.reference_ad,
             'header_ad': self.header_ad, 'type_technic': self.type_technic, 'price': self.price,
             'price_unit': self.price_unit, 'offer_datetime': self.offer_datetime, 'address': self.address,
             'model_technic': self.model_technic, 'year': self.year_make, 'condition': self.condition_technic,
             'maker': self.maker_technic, 'moto_hours': self.moto_hours, 'power_engine': self.power_engine,
             'technic_base': self.technic_base, 'document': self.document})

    @staticmethod
    def time_wait():

        """ Пауза между парсингои объявлений """
        time_wait = random.randint(50, 70)
        time.sleep(time_wait)


if __name__ == '__main__':

    result = DromResearch()
    result.get_data()


