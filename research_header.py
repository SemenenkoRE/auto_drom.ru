import list_technic as lt

expr_l_s = ['л.с.', 'л. с.', ' л с ', ' л с,', ' лс ', ' лс,', 'л.с', 'л/с']

special_symbols = ['.', '_', '/', '-']

class ResearchHeader():

    """ Класс анализирует заголовок объявления и возращает готовые параметры """

    TYPES_TECHNIC = lt.list_type
    MAKER_TECHNIC = lt.list_maker_traktor

    maker_technic = None
    model_technic = None
    year_make = None
    text_header = None

    def __init__(self, text_header):

        self.text_header = text_header.replace(', ', ' ')

        # Основная обработка
        self.set_parameters()

    def set_parameters(self):

        """  """
        research_list = []

        # Делим текст заголовка по пробелам

        if ' ' in self.text_header:
            research_list = self.text_header.split(' ')[:]
        else:
            research_list = [self.text_header][:]


        if len(research_list) == 3:
            self.model_technic = research_list[1]

        if research_list[-1].isdigit():
            self.year_make = float(research_list[-1])

        # Перебор элементов полученного списка

        for el in research_list:

            status = True

            # 3. Определение производителя

            for j in self.MAKER_TECHNIC:

                if status is True:

                    for q, w in j.items():

                        if status is True:

                            for x in w:

                                # Проверка для названий производителя из 2х слов
                                if ' ' in x:
                                    if x in self.text_header.lower():
                                        self.maker_technic = q
                                        status = False
                                        break
                                else:

                                    if el.lower() == x:
                                        self.maker_technic = q
                                        status = False
                                        break

                                    elif x in el.lower():
                                        self.maker_technic = q

            # 5. Определение модели

            if status is True and self.model_technic is None:

                test_upper_case = True
                test_lower_case = True
                test_digit = True
                test_upper_many = True
                test_special_symbols = True

                for j in el:

                    if j.isdigit():
                        test_digit = False

                    elif j.isupper():

                        if test_upper_case is False:
                            test_upper_many = False
                        else:
                            test_upper_case = False

                    elif j.isupper() is False:
                        test_lower_case = False

                    else:
                        for x in special_symbols:
                            if j == x:
                                test_special_symbols = False

                if (test_special_symbols is False and test_digit is False) or \
                        (test_upper_many is False) or \
                        (test_upper_case is False and test_digit is False) or \
                        (test_special_symbols is False and test_lower_case is False) or \
                        (test_lower_case is False and test_digit is False):

                    if self.model_technic is not None:
                        self.model_technic = f'{self.model_technic} {el}'
                        status = False
                    else:
                        self.model_technic = el
                        status = False

        if self.maker_technic is None:
            self.maker_technic = research_list[0]


    def return_result(self):

        return self.maker_technic, self.model_technic, self.year_make

    def print_result(self):

        print(f'производитель: {self.maker_technic}')
        print(f'модель       : {self.model_technic}')
        print(f'год выпуска  : {self.year_make}')

if __name__ == '__main__':

    header = 'Алтайлесмаш ТЛ-4, 2022'

    parameters = ResearchHeader(header)
    print(parameters.return_result())


