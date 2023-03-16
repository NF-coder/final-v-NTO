#import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
#from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from sqlalchemy.orm import Session, sessionmaker
import datetime
from sqlalchemy import select

Base = declarative_base()

class Login_bd(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    def __repr__(self):
        return f"<Customer(id={self.id}, user={self.user}, password={self.password})>"

class Ticker_bd(Base):
    __tablename__ = 'tickers'
    id = Column(Integer, primary_key=True)
    ticker = Column(String(100), nullable=False)
    cost = Column(String, nullable=False)
    last = Column(String, nullable=False)
    def __repr__(self):
        return f"<Customer(id={self.id}, ticker={self.ticker}, cost={self.cost}, last={self.last})>"

class Portf_bd(Base):
    __tablename__ = 'portf'
    user = Column(Integer, primary_key=True)
    portfs = Column(String, nullable=False)
    weights = Column(String, nullable=False)
    def __repr__(self):
        return f"<Customer(id={self.id}, user={self.user}, portfs={self.portfs}, weights={self.weights})>"

class BD:
    def __init__(self):
        global Base
        self.engine = create_engine("postgresql://code:1eera4wDDDe@localhost/db")
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def login_infos(self):
        session = self.session
        customers = session.query(Login_bd).all()
        session.close()
        return customers

    def create_user(self,USER,PWD):
        session = self.session
        new_customer = Login_bd(user=USER, password=PWD)
        session.add(new_customer)
        session.commit()
        session.close()

    def all_portf_get(self):
        session = self.session
        act = session.query(Portf_bd).all()
        session.close()
        return act

    def portf_add(self, act: list, weights: list, USER):
        session = self.session
        act = " ".join(list(map(str,act)))
        weights = " ".join(list(map(str, weights)))
        new_customer = Portf_bd(user=USER, portfs=act, weights=weights)
        session.add(new_customer)
        session.commit()
        session.close()

    def all_act_get(self):
        session = self.session
        act = session.query(Ticker_bd).all()
        session.close()
        return act

    def act_add(self, cost: list, ticker: str):
        session = self.session
        cost = " ".join(list(map(str, cost)))
        now = datetime.datetime.now()
        new_customer = Ticker_bd(ticker=ticker, cost=cost, last=now.strftime("%Y-%m-%d"))
        session.add(new_customer)
        session.commit()
        session.close()

    def act_upd(self,cost: list,ticker:str):
        session = self.session
        cost = " ".join(list(map(str, cost)))
        act = select(Ticker_bd).where(Ticker_bd.c.ticker == ticker)
        act.cost = cost
        now = datetime.datetime.now()
        act.date = now.strftime("%Y-%m-%d")
        session.flush()
        session.close()
