import telebot
import requests
import time
from flask import Flask, render_template, request
from pathlib import Path
import mysql.connector
from mysql.connector import errorcode
import shutil
import os
import json


TOKEN  = '5439017120:AAGLP-eskN9y1x5L8v8N7mszfCdhU4Tj784'
URL = 'https://api.telegram.org/bot'
# Obtain connection string information from the portal
config = {
  'host':'localhost',
  'user':'root',
  'password':'oWeU0nRAwS',
  'database':'musor'
}


def send_message(chat_id, text):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

def run():
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

    
    sqlStr = "SELECT r.chat_id, a.answer, r.id FROM `request` r, `answers` a WHERE (a.requestId = r.id) AND (r.statusId=1) ORDER BY r.dateRequest ASC"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()

    # send answer to telegram bot
    #update status request
    for row in rows:
       time.sleep(2)
       send_message(row[0], row[1])
       cursor.execute("UPDATE  request SET statusId=2 where id ="+str(row[2]))
       conn.commit()
    
    
    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")

if __name__ == '__main__':
    run()