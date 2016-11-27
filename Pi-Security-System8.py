#PI-SECURITY BOX / Raspberry Pi Seucrity System 
#A program with a Terminal interface that allows you to set a raspberry pi running as a 
#standalone security system. When the PIR motion sensor is set off, an alarm can be played,
#an email will be sent remotely to the user, and photo recordings will be taken using the pi camera. 
#The user will be able to activate the security system remotely by sending an email to himself. The emailing
#functionality has not been fully completed yet.  

import datetime
import time
from time import sleep

import RPi.GPIO as io
import picamera

import feedparser		# imports feedparser to parse XML feed
import subprocess
import smtplib
import socket
import time
from email.mime.text import MIMEText
import datetime
import urllib2

import pyglet

user='human@email.com'		# replace dtclass15@gmail.com with your personal gmail user or email, or youruser@newschool.edu for your school account
passwd='**************'		# replace *** with your password for the above account

summaryAuthor = ""
summaryTitle = ""

pir_pin = 17

io.setmode(io.BCM)
camera = picamera.PiCamera()

currentTime = 0
#currentDate = datetime.date.today().strftime("%B %d, %Y")
currentDate = datetime.datetime.strftime(datetime.pdatetime.now(), '%Y-%m-%d %H:%M:%S')

io.setup(pir_pin, io.IN)         # activate input 

activatedMonitoring = False           #Has monitoring been turned on by the remote email switch?
motionDetected = False              #Has motion been detected by the PIR sensor?
remoteEmailSwitch = False           #Has the security system been activated by email?
soundOn = True                    #Turns alarm sounds on
cameraOn = False                   #Turns image / video recording on
intimidationOn = False             #Turns on the "Intimidation" setting of the program
firstTimeStartUp = True            #Is PI-Security starting a brand new session?

startTime = time.clock()

def activateMonitoring (remoteEmailSwitch, firstTimeStartUp, activatedMonitoring, soundOn):
    if (activatedMonitoring == True & firstTimeStartUp == True) :
            print("PI-Security system now active.")
            firstTimeStartUp = False
            if (soundOn == True):                                #If mute is not on then
                sound = pyglet.media.load('Alarm-Activation.mp3')   #play the activation sound 
                sound.play()                                        #when program is first run
                pyglet.app.run()

def startInterface() :           
    inputActivate = (raw_input('Would you like to activate PI-Security? (Yes / No) '))
    if (inputActivate == 'Yes'):
        activatedMonitoring = True
        activateMonitoring(remoteEmailSwitch, firstTimeStartUp, activatedMonitoring, soundOn)
    elif inputActivate == 'No':
        activatedMonitoring = False
        print('Thank you for trying PI-Security! ')
        exit()
    else: 
        print('Command not understood! ')
        startInterface()

inputSound = (raw_input('Would you like to turn the sound on? (Yes / No) '))
if (inputSound == 'Yes'):
    soundOn = True
    print('Sound is turned on! ')
    startInterface()
elif inputSound == 'No':
    soundOn = False
    print('Sound is turned off! ')
    startInterface()
else: 
    print('Command not understood! ')
    exit()

inputCamera = (raw_input('Would you like to turn photo / video recording on? (Yes / No) '))
if (inputCamera == 'Yes'):
    cameraOn = True
    print('Camera is turned on! ')
elif inputCamera == 'No':
    cameraOn = False
    print('Camera is turned off! ')
else: 
    print('Command not understood! ')
    startInterface()

def beginSecurity ():
        print("Movement has been detected!")
        alarmSound()
        startCamera()
        #sleep(5)
        resetSecurity()

def detectMotion (pir_pin): 
    if io.input(pir_pin):
        motionDetected = True
        if (motionDetected == True):
            #print('PIR')
            beginSecurity()

def alarmSound () :
        if (soundOn == False):
            print("Sending silent alarm! ")
        if (soundOn == True):
            print("Sounding alarm! ")
            sound = pyglet.media.load('Alarm.mp3')   #Sounds the alarm signal
            sound.play()                                        
            pyglet.app.run()

def startCamera () :
    if (cameraOn == True):
        print("Movement has been detected!")
        print("Camera is now recording.")
        camera.start_preview()
        camera.capture('Photo taken on ' + currentTime + ' PI-Secure.jpg ')
        sleep(1)
        camera.capture('Photo taken on ' + currentTime + ' PI-Secure.jpg ')
        sleep(2)
        camera.capture('Photo taken on ' + currentTime + ' PI-Secure.jpg ')
        sleep(3)

def resetSecurity (): 
    camera.capture('Photo taken on ' + currentTime + ' PI-Secure.jpg ')
    if (cameraOn == True):              #Has the camera been turned on? The filming contains slight delays
        sleep(3)                        #after each photo is taken, so the sleep delay with the camera on
    else if (cameraOn == False):        #doesn't have to be as long. There must be a sleep delay after
        sleep(6)                        #motion is detected to reduce noise from a less-than-reliable PIR sensor.
    motionDetected = False
    print("Resetting security.")
    camera.capture('Photo taken on ' + currentTime + ' PI-Secure.jpg ')
    camera.stop_preview()

while True:
    if (activatedMonitoring == True | remoteEmaiLSwitch == True):
        detectMotion(pir_pin)           #Pi is programmed to constantly check for motion detection
                                        #if security system is turned on. 

 def searchEmail(summary, title, remoteEmailSwitch, firstTimeStartUp): 
    if (remoteEmailSwitch == False):
 	  newmails = feedparser.parse("https://" + user + ":" + passwd + "@mail.google.com/gmail/feed/atom").entries
        for i in newmails:		#for loop itterates through newmails feed
            if str(i.author)=="NAME (EMAIL)": #replace this string with the author and email you are searching for
                if str(i.title)=="PI-Security: ON"
                    sendEmail(summaryAuthor, summaryTitle) #calls sendEmail function and passes author and summary into the message of the email document
                    remoteEmailSwitch = True
                    firstTimeStartUp = False
    if (remoteEmailSwitch == True & firstTimeStartUp == True):
      newmails = feedparser.parse("https://" + user + ":" + passwd + "@mail.google.com/gmail/feed/atom").entries
        for i in newmails:      #for loop itterates through newmails feed
            if str(i.author)=="NAME (EMAIL)": #replace this string with the author and email you are searching for
                if str(i.title)=="PI-Security: OFF"
                    sendEmail(summaryAuthor, summaryTitle) #calls sendEmail function and passes author and summary into the message of the email document
                    remoteEmailSwitch = False
                    firstTimeStartUp = True


 def sendEmail(str1, str2):
#     # Change to your own account information
#     to = ''
     gmail_user = ''
     gmail_password = ''
     smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
     smtpserver.ehlo()
     smtpserver.starttls()
     smtpserver.ehlo
     smtpserver.login(gmail_user, gmail_password)
     today = datetime.date.today()
     # Very Linux Specific
     arg='ip route list'
     p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
     data = p.communicate()
     split_data = data[0].split()
     ipaddr = split_data[split_data.index('src')+1]
     extipaddr = urllib2.urlopen("http://icanhazip.com").read()
     my_ip = 'Local address: %s\nExternal address: %s' %  (ipaddr, extipaddr)
     msg = MIMEText(my_ip)
     # fills subject of email with the strings which were taken from feedparser
     msg['Subject'] =  'You, ' +  str1 + ' ' + 'have turned ' + str2        #Sends an email stating that you, the user,
     msg['From'] = gmail_user                                               #has either turned PI-Securtiy ON / OFF. 
     msg['To'] = to
     time.sleep(5)
     smtpserver.sendmail(gmail_user, [to], msg.as_string())
     smtpserver.quit()
