from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_create import DromTechnic
from sqlalchemy import desc
from sqlalchemy.pool import NullPool
import datetime


class SqlAddDromTechnic:

    """  """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_drom", poolclass=NullPool, echo=True)

    def __init__(self, **kwargs):
        self.filling_data(kwargs)

    def filling_data(self, values_collection):
        session = sessionmaker(bind=self.engine)
        session = session()
        session.add(DromTechnic(id=values_collection['id'],
                                            hex_id=values_collection['hex_id'],
                                            reference_ad=values_collection['reference_ad'],
                                            header_ad=values_collection['header_ad'],
                                            type_technic=values_collection['type_technic'],
                                            price=values_collection['price'],
                                            price_unit=values_collection['price_unit'],
                                            offer_datetime=values_collection['offer_datetime'],
                                            address=values_collection['address'],
                                            model_technic=values_collection['model_technic'],
                                            year=values_collection['year'],
                                            condition=values_collection['condition'],
                                            maker_technic=values_collection['maker'],
                                            moto_hours=values_collection['moto_hours'],
                                            power_engine=values_collection['power_engine'],
                                            technic_base=values_collection['technic_base'],
                                            document=values_collection['document']))

        session.commit()
        session.remove()


class SqlDataBaseQuery:

    """  """

    engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_drom", echo=True)

    def __init__(self):
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    def query_delete_row(self, research_id):

        """ """

        result = self.session.query(DromTechnic).all()

        for row in result:
            if row.id == research_id:
                self.session.delete(row)
                self.session.commit()


    def query_last_id(self):

        """ Получение унркального id для добавляемой строки """

        last_id = None
        result = self.session.query(DromTechnic).order_by(desc(DromTechnic.id))

        for row in result:
            last_id = row.id + 1
            break

        return last_id


if __name__ == '__main__':

    sql_query = SqlDataBaseQuery()
    # sql_query.query_get_all()
    # sql_query.query_get_data_id(45)
    sql_query.query_delete_row(1)
    # print(sql_query.query_get_last_id())

    pass

