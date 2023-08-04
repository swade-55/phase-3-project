# lib/models.py
from sqlalchemy import create_engine, func, MetaData
from sqlalchemy import ForeignKey,Column, Integer,String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
engine = create_engine('sqlite:///asset_management.db')

Base = declarative_base()

# asset_user = Table(
#     'asset_users',
#     Base.metadata,
#     Column('locker_id', ForeignKey('lockers.locker_id'), primary_key=True),
#     Column('ee_id', ForeignKey('users.ee_id'),primary_key=True),
#     extend_existing=True
# )
    
class User(Base):
    __tablename__ = 'users'
    
    ee_id = Column(Integer(),primary_key = True)
    full_name = Column(String())
    user_group = Column(String())
    badge_number = Column(Integer())
    checked_out_asset = Column(Integer())
    
    assets = relationship('Asset',backref=backref('user'))
    
    def __repr__(self):
        return f'{self.full_name}({self.ee_id}) has {self.checked_out_asset} checked out under her name!'
    
class Locker(Base):
    __tablename__ = 'lockers'
    
    locker_id = Column(Integer(),primary_key=True)
    locker_name = Column(String())
    locker_serial_number = Column(Integer())
    asset_count = Column(Integer())
    last_updated_at = Column(DateTime(), onupdate=func.now())
    
    assets = relationship('Asset',backref=backref('locker'))
    
    
    
    def __repr__(self):
        return f'locker (id={self.locker_id}, ' + \
            f'name={self.locker_name})'
    
class Asset(Base):
    __tablename__ = 'assets'
    
    asset_id = Column(Integer(),primary_key = True)
    asset_type = Column(String())
    serial_number = Column(Integer())
    device_location = Column(Integer())
    slot_location = Column(Integer())
    owner = Column(String())
    status_changed_at = Column(DateTime(), server_default=func.now())
    user_id = Column(Integer(), ForeignKey('users.ee_id'))
    locker_id = Column(Integer(), ForeignKey('lockers.locker_id'))
    
    
    def __repr__(self):
        return f'Asset(id={self.asset_id}, ' + \
            f'type={self.asset_type})'
    

    
    
    

    