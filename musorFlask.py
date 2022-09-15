# save this as app.py
from flask import Flask, render_template, request
from pathlib import Path
import mysql.connector
from mysql.connector import errorcode
import shutil
import os
import json


# Obtain connection string information from the portal
config = {
  'host':'localhost',
  'user':'root',
  'password':'oWeU0nRAwS',
  'database':'musor'
}

var_list = []

app = Flask(__name__)

@app.route("/")
def hello():
    # Construct connection string
    try:
      conn = mysql.connector.connect(**config)
      print("Connection established")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
         print("Something is wrong with the user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
         print("Database does not exist")
      else:
         print(err)
    else:
      cursor = conn.cursor()

    #take only one row
    sqlStr = "SELECT * FROM request WHERE statusId = 0 order by dateRequest asc LIMIT 1;"
    cursor.execute(sqlStr)

    rows = cursor.fetchall()
    id = 0
    localFilePath = ''
    filename = "musor.jpeg"

    for row in rows:
       id = row[0]
       localFilePath = row[1]
       
    if ((id!=0) and (localFilePath!='')):
       var_list.append(id)
       path = ""
       IMG_FOLDER = os.path.join('static', 'images')
       # Join various path components
       full_filename = os.path.join(IMG_FOLDER, filename)
       # Copy file.
       shutil.copy(localFilePath,full_filename)

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
    return render_template("/frontend/index.html", user_image = filename)

@app.route("/answer", methods=['POST'])
def answerFun():
    # Construct connection string
    # phrase = request.form['phrase']
    # get id record
    requestId = var_list.pop()
    print("requestId="+str(requestId))
    phrase = request.json
    answer = ""
    for y in phrase:
        answer = answer + y["description"]+","
    print(answer)

      # Construct connection string
    try:
      conn = mysql.connector.connect(**config)
      print("Connection established")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
         print("Something is wrong with the user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
         print("Database does not exist")
      else:
         print(err)
    else:
      cursor = conn.cursor()

    #insert into table
    cursor.execute("INSERT INTO answers (requestId, answer) VALUES (%s, %s);", (requestId, answer))
    conn.commit()
    cursor.execute("UPDATE  request SET statusId=1 where id ="+str(requestId))
    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Inserted.")
    return phrase



if __name__ == '__main__':
    app.debug = True
    app.run(host="93.95.97.136")
