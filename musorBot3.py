import telebot
import requests
import time
import sys
import telegram
import urllib.request
import cv2
from time import sleep
import yadisk
import mysql.connector
from mysql.connector import errorcode

fromBotDir = 'images_from_bot'
toBotDir = 'images_to_bot'

botName = 'musorPanelBot'
botToken  = '5439017120:AAGLP-eskN9y1x5L8v8N7mszfCdhU4Tj784'
baseUrl = 'https://api.telegram.org/bot%s' % botToken
longPoolingTimeoutSec = 60
tokenYandexDisk = 'AQAAAAABNl3PAAhFnGhfpXK2WUPesOYsI7DFq4E'
sleepIntervalSec = 2
lastConsumedUpdateInit = 0

# Obtain connection string information from the portal
config = {
  'host':'localhost',
  'user':'root',
  'password':'oWeU0nRAwS',
  'database':'musor'
}


def detectionsDraw(image, detections):
    a=5
    #for (x, y, w, h) in detections:
    #    print("(({0}, {1}), ({2}, {3}))".format(x, y, x + w, y + h))
    #    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


def detectFace(inputImFile, outImFile):
    a=5
    #cascade = cv2.CascadeClassifier(cascadeFile)
    #image = cv2.imread(inputImFile)
    #if image is None:
    #    print("ERROR: Image did not load.")
    #    return (0, "ERROR: Image did not load.")
    #detections = cascadeDetect(cascade, image)
    #detectionsDraw(image, detections)
    #print("Found {0} objects!".format(len(detections)))
    #print("saving into {}".format(outImFile))
    #cv2.imwrite(outImFile, image)
    #detectMsg = ''
    #if len(detections) > 0:
    #    detectMsg = "Found {0} objects!".format(len(detections))
    #else:
    #    detectMsg = "None found"
    #return len(detections), detectMsg

def saveYandexDisk(updateId):
    y = yadisk.YaDisk(token=tokenYandexDisk)
    if y.check_token():
       newFilePath = fromBotDir + '/' + str(updateId) + '.jpeg'
       y.upload(newFilePath,'/Musor/'+str(updateId) + '.jpeg',overwrite=True)
    else:
      print("Error with yandex disk saving")

def saveToDB(localFilePath, chat_id, update_id):
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
    # Insert some data into table
    cursor.execute("INSERT INTO request (localFilePath, chat_id, update_id,  statusId)  VALUES (%s, %s, %s, 0);", (localFilePath, chat_id, update_id))
    print("Inserted",cursor.rowcount,"row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()

def botWorker(counter, lastConsumedUpdate):
    bot = telegram.Bot(token=botToken)
    # print bot.getMe()
    updates = bot.getUpdates(offset=lastConsumedUpdate + 1, timeout=longPoolingTimeoutSec)
    numOfUpdates = len(updates)
    numOfNewUpdates = 0 if (numOfUpdates < 1) else updates[-1].update_id - lastConsumedUpdate  # assumption of continuous counter of events
    if numOfNewUpdates == 0:
        print('{}. No new updates'.format(counter))
        return lastConsumedUpdate
    else:
        print('{}. There are {} new updates'.format(counter, numOfNewUpdates))
    for u in updates:
        updateId = u.update_id
        if updateId <= lastConsumedUpdate:
            break
        print('updateId={}, date={}'.format(u.update_id, u.message.date))
    for u in updates:
        updateId = u.update_id
        if updateId <= lastConsumedUpdate:
            continue
        print('updateId={}, date={}'.format(u.update_id, u.message.date))
        if u.message.photo:
            try:
              print('There are {} photos in this update'.format(len(u.message.photo)))
              biggestPhoto = u.message.photo[-1]
              biggestPhotoFileId = biggestPhoto.file_id
              print('biggestPhoto= {}x{}, fileId={}'.format(biggestPhoto.height, biggestPhoto.width, biggestPhoto.file_id))
              newFile = bot.getFile(biggestPhotoFileId)
              newFileUrl = newFile.file_path
              print(newFile)
              newFilePath = fromBotDir + '/' + str(updateId) + '.jpeg'  # build from updateId
              print(f'newFilePath={newFilePath}')
              photoFile = urllib.request.urlopen(newFileUrl)
              output = open(newFilePath, 'wb')
              output.write(photoFile.read())
              output.close()
              saveYandexDisk(updateId)
              #outImFile = toBotDir + '/' + str(updateId) + '_detected' + '.jpeg'
              #numFaces, detectMsg = detectFace(newFilePath, outImFile)
              chat_id = u.message.chat_id
              print('chat_id={}'.format(chat_id))
              saveToDB(newFilePath, chat_id, str(updateId))
              #print('outImFile={}'.format(outImFile))
              # bot.sendPhoto(chat_id, outImFile, caption='X faces detected')
              #message = bot.sendPhoto(photo=open(outImFile, 'rb'), caption=detectMsg, chat_id=chat_id)
            except:
              print("Some error!")
        lastConsumedUpdate = u.update_id
    print('Last consumed update: {}'.format(lastConsumedUpdate))
    return lastConsumedUpdate


def main(argv=None):
    print('Starting Telegram bot backend')
    lastConsumedUpdate = lastConsumedUpdateInit
    counter = 0
    while True:
        counter = counter + 1
        lastConsumedUpdate = botWorker(counter, lastConsumedUpdate)
        sleep(sleepIntervalSec)


if __name__ == '__main__':
    sys.exit(main())