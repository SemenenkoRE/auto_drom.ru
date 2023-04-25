from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:111111@localhost/data_base_drom", poolclass=NullPool, echo=True)
Base = declarative_base()


class DromTechnic(Base):
    __tablename__ = 'sh_technic_drom'

    id = Column(Integer, primary_key=True)
    hex_id = Column(String(40), unique=True)
    reference_ad = Column(String(255), nullable=False)
    header_ad = Column(String(255), nullable=False)
    type_technic = Column(String(30), nullable=True)
    price = Column(Float, nullable=True)
    price_unit = Column(String(10), nullable=False)
    offer_datetime = Column(DateTime, nullable=False)
    address = Column(String(250), nullable=True)
    model_technic = Column(String(30), nullable=True)
    year = Column(Float, nullable=True)
    condition = Column(String(30), nullable=True)
    maker_technic = Column(String(30), nullable=True)
    moto_hours = Column(Float, nullable=True)
    power_engine = Column(Float, nullable=True)
    technic_base = Column(String(30), nullable=True)
    document = Column(String(15), nullable=True)

Base.metadata.create_all(engine)

