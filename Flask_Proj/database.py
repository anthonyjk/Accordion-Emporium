import mysql.connector
import json
import pandas as pd

# Reading json file
f = open('accordion.json')

data = json.load(f)

accordion_data = []

for line in data:
    if line not in accordion_data: # Removing repeats
        accordion_data.append(line)

f.close()

# Working with SQL Database
mydb = mysql.connector.connect(
    host="localhost",
    user="worker",
    password="pass",
    database = "accordions"
)

mycursor = mydb.cursor(buffered=True)

def get_sql_data(row_name = "accID"):
    global mycursor
    sql = f"SELECT * FROM information ORDER BY {row_name}"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult

def load_json(file):
    f = open(file)

    data = json.load(f)

    str_data = []

    for line in data:
        if line not in str_data: # Removing repeats
            str_data.append(line)

    f.close()

    return str_data

def update_database(data, overwrite, push = False):
    global mycursor

    if overwrite:
        mycursor.execute("DELETE FROM information")

    for i in range(len(data)):
        ID = i+1
        name = data[i]['name']
        price = float(data[i]['price'])
        sql = "INSERT INTO information (accID, name, price, preowned, brand, color, extra, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        name, preowned, brand, color, extra, a_type = alamo_vars(name)
        val = [ID, name, price, preowned, brand, color, extra, a_type]
        mycursor.execute(sql, val)

    if(push):
        mydb.commit() # To make changes

    #mycursor.execute("SELECT * FROM information")
    #myresult = mycursor.fetchall()
    #for x in myresult:
       # print(x)

def alamo_vars(name):
    preowned = False
    color = ""
    if "pre-owned" in name.lower() or "pre owned" in name.lower():
        preowned = True
        name = name[10:len(name) - 7]

    print(name)

    if " - " in name:
        name, color = name.split(" - ")
    elif ", " in name:
        name, color = name.split(", ")
    else:
        color = "Not Listed"
    brand = name.split(" ")[0]
    name = name[len(brand) + 1:]

    extra = " "
    if "w/" in color:
        color, extra = color.split(" w/ ")

    a_type = "Button"
    if "piano" in name.lower():
        a_type = "Piano"

    return [name, preowned, brand, color, extra, a_type]

def create_sql_template():
    global mycursor

    sql = "SELECT * FROM information"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    df = pd.DataFrame()
    for x in myresult:
        df2 = pd.DataFrame(list(x)).T
        df = pd.concat([df, df2])

    df.to_html('sql-data.html')

#accordion_data = load_json('accordion.json')

#update_database(accordion_data, push = False)

#create_sql_template()


