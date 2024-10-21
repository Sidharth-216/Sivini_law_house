print("                 T S S P D C L                  ")
print("                  ELECTRICITY                  ")
print("                 BILL-CUM NOTICE                  ")
print(" IP Southern ")
print("Odisha Distribution Ltd")
print("Bill Of Supply For")
print("Electricity")
print("************************************************************")
import random
import sqlite3
import datetime
from database import connect_to_database
import time
now=datetime.datetime.now()
print("DATE:",now.strftime("%d-%m-%Y"),"    ", "TIME:",now.strftime("%H:%M:%S"))
mina=100000
maxa=999999
mini=1000
maxi=9999
mixa1=9100000000
mini1=9999999999
mobo=random.randint(mixa1,mini1)
enc=random.randint(mini,maxi)
areacd=random.randint(mina,maxa)
print(f"\nAREA CODE:{areacd}","      ",f"ERONo:{enc}",end=' ')
print(f"\nMOB NO:+91 {mobo}")
base_charge_rates = {
    "<= 150 units (kWh)": 3.25,
    "> 150 - <= 400 (kWh)": 4.22,
    "> 400 (kWh)": 4.42,}
fuel_adjustable_charge_rate = 0.6689
service_charge = 24.62
tax_rate = 0.07  # 7% tax rate

# Connect to your MySQL database
def connect_to_database():
    return sqlite3.connect('lawfirm.db', timeout=30)  # Increased timeout
#(host= "localhost",user= "root",password= "sidharth#21605@patnaik",database= "electricbill")
print("Database connection successful.")

def execute_with_retry(query, params=(), retries=5):
    for attempt in range(retries):
        try:
            with connect_to_database() as conn:
                conn.execute('PRAGMA journal_mode=WAL;')  # Enable Write-Ahead Logging
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                time.sleep(0.5)  # Wait before retrying
            else:
                raise  # Re-raise the exception if it's not a lock issue or max retries reached


# Create a cursor to interact with the database


def initialize_database():
    try:
        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS electirc_bill (
            bill_id TEXT PRIMARY KEY,
            previous_month_status TEXT,
            previous_month_amount REAL,
            current_month_bill REAL
        );
    ''')

        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS electirc_bill (
            bill_id TEXT PRIMARY KEY,
            previous_month_status TEXT,
            previous_month_amount REAL,
            current_month_bill REAL
        );
    ''')
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
# Call this function when your application starts
initialize_database()

# Function to create the electirc_bill table
connection = connect_to_database()
cursor = connection.cursor()


# Query to retrieve the previous month's bill status and amount, and the current month's bill
# Query to retrieve the previous month's bill status and amount, and the current month's bill
result = cursor.execute("SELECT previous_month_status, previous_month_amount, current_month_bill FROM electirc_bill ORDER BY bill_id DESC LIMIT 1").fetchall()


# Debugging: Print the result to see what it contains
print("Query Result:", result)

# Check if result is not empty before accessing its elements
if result:
    previous_month_status, previous_month_amount, current_month_bill = result[0]
else:
    print("No records found for the given bill ID.")
    previous_month_status, previous_month_amount, current_month_bill = None, None, None  # Set to None or handle as needed

# Continue with the rest of your code...
# Now you can safely execute queries on the electirc_bill table
# Example: Check if the table was created successfully
try:
    cursor.execute("SELECT * FROM electirc_bill")
    print("Table 'electirc_bill' exists and is ready for use.")
except sqlite3.OperationalError:
    print("Table 'electirc_bill' does not exist.")


# Extract the status, amount, and current month's bill
previous_month_status, previous_month_amount, current_month_bill,bill_id = result[0],result[0],result[0],result[0]


# Display the status, amount, and the current month's bill
print("\nEx:-(ec2001,ec2002.........ec2004)\n")

c=input("bill_id:")
if c=='ec2001':
    print("NAME:SIDHARTH PATNAIK")
    print("AGE:23")
    print("Meter Reader NO:9437458266")
    if previous_month_status == "unpaid":
        print(f"Previous Month's Bill: Due with an amount of ₹{previous_month_amount}")
    else:
        print(f"Previous Month's Bill: Paid with an amount of =₹{previous_month_amount[2]}")
        print("no due")
        units=float(input("enter the unit="))
        if units > 0 and units <= 100:
            print("TYPE:DOMESTIC")
            tax=(units*1.4)/100
            print("total tax",tax)
            payment = units * 1.5+tax
            fixedCharge = 25 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    
        elif units > 100 and units <= 200:
            print("TYPE:DOMESTIC")
            tax=(units*2.4)/100
            print("total tax=",tax)
            payment = (100 * 1.5) + (units - 100) * 2.5+tax
            fixedCharge = 50 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 200 and units <= 300:
            print("TYPE:DOMESTIC")
            tax=(units*3.4)/100
            print("total tax",tax)
            payment =  (100 * 1.5) + (200 - 100) * 2.5 + (units - 200) * 4+tax
            fixedCharge = 75 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 300 and units <= 350:
            print("TYPE:DOMESTIC")
            tax=(units*5.4)/100
            print("total tax",tax)
            payment = (100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300) * 5+tax   
            fixedCharge = 100 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units >350:
            print("TYPE:COMMECRIAL")
            appliances={}
            #Function to input appliance data
            print("************************************************************")
            def input_appliances():
                while True:
                    appliance_name = input("Enter the name of the appliance (or 'done' to finish): ")
                    if appliance_name.lower() == 'done':
                        break
                    power_consumption = float(input(f"Enter the power consumption of {appliance_name} (in watts): "))
                    daily_usage_hours = float(input(f"How many hours do you generally use {appliance_name} per day? "))
                    appliances[appliance_name] = {"power_consumption": power_consumption,"daily_usage_hours": daily_usage_hours,}
            input_appliances()
            # Function to calculate the monthly electricity cost
            def calculate_electricity_cost(appliances):
                total_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())*30 / 1000  # Convert total power to kWh or unit per month
                base_charge = 0
                total_cost_with_tax=0
               

                # Calculate the base charge based on usage
                if total_power <= 150:
                    base_charge = total_power * base_charge_rates["<= 150 units (kWh)"]
                elif total_power <= 400:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + (total_power - 150) * base_charge_rates["> 150 - <= 400 (kWh)"]
                else:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + 250 * base_charge_rates["> 150 - <= 400 (kWh)"] + (total_power - 400) * base_charge_rates["> 400 (kWh)"]
                    fuel_adjustable_charge = total_power * fuel_adjustable_charge_rate
                    total_cost_before_tax = base_charge + fuel_adjustable_charge + service_charge
                    total_cost_with_tax = total_cost_before_tax * (1 + tax_rate)
                    print("total__bill",total_cost_with_tax)
                return total_cost_with_tax
            # Calculate the monthly electricity cost
            monthly_cost = calculate_electricity_cost(appliances)
            print("************************************************************")
            def suggest_appliance_adjustments(appliances, target_bill):
                current_cost = calculate_electricity_cost(appliances)
                adjustments = {}
                if current_cost <target_bill:
                    adjustments["message"] = "You are currently under your target bill."
                else:
                    adjustments["message"] = "You are currently over your target bill."
                    remaining_cost = current_cost - target_bill

                    # Calculate the total daily power consumption
                    total_daily_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())

                    if total_daily_power == 0:
                        adjustments["message"] = "It is not possible to reach your target bill with the current appliances."
                    else:
                        print("************************************************************")
                        # Calculate the maximum reduction possible to get to the target bill
                        max_possible_reduction_hours = remaining_cost / (total_daily_power / 1000)
                        for appliance_name, appliance_data in appliances.items():
                            # Reduce usage of each appliance by the same proportion
                            reduction_ratio = appliance_data["power_consumption"] * appliance_data["daily_usage_hours"] / total_daily_power
                            hours_to_reduce = min(max_possible_reduction_hours * reduction_ratio, appliance_data["daily_usage_hours"])
                            adjustments[appliance_name] = hours_to_reduce
                            
                return adjustments
            # Let users input the target monthly electricity bill
            target_bill = float(input("Enter your target monthly electricity bill amount: "))

            # Suggest adjustments to meet the target bill
            adjustments = suggest_appliance_adjustments(appliances, target_bill)
            # Display suggestions to meet the target bill
            print(adjustments["message"])
            print("\nSuggested Appliance Usage Adjustments:")
            for appliance, hours in adjustments.items():
                if appliance != "message":
                    print(f"Reduce usage of {appliance} by {hours:2f} hours per day")
        

                 
            print("************************************************************")
            tax=(units*8.4)/100
            print("total tax",tax)
            payment=(100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300)*6
            print("bill:",payment)
            carbonem=payment+(units*8)/100
            print("************************************************************")
            print("carbon emmision tax:",carbonem)
            print("energy consuption is more ")
            print("************************************************************")
            fixedCharge=1000
            payment=payment+carbonem+tax
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    d=[]
    try:
        d.append(total)
        
        e=str(d[0])
        cursor=connection.cursor()
    except:
        print("unable to update")
    update_query="UPDATE electirc_bill SET current_month_bill =" + e +"WHERE bill_id='" + c +"'"
    #inserting the calculated data into the specific column
    cursor.execute(update_query)
    p="SELECT current_month_bill FROM electirc_bill where bill_id='ec2001'"
    cursor.execute(p)
    h=cursor.fetchall()
    val = h[0][0]    
    print("current amount:₹",val)
    #commit the changes and close the connection
    connection.commit()
    connection.close()
   
elif c=='ec2002':
    print("NAME:SUMIT PATNAIK")
    print("AGE:24")
    print("Meter Reader NO:9678543632")
    if previous_month_status == "unpaid":
        print(f"Previous Month's Bill: Due with an amount of ₹{previous_month_amount}")
    else:
        print(f"Previous Month's Bill: Paid with an amount of =₹{previous_month_amount[2]}")
        print("no due")
        units=float(input("enter the unit="))
        if units > 0 and units <= 100:
            print("TYPE:DOMESTIC")
            tax=(units*1.4)/100
            print("total tax",tax)
            payment = units * 1.5+tax
            fixedCharge = 25 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    
        elif units > 100 and units <= 200:
            print("TYPE:DOMESTIC")
            tax=(units*2.4)/100
            print("total tax=",tax)
            payment = (100 * 1.5) + (units - 100) * 2.5+tax
            fixedCharge = 50 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 200 and units <= 300:
            tax=(units*3.4)/100
            print("total tax",tax)
            payment =  (100 * 1.5) + (200 - 100) * 2.5 + (units - 200) * 4+tax
            fixedCharge = 75 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 300 and units <= 350:
            print("TYPE:DOMESTIC")
            tax=(units*5.4)/100
            print("total tax",tax)
            payment = (100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300) * 5+tax   
            fixedCharge = 100 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units >350:
            print("TYPE:COMMERCIAL")
            appliances={}
            #Function to input appliance data
            print("************************************************************")
            def input_appliances():
                while True:
                    appliance_name = input("Enter the name of the appliance (or 'done' to finish): ")
                    if appliance_name.lower() == 'done':
                        break
                    power_consumption = float(input(f"Enter the power consumption of {appliance_name} (in watts): "))
                    daily_usage_hours = float(input(f"How many hours do you generally use {appliance_name} per day? "))
                    appliances[appliance_name] = {"power_consumption": power_consumption,"daily_usage_hours": daily_usage_hours,}
            input_appliances()
            # Function to calculate the monthly electricity cost
            def calculate_electricity_cost(appliances):
                total_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())*30 / 1000  # Convert total power to kWh or unit per month
                base_charge = 0
                total_cost_with_tax=0

                # Calculate the base charge based on usage
                if total_power <= 150:
                    base_charge = total_power * base_charge_rates["<= 150 units (kWh)"]
                elif total_power <= 400:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + (total_power - 150) * base_charge_rates["> 150 - <= 400 (kWh)"]
                else:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + 250 * base_charge_rates["> 150 - <= 400 (kWh)"] + (total_power - 400) * base_charge_rates["> 400 (kWh)"]
                    fuel_adjustable_charge = total_power * fuel_adjustable_charge_rate
                    total_cost_before_tax = base_charge + fuel_adjustable_charge + service_charge
                    total_cost_with_tax = total_cost_before_tax * (1 + tax_rate)
                    print("total__bill",total_cost_with_tax)
                return total_cost_with_tax
            # Calculate the monthly electricity cost
            monthly_cost = calculate_electricity_cost(appliances)

            def suggest_appliance_adjustments(appliances, target_bill):
                current_cost = calculate_electricity_cost(appliances)
                adjustments = {}
                if current_cost < target_bill:
                    adjustments["message"] = "You are currently under your target bill."
                else:
                    adjustments["message"] = "You are currently over your target bill."
                    remaining_cost = current_cost - target_bill

                    # Calculate the total daily power consumption
                    total_daily_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())

                    if total_daily_power == 0:
                        adjustments["message"] = "It is not possible to reach your target bill with the current appliances."
                    else:
                        # Calculate the maximum reduction possible to get to the target bill
                        max_possible_reduction_hours = remaining_cost / (total_daily_power / 1000)
                        for appliance_name, appliance_data in appliances.items():
                            # Reduce usage of each appliance by the same proportion
                            reduction_ratio = appliance_data["power_consumption"] * appliance_data["daily_usage_hours"] / total_daily_power
                            hours_to_reduce = min(max_possible_reduction_hours * reduction_ratio, appliance_data["daily_usage_hours"])
                            adjustments[appliance_name] = hours_to_reduce
                            
                return adjustments
            # Let users input the target monthly electricity bill
            target_bill = float(input("Enter your target monthly electricity bill amount: "))

            # Suggest adjustments to meet the target bill
            adjustments = suggest_appliance_adjustments(appliances, target_bill)
            # Display suggestions to meet the target bill
            print(adjustments["message"])
            print("\nSuggested Appliance Usage Adjustments:")
            for appliance, hours in adjustments.items():
                if appliance != "message":
                    print(f"Reduce usage of {appliance} by {hours:.2f} hours per day")
        

                 
            print("************************************************************")
            tax=(units*8.4)/100
            print("total tax",tax)
            payment=(100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300)*6
            print("bill:",payment)
            carbonem=payment+(units*8)/100
            print("************************************************************")
            print("carbon emmision tax:",carbonem)
            print("energy consuption is more ")
            print("************************************************************")
            fixedCharge=1000
            payment=payment+carbonem+tax
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    d=[]
    try:
        d.append(total)
        
        e=str(d[0])
        cursor=connection.cursor()
    except:
        print("unable to update")
    update_query="UPDATE electirc_bill SET current_month_bill =" + e +"WHERE bill_id='" + c +"'"
    #inserting the calculated data into the specific column
    cursor.execute(update_query)
    p="SELECT current_month_bill FROM electirc_bill where bill_id='ec2002'"
    cursor.execute(p)
    h=cursor.fetchall()
    val = h[0][0]    
    print("current amount:₹",val)
    #commit the changes and close the connection
    connection.commit()
    connection.close()
    
elif c=='ec2003':
    print("NAME:KIRAN SAHU")
    print("AGE:24")
    print("Meter Reader NO:4321678576")
    status = cursor.execute("select previous_month_status from electirc_bill where previous_month_status = 'unpaid'")
    if status == 'unpaid':
        print(f"select previous_month_amount from electirc_bill where bill_id = 'ec2003'")
    else:
        print(f"Previous Month's Bill: Paid with an amount of =₹{previous_month_amount[2]}")
        print("no due")
        units=float(input("enter the unit="))
        print("************************************************************")
        if units > 0 and units <= 100:
            tax=(units*1.4)/100
            print("total tax",tax)
            payment = units * 1.5+tax
            fixedCharge = 25 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    
        elif units > 100 and units <= 200:
            tax=(units*2.4)/100
            print("total tax=",tax)
            payment = (100 * 1.5) + (units - 100) * 2.5+tax
            fixedCharge = 50 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 200 and units <= 300:
            tax=(units*3.4)/100
            print("total tax",tax)
            payment =  (100 * 1.5) + (200 - 100) * 2.5 + (units - 200) * 4+tax
            fixedCharge = 75 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 300 and units <= 350:
            tax=(units*5.4)/100
            print("total tax",tax)
            payment = (100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300) * 5+tax   
            fixedCharge = 100 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units >350:
            appliances={}
            #Function to input appliance data
            def input_appliances():
                while True:
                    appliance_name = input("Enter the name of the appliance (or 'done' to finish): ")
                    if appliance_name.lower() == 'done':
                        break
                    power_consumption = float(input(f"Enter the power consumption of {appliance_name} (in watts): "))
                    daily_usage_hours = float(input(f"How many hours do you generally use {appliance_name} per day? "))
                    appliances[appliance_name] = {"power_consumption": power_consumption,"daily_usage_hours": daily_usage_hours,}
            input_appliances()
            # Function to calculate the monthly electricity cost
            def calculate_electricity_cost(appliances):
                total_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())*30 / 1000  # Convert total power to kWh or unit per month
                base_charge = 0
                total_cost_with_tax=0

                # Calculate the base charge based on usage
                if total_power <= 150:
                    base_charge = total_power * base_charge_rates["<= 150 units (kWh)"]
                elif total_power <= 400:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + (total_power - 150) * base_charge_rates["> 150 - <= 400 (kWh)"]
                else:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + 250 * base_charge_rates["> 150 - <= 400 (kWh)"] + (total_power - 400) * base_charge_rates["> 400 (kWh)"]
                    fuel_adjustable_charge = total_power * fuel_adjustable_charge_rate
                    total_cost_before_tax = base_charge + fuel_adjustable_charge + service_charge
                    total_cost_with_tax = total_cost_before_tax * (1 + tax_rate)
                    print("total__bill",total_cost_with_tax)
                return total_cost_with_tax
            # Calculate the monthly electricity cost
            monthly_cost = calculate_electricity_cost(appliances)

            def suggest_appliance_adjustments(appliances, target_bill):
                current_cost = calculate_electricity_cost(appliances)
                adjustments = {}
                if current_cost < target_bill:
                    adjustments["message"] = "You are currently under your target bill."
                else:
                    adjustments["message"] = "You are currently over your target bill."
                    remaining_cost = current_cost - target_bill

                    # Calculate the total daily power consumption
                    total_daily_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())

                    if total_daily_power == 0:
                        adjustments["message"] = "It is not possible to reach your target bill with the current appliances."
                    else:
                        # Calculate the maximum reduction possible to get to the target bill
                        max_possible_reduction_hours = remaining_cost / (total_daily_power / 1000)
                        for appliance_name, appliance_data in appliances.items():
                            # Reduce usage of each appliance by the same proportion
                            reduction_ratio = appliance_data["power_consumption"] * appliance_data["daily_usage_hours"] / total_daily_power
                            hours_to_reduce = min(max_possible_reduction_hours * reduction_ratio, appliance_data["daily_usage_hours"])
                            adjustments[appliance_name] = hours_to_reduce
                            
                return adjustments
            # Let users input the target monthly electricity bill
            target_bill = float(input("Enter your target monthly electricity bill amount: "))

            # Suggest adjustments to meet the target bill
            adjustments = suggest_appliance_adjustments(appliances, target_bill)
            # Display suggestions to meet the target bill
            print(adjustments["message"])
            print("\nSuggested Appliance Usage Adjustments:")
            for appliance, hours in adjustments.items():
                if appliance != "message":
                    print(f"Reduce usage of {appliance} by {hours:.2f} hours per day")


                 
            print("************************************************************")
            tax=(units*8.4)/100
            print("total tax",tax)
            payment=(100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300)*6
            print("bill:",payment)
            carbonem=payment+(units*8)/100
            print("************************************************************")
            print("carbon emmision tax:",carbonem)
            print("energy consuption is more ")
            print("************************************************************")
            fixedCharge=1000
            payment=payment+carbonem+tax
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    d=[]
    try:
        d.append(total)
        
        e=str(d[0])
        cursor=connection.cursor()
    except:
        print("unable to update")
    update_query="UPDATE electirc_bill SET current_month_bill =" + e +"WHERE bill_id='" + c +"'"
    #inserting the calculated data into the specific column
    cursor.execute(update_query)
    p="SELECT current_month_bill FROM electirc_bill where bill_id='ec2003'"
    cursor.execute(p)
    h=cursor.fetchall()
    val = h[0][0]    
    print("current amount:₹",val)
    #commit the changes and close the connection
    connection.commit()
    connection.close()
elif c=='ec2004':
    print("NAME:SUDHANSHU MUDLIE")
    print("AGE:24")
    print("Meter Reader NO:3425674329")
    if previous_month_status == "unpaid":
        print(f"Previous Month's Bill: Due with an amount of ₹{previous_month_amount}")
    else:
        print(f"Previous Month's Bill: Paid with an amount of =₹{previous_month_amount[2]}")
        print("no due")
        units=float(input("enter the unit="))
        print("************************************************************")
        if units > 0 and units <= 100:
            tax=(units*1.4)/100
            print("total tax",tax)
            payment = units * 1.5+tax
            fixedCharge = 25 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    
        elif units > 100 and units <= 200:
            tax=(units*2.4)/100
            print("total tax=",tax)
            payment = (100 * 1.5) + (units - 100) * 2.5+tax
            fixedCharge = 50 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 200 and units <= 300:
            tax=(units*3.4)/100
            print("total tax",tax)
            payment =  (100 * 1.5) + (200 - 100) * 2.5 + (units - 200) * 4+tax
            fixedCharge = 75 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units > 300 and units <= 350:
            tax=(units*5.4)/100
            print("total tax",tax)
            payment = (100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300) * 5+tax   
            fixedCharge = 100 # Extra charge
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
        elif units >350:
            appliances={}
            #Function to input appliance data
            def input_appliances():
                while True:
                    appliance_name = input("Enter the name of the appliance (or 'done' to finish): ")
                    if appliance_name.lower() == 'done':
                        break
                    power_consumption = float(input(f"Enter the power consumption of {appliance_name} (in watts): "))
                    daily_usage_hours = float(input(f"How many hours do you generally use {appliance_name} per day? "))
                    appliances[appliance_name] = {"power_consumption": power_consumption,"daily_usage_hours": daily_usage_hours,}
            input_appliances()
            # Function to calculate the monthly electricity cost
            def calculate_electricity_cost(appliances):
                total_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())*30 / 1000  # Convert total power to kWh or unit per month
                base_charge = 0
                total_cost_with_tax=0

                # Calculate the base charge based on usage
                if total_power <= 150:
                    base_charge = total_power * base_charge_rates["<= 150 units (kWh)"]
                elif total_power <= 400:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + (total_power - 150) * base_charge_rates["> 150 - <= 400 (kWh)"]
                else:
                    base_charge = 150 * base_charge_rates["<= 150 units (kWh)"] + 250 * base_charge_rates["> 150 - <= 400 (kWh)"] + (total_power - 400) * base_charge_rates["> 400 (kWh)"]
                    fuel_adjustable_charge = total_power * fuel_adjustable_charge_rate
                    total_cost_before_tax = base_charge + fuel_adjustable_charge + service_charge
                    total_cost_with_tax = total_cost_before_tax * (1 + tax_rate)
                    print("total__bill",total_cost_with_tax)
                return total_cost_with_tax
            # Calculate the monthly electricity cost
            monthly_cost = calculate_electricity_cost(appliances)

            def suggest_appliance_adjustments(appliances, target_bill):
                current_cost = calculate_electricity_cost(appliances)
                adjustments = {}
                if current_cost < target_bill:
                    adjustments["message"] = "You are currently under your target bill."
                else:
                    adjustments["message"] = "You are currently over your target bill."
                    remaining_cost = current_cost - target_bill

                    # Calculate the total daily power consumption
                    total_daily_power = sum(item["power_consumption"] * item["daily_usage_hours"] for item in appliances.values())

                    if total_daily_power == 0:
                        adjustments["message"] = "It is not possible to reach your target bill with the current appliances."
                    else:
                        # Calculate the maximum reduction possible to get to the target bill
                        max_possible_reduction_hours = remaining_cost / (total_daily_power / 1000)
                        for appliance_name, appliance_data in appliances.items():
                            # Reduce usage of each appliance by the same proportion
                            reduction_ratio = appliance_data["power_consumption"] * appliance_data["daily_usage_hours"] / total_daily_power
                            hours_to_reduce = min(max_possible_reduction_hours * reduction_ratio, appliance_data["daily_usage_hours"])
                            adjustments[appliance_name] = hours_to_reduce
                            
                return adjustments
            # Let users input the target monthly electricity bill
            target_bill = float(input("Enter your target monthly electricity bill amount: "))

            # Suggest adjustments to meet the target bill
            adjustments = suggest_appliance_adjustments(appliances, target_bill)
            # Display suggestions to meet the target bill
            print(adjustments["message"])
            print("\nSuggested Appliance Usage Adjustments:")
            for appliance, hours in adjustments.items():
                if appliance != "message":
                    print(f"Reduce usage of {appliance} by {hours:.2f} hours per day")


                 
            print("************************************************************")
            tax=(units*8.4)/100
            print("total tax",tax)
            payment=(100 * 1.5) + (200 - 100) * 2.5 + (300 - 200) * 4 + (units - 300)*6
            print("bill:",payment)
            carbonem=payment+(units*8)/100
            print("************************************************************")
            print("carbon emmision tax:",carbonem)
            print("energy consuption is more ")
            print("************************************************************")
            fixedCharge=1000
            payment=payment+carbonem+tax
            total = payment + fixedCharge
            print("total payment",payment)
            print("total bill",total)
    d=[]
    try:
        d.append(total)
        
        e=str(d[0])
        cursor=connection.cursor()
    except:
        print("unable to update")
    update_query="UPDATE electirc_bill SET current_month_bill =" + e +"WHERE bill_id='" + c +"'"
    #inserting the calculated data into the specific column
    cursor.execute(update_query)
    p="SELECT current_month_bill FROM electirc_bill where bill_id='ec2004'"
    cursor.execute(p)
    h=cursor.fetchall()
    val = h[0][0]    
    print("current amount:₹",val)
    #commit the changes and close the connection
    connection.commit()
    connection.close()
    
else:
    print("invaild bill id")
# Close the cursor and the database connection
cursor.close()
