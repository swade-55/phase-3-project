#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Asset, Locker, User

if __name__ == '__main__':
    engine = create_engine('sqlite:///asset_management.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Asset).delete()
    session.query(Locker).delete()
    session.query(User).delete()

    fake = Faker()

    types = ['Radio', 'iPad', 'RF Scanner',
        'Vocollect', 'Zebra Scanner']
    user_groups = ['Selector', 'Management','Loader','Forklift Operator']
    locker_names = ['one','two']

        
    users = []
    for i in range(50):
        user = User(
            full_name=fake.unique.name(),
            user_group=random.choice(user_groups),
            badge_number= random.randint(1,5000),
            checked_out_asset= 0,           
        )

        session.add(user)
        session.commit()
        users.append(user)        
    
    
        assets = []
    for i in range(50):
        asset = Asset(
            asset_type=random.choice(types),
            serial_number=random.randint(1005, 1060),
            device_location= random.randint(1, 10),
            owner=None, 
            # how to populate locker_id with actual data?   
            user_id = 100,
            locker_id = random.randint(1,2),       
        )

        session.add(asset)
        session.commit()
        assets.append(asset)
        
        lockers = []
    for i in range(2):
        locker = Locker(
            locker_name=(locker_names[i]),
            locker_serial_number=random.randint(5, 60),
            asset_count=session.query(Asset).filter_by(locker_id=i+1).count(),          
        )
        session.add(locker)
        session.commit()
        lockers.append(locker)
