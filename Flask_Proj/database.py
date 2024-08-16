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

def get_sql_data():
    sql = "SELECT * FROM information"
    mycursor = mydb.cursor()
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
    mycursor = mydb.cursor()

    if overwrite:
        mycursor.execute("DELETE FROM information")

    for i in range(len(data)):
        ID = i+1
        name = data[i]['name']
        price = float(data[i]['price'])
        sql = "INSERT INTO information (accID, name, price) VALUES (%s, %s, %s)"
        val = [ID, name, price]
        mycursor.execute(sql, val)

    if(push):
        mydb.commit() # To make changes

    #mycursor.execute("SELECT * FROM information")
    #myresult = mycursor.fetchall()
    #for x in myresult:
       # print(x)

def create_sql_template():
    sql = "SELECT * FROM information"

    mycursor = mydb.cursor()
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


