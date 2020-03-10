from sqlalchemy.ext.declarative import  declarative_base
from sqlalchemy import  Column, Integer, String, Date

Base = declarative_base()
Base
class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    id_str = Column(String)
    created_at = Column(Date)
    user_id = Column(String)
    language = Column(String)
    geo = Column(String)
    text = Column(String)
    coordinates = Column(String)

    def __repr__(self):
        return "<id_str='{}', created_at='{}', user_id='{}', language='{}', geo='{}', text='{}', coordinates='{}')"\
            .format(self.id_str, self.created_at, self.user_id, self.language, self.geo, self.text, self.coordinates)


class Retweets(Base):
    __tablename__ = 'retweets'
    id = Column(Integer, primary_key=True)
    origin_id_str = Column(String)
    id_str = Column(String)
    created_at = Column(Date)
    user_id = Column(String)
    language = Column(String)
    geo = Column(String)
    text = Column(String)
    coordinates = Column(String)

    def __repr__(self):
        return "<origin_id_str='{}' id_str='{}', created_at='{}', user_id='{}', language='{}', geo='{}', text='{}', coordinates='{}')"\
            .format(self.origin_id_str, self.id_str, self.created_at, self.user_id, self.language, self.geo, self.text, self.coordinates)

