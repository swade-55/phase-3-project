from datetime import datetime
from sqlalchemy import (create_engine, desc,
    Index, Column, DateTime, Integer, String,func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Asset, Locker, User

Base = declarative_base()
engine = create_engine('sqlite:///asset_management.db')

Session = sessionmaker(bind=engine)

session = Session()


#takeaways
#checks that input validation
#while loop to keep continuing application



if __name__ == '__main__':    
    print("Welcome to Asset Management! Please enter ee_id to begin!")
    employee_id = int(input())
    print("Please Enter 1-CheckOut,2-CheckIn,3-Check Inventory, 4- Exit Application")
    x = input()
    
    while x != "4":
        
        if (x == "1"):
            print("Type Asset Type")
            searched_asset = input()
            print("Type Employee ID")
            res = session.query(Asset).filter(Asset.asset_type==searched_asset).all()
            print(res)
            print("Please select asset to check out by asset_id")
            checked_out_item = input()
            #why do i have to redeclare the employee_id variable?
            employee_id = int(input("Please type eeid to confirm"))
            query = session.query(Asset).filter(Asset.asset_id == checked_out_item)
            updated_record = query.first()
            employee_query = session.query(User).filter(User.ee_id==employee_id)
            employee_updated = employee_query.update({
                User.checked_out_asset:User.checked_out_asset+1
            })
            
            session.delete(updated_record)
            session.commit()
            # why is this not printing out?
            for record in query:
                print(f"{record.asset_type}(asset id: {record.asset_id}) has been checked out!")
            print(employee_query.first())
        elif (x=="2"):
            new_asset_type = input("Type asset type: ") 
            new_serial_number = input("Type serial number: ")
            new_device_location = input("Type locker location: ")
            new_owner = input("Type your employee ID: ")
            new_user = input("Type your employee ID: ")
            new_locker_id = input("Type locker id: ")
            print("done")
            new_asset = Asset(
                asset_type=new_asset_type,
                serial_number=new_serial_number,
                device_location=new_device_location,
                owner = new_owner,
                user_id = new_user,
                locker_id = new_locker_id,                
            )
            session.query(Locker).update({
                Locker.asset_count:Locker.asset_count+1
            })
            session.add(new_asset)
            session.commit()            
        elif(x=="3"):
            print("Please enter a locker number")
            lockerName= input()
            locker_count = session.query(Locker).filter(Locker.locker_name==lockerName)
            for record in locker_count:
                print(f"Locker balance is {record.asset_count} assets!")            
        else:
            print("You entered a number that wasn't recognized! Please try again!")
    else:
        print("You exited the application!")
    
# Questions:
# how to redirect user to main menu when they're done with transaction?
# why isn't lockers table updating count when i use check in functionality?
    