from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Asset, Locker, User

Base = declarative_base()
engine = create_engine('sqlite:///asset_management.db')

Session = sessionmaker(bind=engine)

session = Session()

def main():
    user_input = 0
    wrong_command = 0
    while user_input != "4":
        print("***Welcome to Asset Management! Please select from the following choices!***")
        print("1) Check out asset!")
        print("2) Check in asset!")
        print("3) Inspect inventory!")
        print("4) Exit!")
        user_input = input()       
        if (user_input == "1"):
            print("Type Asset Type")
            searched_asset = input()
            print("Type Employee ID")
            res = session.query(Asset).filter(Asset.asset_type==searched_asset).all()
            print(f"Please see all available {searched_asset}'s below!")
            for asset in res:
                print(f"{asset.asset_id} {asset.asset_type} {asset.serial_number}")
            # print(res)
            print("Please select asset to check out by asset_id")
            checked_out_item = input()
            employee_id = int(input("Please type eeid to confirm"))
            query = session.query(Asset).filter(Asset.asset_id == checked_out_item)
            updated_record = query.first()
            employee_query = session.query(User).filter(User.ee_id==employee_id)
            
            session.delete(updated_record)
            session.commit()
            for record in query:
                print(f"{record.asset_type}(asset id: {record.asset_id}) has been checked out!")
            print(employee_query.first())
        elif (user_input=="2"):
            new_asset_type = input("Type asset type: ") 
            new_serial_number = input("Type serial number: ")
            new_user = input("Type your employee ID: ")
            new_locker_id = input("Type locker id: ")
            print(f"See locker number {new_locker_id} inventory check below!")
            new_asset = Asset(
                asset_type=new_asset_type,
                serial_number=new_serial_number,
                user_id = new_user,
                locker_id = new_locker_id,                
            )
            session.query(Locker).filter(Locker.locker_id==new_locker_id).update({
                Locker.asset_count:Locker.asset_count+1
            })
            session.query(User).filter(User.ee_id==new_user).update({
                User.checked_out_asset:User.checked_out_asset+1
            })
            session.add(new_asset)
            session.commit()            
        elif(user_input=="3"):
            print("Please enter a locker number")
            lockerName= input()
            locker_count = session.query(Locker).filter(Locker.locker_name==lockerName)
            for record in locker_count:
                print(f"Locker balance is {record.asset_count} assets!")            
        elif(user_input == "4"):
            print("Terminating program!")
        else:
            wrong_command += 1
            print(f"You entered a wrong command {wrong_command} times!")
            print("Please choose again.")
    print("You exited the application!")
        
if __name__ == '__main__': 
    main()
    
