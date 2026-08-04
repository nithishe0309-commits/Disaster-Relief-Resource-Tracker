import pymysql
from datetime import datetime
conn=pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="tracker"
    )
cursor=conn.cursor()
cursor.execute("use tracker")
            
tables=["""
         create table if not exists affected_areas(
         id int auto_increment primary key,
         area_name varchar(60) not null,
         disaster_type varchar(60) not null)
         """,
        """
        create table if not exists supplies(
         id int auto_increment primary key,
         item_name varchar(50)not null,
         quantity int)
         """,
        """
        create table if not exists volunteers(
         id int auto_increment primary key,
         name varchar(100),
         age int,
         phone varchar(10) not null,
         assigned_area_id int not null,
         foreign key (assigned_area_id) references affected_areas(id))
         """,
        
        """
        create table if not exists distribution(
         id int auto_increment primary key,
         volunteer_id int,
         supply_id int,
         area_id int,
         quantity_distributed int,
         distribution_date date,
         foreign key(supply_id) references supplies(id),
         foreign key(area_id) references affected_areas(id),
         foreign key(volunteer_id) references volunteers(id))
         """
        ]
for table in tables:
    cursor.execute(table)
conn.commit()
def add_affected_area():
    print("\n🗺 Add New Affected Area Details 🗺")
    area_name=input("Enter Area Name:")
    disaster_type=input("Enter Disaster Type (Flood|cyclone|Earthquake|etc.):")
    sql="insert into affected_areas (area_name,disaster_type) values (%s,%s)"
    values=(area_name,disaster_type)
    cursor.execute(sql,values)
    conn.commit()
    print("✅Area Added successfully!")

def add_volunteer():
    print("\n👥 Add New Volunteer Details 👥")
    name=input("Enter Volunteer Name:")
    try:
        age=int(input("Enter Volunter Age:"))
    except ValueError:
        print("❌Age must be a number!")
        return
    phone=int(input("Enter Volunter Phone Number(10-digits):"))
    cursor.execute("select id,area_name,disaster_type from affected_areas")
    areas=cursor.fetchall()
    if not areas:
        print("ERROR:No affected areas found!")
        print("PLEASE add an affected area first")
        return
    print("\n🗺 Avialable Affected Areas 🗺")
    print("-"*50)
    print("ID | Area Name | Disaster Type")
    print("-"*50)
    for area in areas:
        print(f"{area[0]:2} | {area[1]:15} | {area[2]:5}")
    print("-"*50)
    try:
        assigned_area_id=int(input("Enter Area ID to assign this Volunteer to:"))
    except ValueError:
        print("❌Area ID must be a number!")
        return
    cursor.execute("select id from affected_areas where id=%s",(assigned_area_id,))
    if not cursor.fetchall():
        print(f"ERROR: Area ID {assigned_area_id} doesn't exist!")
        return
    sql="insert into volunteers (name,age,phone,assigned_area_id) values(%s,%s,%s,%s)"
    values=(name,age,phone,assigned_area_id)
    cursor.execute(sql,values)
    conn.commit()
    print(f"✅Volunteer {name} Added Successfully!")
    print(f"Assigned to Area ID:{assigned_area_id}")

def add_supply():
    print("\n📦Add New Supply Details📦")
    item_name=input("Enter the Item Name:")
    try:
        quantity=int(input("Enter the Quantity:"))
    except ValueError:
        print("❌Quantity must be a number!")
        return
    sql="insert into supplies (item_name, quantity) values(%s,%s)"
    values=(item_name,quantity)
    cursor.execute(sql,values)
    conn.commit()
    print(f"✅Supply {item_name} Added Successfully!")

def record_distribution():
    print("\n🚚 Record Distibutions 🚚")
    today=datetime.now().strftime("%Y-%m-%d")
    print("\n👥 Available Volunteers")
    cursor.execute("SELECT id, name, phone FROM volunteers")
    volunteers = cursor.fetchall()
    if not volunteers:
        print("❌ No volunteers found! Add volunteers first.")
        return
    print("-" * 40)
    print("ID|   Name    | Phone")
    print("-" * 40)
    for vol in volunteers:
       print(f"{vol[0]:2} | {vol[1]:20} | {vol[2]:15}")
    print("-" * 40)
    try:
        volunteer_id=int(input("Enter Volunteer ID Who Distributed:"))
    except ValueError:
        print("❌Volunteer ID must be a number!")
        return
    print("\n📦 Available Supplies 📦")
    cursor.execute("SELECT id, item_name, quantity FROM supplies WHERE quantity > 0")
    supplies = cursor.fetchall()
    if not supplies:
        print("❌ No supplies available! Add supplies first.")
        return
    print("-" * 50)
    print("ID|  Item Name    | Quantity")
    print("-" * 50)
    for sup in supplies:
        print(f"{sup[0]:2} | {sup[1]:25} | {sup[2]:6}")
    print("-" * 50)
    try:
        supply_id=int(input("Enter Supply ID Distributed:"))
    except ValueError:
        print("❌Supply ID must be a number!")
        return
    print("\n🗺 Available Areas 🗺")
    cursor.execute("SELECT id, area_name, disaster_type FROM affected_areas")
    areas = cursor.fetchall()
    if not areas:
        print("❌ No affected areas found! Add areas first.")
        return
    print("-" * 50)
    print("ID | Area Name | Disaster Type")
    print("-" * 50)
    for area in areas:
        print(f"{area[0]:2} | {area[1]:20} | {area[2]:15}")
    print("-" * 50)
    try:
        area_id=int(input("Enter Area ID Where Distributed:"))
    except ValueError:
        print("❌Area ID must be a number!")
        return
    try:
        quantity=int(input("Enter the Quantity Distributed:"))
    except ValueError:
        print("❌Quantity must be a number!")
        return
    sql="insert into distribution(volunteer_id,supply_id,area_id,quantity_distributed,distribution_date)values (%s,%s,%s,%s,%s)"
    values=(volunteer_id,supply_id,area_id,quantity,today)
    cursor.execute(sql,values)
    conn.commit()
    print("✅Distribution Recorded Successfully!")
    print(f"📅Date:{today}")
    
        
def view_data():
    print("🔍 ---VIEW DATA--- 🔍")
    print("1. View Affected Areas🗺")
    print("2. View Volunteers with Assigned Area👥")
    print("3. View Supplies📦")
    print("4. View Distribution Records🚚")
    print("5. Back to Main Menu🏠")
    try:
        choice=int(input("Enter Your Choice(1-5):"))
    except valueError:
        print("❌ Please enter a number!")
        return
    if choice==1:
        cursor.execute("select*from affected_areas")
        areas = cursor.fetchall()
        print("\n---🗺 Affected Areas 🗺---")
        print("ID|   Area Name         | Disaster Type")
        print("-" * 50)
        for area in areas:
            print(f"{area[0]:2}| {area[1]:20} | {area[2]:15}")
    elif choice==2:
        cursor.execute("""select v.id,v.name,v.age,v.phone,a.area_name from volunteers v
                          join affected_areas a on v.assigned_area_id = a.id
                          order by v.id
                          """)
        volunteers=cursor.fetchall()
        print("\n---👥 Volunteers 👥---")
        print("ID | Volunteer's Name     | Age | Phone Number    | Assigned Area")
        print("-"*70)
        for vol in volunteers:
            print(f"{vol[0]:2} | {vol[1]:20} | {vol[2]:3} | {vol[3]:15} | {vol[4]:25}")
    elif choice==3:
        cursor.execute("select*from supplies")
        supplies=cursor.fetchall()
        print("\n---📦 Supplies 📦---")
        print("ID|     Item Name             | Quantity")
        print("-"*50)
        for sup in supplies:
            print(f"{sup[0]:2}| {sup[1]:25} | {sup[2]:6}")
    elif choice==4:
        cursor.execute("""
                        select d.id,v.name,s.item_name,a.area_name,d.quantity_distributed,d.distribution_date from distribution d
                        join volunteers v on d.volunteer_id=v.id
                        join supplies s on d.supply_id=s.id
                        join affected_areas a on d.area_id=a.id
                        order by d.id
                        """)
        distributions=cursor.fetchall()
        print("\n---🚚 Distributions Records 🚚---")
        print("ID |   Volunteer          |   Item Name                    |   Area               | Qty  |Date")
        print("-"*105)
        for dist in distributions:
            print(f"{dist[0]:2} | {dist[1]:20} | {dist[2]:30} | {dist[3]:20} | {dist[4]:4} | {dist[5]}")
    elif choice==5:
         return
    else:
        print("❌INVALID CHOICE! Please Try Again.")

def main_menu():
    while True:
        print("="*50)
        print("DISASTER RELIEF RESOURCE TRACKER🌀🌋")
        print("="*50)
        print("1. Add New Volunteer👥")
        print("2. Add New Affected Area🗺")
        print("3. Add Supply📦")
        print("4. Record Distribution🚚")
        print("5. View Data🔍")
        print("6. Exit👋")
        print("="*50)

        choice=input("Enter Your Choice (1-6): ")
        if choice == '1':
            add_volunteer()
        elif choice == '2':
            add_affected_area()
        elif choice == '3':
            add_supply()
        elif choice == '4':
            record_distribution()
        elif choice == '5':
            view_data()
        elif choice == '6':
            print("Thank You for using Disaster Relief Resource Tracker!👋")
            break
        else:
            print("❌INVALID Choice! Please Enter 1-6.")
main_menu()
cursor.close()
conn.close()

