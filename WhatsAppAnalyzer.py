import os
from functools import partial
import time
import shutil
import sqlite3
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

import pandas as pd
import datetime
import dlib
import face_recognition
from threading import Thread, Event
import threading
#import boto3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from PIL import ImageTk, Image

print("")
print("***** INITIALIZING PROGRAM - Android WhatsApp Analyzer *****")
print("")
Avatar = "Avatar"
DCIMpic = "DCIM"

cwdirec = os.getcwd() +"\\"+Avatar
for filez in os.listdir(cwdirec):
    cwd_img = cwdirec+"/"+filez
    imgur = Image.open(cwd_img)
    imgur = imgur.resize((125, 125))
    imgur.save(cwd_img)

cwdirec = os.getcwd()

class whatsappArtifacts:
    id = ""
    contactNumber = ""
    fromMe = False
    data = ""
    timestamp = 0
    recieveTimestamp = 0
    mediaURL = ""
    mediaType = ""
    mediaSize = None
    mediaName = ""
    next = None

    def __init__(self, id, contactNumber, fromMe, data, timestamp, rcvTimestamp, mediaURL, mediaType, mediaSize,
                 mediaName):
        self.id = id
        self.contactNumber = contactNumber
        self.fromMe = fromMe
        self.data = data
        self.timestamp = timestamp
        self.recieveTimestamp = rcvTimestamp
        self.mediaURL = mediaURL
        self.mediaType = mediaType
        self.mediaSize = mediaSize
        self.mediaName = mediaName

class susImage:
    def __init__(self, frame, path, Tkinter):
        self.path = path
        self.frame = frame
        self.image2 = Tkinter.PhotoImage(file='%s' %path)
        self.label = Label(self.frame, image=self.image2)
        self.image = self.image2
        self.image.pack()

class WSsinglyLinkedList:
    head = None
    last = None

    def __init__(self, whatsappArtifacts):
        self.head = whatsappArtifacts
        self.last = whatsappArtifacts

    def addItem(self, whatsappArtifacts):
        self.last.next = whatsappArtifacts
        self.last = whatsappArtifacts

    def delItem(self, whatsappArtifacts):
        pntr = self.head
        while pntr != None:
            if pntr.next == whatsappArtifacts:
                pntr.next = whatsappArtifacts.next
                break
            else:
                pntr = pntr.next

class SimilarImageObj:
    name = None
    next = None

    def __init__(self, name):
        self.name = name


class PICsinglyLinkedList:
    head = None
    last = None

    def __init__(self, SimilarImageObj):
        self.head = SimilarImageObj
        self.last = SimilarImageObj

    def addItem(self, SimilarImageObj):
        self.last.next = SimilarImageObj
        self.last = SimilarImageObj

    def delItem(self, SimilarImageObj):
        pntr = self.head
        while pntr != None:
            if pntr.next == SimilarImageObj:
                pntr.next = SimilarImageObj.next
                break
            else:
                pntr = pntr.next

def loadDatabases(contactDBPath, WSDBPath):
    ContactConnection = sqlite3.connect(contactDBPath)
    contactdf = pd.read_sql_query("select number from calls;", ContactConnection)

    WhatsappDBConnection = sqlite3.connect(WSDBPath)
    WSdf = pd.read_sql_query("select * from messages;", WhatsappDBConnection)

    return contactdf, WSdf

def countCallFrequency(contactsDB):
    df = contactsDB
    # Initilising the dictionary with all contact details
    numberCount = {}  # Stores all contact details within the call log and their call frequencies
    for x in range(df.shape[0]):
        if df.loc[x, 'number'][:3] == "+65":
            if df.loc[x, 'number'][3] == "6":
                continue
            else:
                numberCount[df.loc[x, 'number'][3:]] = 0
        else:
            if df.loc[x, 'number'][0] == "6":
                continue
            else:
                numberCount[df.loc[x, 'number']] = 0

    # Calculating number of calls for each contact
    for x in range(df.shape[0]):

        if df.loc[x, 'number'][:3] == "+65":
            if df.loc[x, 'number'][3] == "6":
                continue
            else:
                value = numberCount[df.loc[x, 'number'][3:]]
                numberCount[df.loc[x, 'number'][3:]] = value + 1

        else:
            if df.loc[x, 'number'][0] == "6":
                continue
            else:
                value = numberCount[df.loc[x, 'number']]
                numberCount[df.loc[x, 'number']] = value + 1
                # print(df.loc[x, 'number'])
                # print(numberCount[df.loc[x, 'number']])

    sortedCallsFreq = sorted(numberCount.items(), key=lambda item: item[1], reverse=True)
    top5CalledNumber = []  # Stores the top 5 called number in the call log.

    for x in range(5):
        top5CalledNumber.append(sortedCallsFreq[x][0])
    return top5CalledNumber

def loadKeyword(filename):
    keywords = []
    file = open(filename, "r")
    for word in file:
        if '\n' in word:
            word = word[:-1]
        keywords.append(word)
    return keywords

def findWSArtifact(whatsappDB, top5CalledNumber, incriminatingWhatsappText, keywords):
    df = whatsappDB
    for x in range(len(top5CalledNumber)):
        incriminatingWhatsappText[top5CalledNumber[x]] = None

    for x in range(df.shape[0]):
        if df.loc[x, "key_remote_jid"][2:10] in top5CalledNumber and df.loc[x, "data"] != None:
            for i in range(len(keywords)):
                if keywords[i] in df.loc[x, "data"]:
                    # print(df.loc[x, "key_remote_jid"][2:10] + ": " + df.loc[x, "data"])
                    incoming = False
                    # print(df.loc[x, "key_from_me"])
                    if df.loc[x, "key_from_me"] == 0:
                        incoming = True

                    timestamp = str(df.loc[x, "timestamp"])
                    actualDateTime = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
                    # print(actualDateTime.strftime("%d-%m-%Y %H:%M:%S"))

                    recvtimestamp = str(df.loc[x, "received_timestamp"])
                    actualRecvDateTime = datetime.datetime.fromtimestamp(int(recvtimestamp) / 1000)
                    # print("recv: " + actualRecvDateTime.strftime("%d-%m-%Y %H:%M:%S"))

                    WsArtifact = whatsappArtifacts(df.loc[x, "_id"], df.loc[x, "key_remote_jid"][2:10], incoming,
                                                   df.loc[x, "data"], actualDateTime.strftime("%d-%m-%Y %H:%M:%S"),
                                                   actualRecvDateTime.strftime("%d-%m-%Y %H:%M:%S"),
                                                   df.loc[x, "media_url"],
                                                   df.loc[x, "media_mime_type"], df.loc[x, "media_size"],
                                                   df.loc[x, "media_name"])
                    # print(".timestamp: " + WsArtifact.timestamp)
                    # print(".data: " + WsArtifact.data)
                    # print(WsArtifact.fromMe)

                    if incriminatingWhatsappText[df.loc[x, "key_remote_jid"][2:10]] is None:
                        listOfWSEvidence = WSsinglyLinkedList(WsArtifact)
                        incriminatingWhatsappText[str(df.loc[x, "key_remote_jid"][2:10])] = listOfWSEvidence
                        # print(incriminatingWhatsappText[str(df.loc[x, "key_remote_jid"][2:10])].last.data)


                    else:
                        listOfWSEvidence = incriminatingWhatsappText[str(df.loc[x, "key_remote_jid"][2:10])]
                        listOfWSEvidence.addItem(WsArtifact)
                        # print(incriminatingWhatsappText[str(df.loc[x, "key_remote_jid"][2:10])].last.data)

def faceRecognition(displayPicPath, picLibraryPath, top5CalledNumber, listOfDP, listOfDPPath, SimilarPic,
                    numberToCheck):
    print("--- Initializing Facial Recognition ---")
    number = numberToCheck
    whatsappDisplayPic = listOfDP
    whatsappDisplayPicPath = listOfDPPath
    # print("length of whatsappDisplayPicPath:" + str(len(whatsappDisplayPicPath)))

    # print(displayPicPath)
    for root, dirs, files in os.walk(displayPicPath):
        for file in files:
            if number in file:
                # print("In: " + number)
                image = face_recognition.load_image_file(displayPicPath + "\\" + file)
                if len(face_recognition.face_encodings(image)) > 0:
                    imageEncoded = face_recognition.face_encodings(image)[0]
                    whatsappDisplayPic.append(imageEncoded)
                    whatsappDisplayPicPath.append(str(file))
                    break
                else:
                    whatsappDisplayPic.append(str(file))
                    whatsappDisplayPicPath.append(str(file))
                    break
            elif file == "me.jpg":
                whatsappDisplayPic.append("No display picture")
                whatsappDisplayPicPath.append("None")
            else:
                continue
    # print(len(whatsappDisplayPic))


    for i in range(len(top5CalledNumber)):
        if top5CalledNumber[i] == numberToCheck:
            if whatsappDisplayPic[i] != "No display picture":
                imageObj = SimilarImageObj(whatsappDisplayPicPath[i])
                linkedList = PICsinglyLinkedList(imageObj)
                SimilarPic[str(top5CalledNumber[i])] = linkedList
                # SimilarPic["93212616"]
            else:
                SimilarPic[str(top5CalledNumber[i])] = "None"
                # print(SimilarPic[str(top5CalledNumber[i])])

    for i in range(len(top5CalledNumber)):
        if top5CalledNumber[i] == numberToCheck:
            # print(top5CalledNumber[i])
            if type(whatsappDisplayPic[i]) is not str and whatsappDisplayPic[i] is not "None":
                for root, dirs, files in os.walk(picLibraryPath):
                    for file in files:
                        ext = file.split(".")[-1]
                        if ext != "jpg":
                            continue
                        print("Matching: " + file)
                        image = face_recognition.load_image_file(picLibraryPath + "\\" + file)

                        if len(face_recognition.face_encodings(image)) > 0:
                            imageEncoded = face_recognition.face_encodings(image)[0]
                            results = face_recognition.compare_faces([whatsappDisplayPic[i]], imageEncoded)
                            # print(results)
                            if results[0]:
                                imageObj = SimilarImageObj(file)
                                linkedList = SimilarPic[str(top5CalledNumber[i])]
                                linkedList.addItem(imageObj)
                                SimilarPic[str(top5CalledNumber[i])] = linkedList
                                relpath1 = "sus" + str(i + 1) + "\\" + file
                                abspath1 = os.path.abspath(relpath1)
                                relpath2 = "DCIM\\" + file
                                abspath2 = os.path.abspath(relpath2)
                                command = "copy " + str(abspath2) + " " + str(abspath1)
                                fullcommand = "cmd /c " + command
                                # print(fullcommand)
                                os.system(fullcommand)
                            # print(results[0])
                        else:
                            # print("Not human picture")
                            continue
            else:
                print("No Images Found - Skipped")
                continue
    return whatsappDisplayPic, whatsappDisplayPicPath, SimilarPic

def reportGenerator(contactNum, keywords):
    print("--- Initiating Report Generation ---")
    env = Environment(loader=FileSystemLoader('.'))
    # A HTML file has to be created to be used as a template.
    # In this case, I used "report.html" in the same directory as this py file
    template = env.get_template("report.html")

    messages = []
    messagesLinkedList = incriminatingWhatsappText[contactNum]
    if messagesLinkedList is None:
        messages.append("No Keywords detected in WhatsApp Conversation")
    else:
        currentNum = messagesLinkedList.head
        lastNum = messagesLinkedList.last

        while currentNum.id != lastNum.id:
            messages.append(currentNum.timestamp + "<br>")
            if (currentNum.fromMe == 1):
                messages.append("From: " + currentNum.contactNumber)
                messages.append("<br>To: -Self-")
            else:
                messages.append("From: -Self-")
                messages.append("<br>To: " + currentNum.contactNumber)
                messages.append("<br>")
                messages.append(currentNum.data)
                messages.append("<br><br>")
            currentNum = currentNum.next

    messages = str(messages)[1:-1]
    messages = messages.replace("'", "")
    messages = messages.replace('"', "")
    messages = messages.replace(",", "")
    if messages == " " or messages == "":
        messages = "No Keywords detected in WhatsApp Conversation"
    # print(messages)
    # print("TEST: " + contactNum)
    template_segments = {
                        "title": "Mobile Phone Analysis Report: ",
                        "num": contactNum,
                        "keywords": keywords,
                        "messageData1": messages
                        }

    html_out = template.render(template_segments)

    cwd = os.getcwd()
            # Generated PDF will appear in the "Reports" Folder
            # Generated PDF name will be assigned here
    report_name = "Mobile Phone Analysis Report - " + contactNum
    file_ext = ".pdf"
    file_path = Path(cwd + '/Reports/' + report_name + file_ext)

    i = 1
    while file_path.is_file():
        file_path = Path(cwd + '/Reports/' + report_name + '(' + str(i) + ')' + file_ext)
        i = i + 1

    HTML(string=html_out).write_pdf(file_path)


# def rekognition(sourceFile, targetFile):
#     client = boto3.client('rekognition')
#
#     imageSource = open(sourceFile, 'rb')
#     imageTarget = open(targetFile, 'rb')
#
#     response = client.compare_faces(SimilarityThreshold=80,
#                                     SourceImage={'Bytes': imageSource.read()},
#                                     TargetImage={'Bytes': imageTarget.read()})
#
#     for faceMatch in response['FaceMatches']:
#         position = faceMatch['Face']['BoundingBox']
#         similarity = str(faceMatch['Similarity'])
#         print('The face at ' +
#               str(position['Left']) + ' ' +
#               str(position['Top']) +
#               ' matches with ' + similarity + '% confidence')

    # imageSource.close()
    # imageTarget.close()
    # return len(response['FaceMatches'])

# FUNCTIONS AVAILABLE:
# 1. loadDatabases (Pass in all 3 absolute path to the database file. MUST be in contacts2.db > msgstore.db > mmssms.db order)
# 2. countCallFrequency (Pass in the pandas data frame for contacts2.db which is the 1 returned value from loadDatabases().)
# 3. loadKeyword (Pass in the absolute path for the text file for the keywords.)
# 4. findWSArtifact (Pass in the dataframe for msgstore.db which is the 2nd return value of loadDatabases(),
#                    pass in the output of countCallFrequency(),
#                    pass in an empty python dictionary called "incriminatingWhatsappText",
#                    pass in the output of loadKeyword()
# 5. os.system() (Pass in the absolute path to where the Avatar file is located)
# 6. faceRecognition (Pass in the absolute path to where the Avatar file is located,
#                     pass in the absolute path to where the image library is located,
#                     pass in the the output of countCallFrequency(),
#                     pass in an empty python list called "whatsappDisplayPic",
#                     pass in an empty python list called "whatsappDisplayPicPath",
#                     pass in an empty python dictionary called "SuspectPic",
#                     pass in the mobile number you wish to search that is among the top 5 called numbers. Must be a string.)
#                       e.g. 93212616

# OUTPUT TO HANDLE:
# 1. top5CalledNumber:
#                               Display each number as one page.
# 2. incriminatingWhatsappText:
#                               Display all the texts(.data of the object in the linked list) and their time sent(.timestamp of object in the linked list).
#                               Data is a singly linked list called WSSinglyLinkedList defined above.
# 3. SuspectPic:
#                Display all image (.name of the object in the linked list, is the absolute path to image).
#                REMEMBER check according whatsappDisplayPic list.
#                If value for whatsappDisplayPic[index] is "No display picture" display a stickman
#                If value for whatsappDisplayPic[index] is a string like "xxxxxxx@s.whatsapp.jpg" go to whatsappDisplayPicPath[index] get the absolute path of the image.
#                If value for whatsappDisplayPic[index] is an array like [[xxx, xxx, xxx....xxx]] go to SuspectPic[Mobile number] to get the singly linked list.
#                Data is a singly linked list called PICSinglyLinkedList defined above.

contactdf, WSdf = loadDatabases("contacts2.db", "msgstore.db")

top5CalledNumber = countCallFrequency(contactdf)
# print("top 5 called number: ")
# print(top5CalledNumber)

keywords = loadKeyword("Keywords.txt")  # List of keywords read in from a text file "keywords.txt"
print("Loaded Keywords:")
print(keywords)

incriminatingWhatsappText = {}  # Dictionary for containing linked list of text messages containing keywords.
findWSArtifact(WSdf, top5CalledNumber, incriminatingWhatsappText, keywords)
# print(incriminatingWhatsappText["97360019"].head.data)
# print(incriminatingWhatsappText["97360019"].head.timestamp)
# print(incriminatingWhatsappText["97360019"].last.data)
# print(incriminatingWhatsappText["97360019"].last.timestamp)

# os.system('cmd /c "photoviewer ./photo.jpg" ')
command = " cd /d " + Avatar + " & ren *.j *.jpg"
fullcommand = "cmd /c" + command
# print(fullcommand)
os.system(fullcommand)
os.system('cmd /c "cd /d sus1 & del /Q *.*"')
os.system('cmd /c "cd /d sus2 & del /Q *.*"')
os.system('cmd /c "cd /d sus3 & del /Q *.*"')
os.system('cmd /c "cd /d sus4 & del /Q *.*"')
os.system('cmd /c "cd /d sus5 & del /Q *.*"')

# test = rekognition("kaizhi.jpg", "family.jpg")
# if test > 0:
#     print("match")

whatsappDisplayPic = []  # Stores the raw binary of the encoded display picture
whatsappDisplayPicPath = []  # Stores the full absolute path name to the display picture
SuspectPic = {}

for i in range(len(top5CalledNumber)):
    print("running: " + top5CalledNumber[i])
    whatsappDisplayPic, whatsappDisplayPicPath, SuspectPic = faceRecognition(
        Avatar,
        DCIMpic, top5CalledNumber,
        whatsappDisplayPic, whatsappDisplayPicPath, SuspectPic, top5CalledNumber[i])

# print("Finish")
# loadingGUI.destroy()
# def UploadFolder(event=None):
#     Folder1 = None
#     Folder1 = filedialog.askopenfilename()
#
#     if Folder1 != "":
#         current_directory = os.getcwd()
#         print(Folder1)
#         print(current_directory)
#         #cmd = 'copy "-{0} -{1}"'.format(Folder1, current_directory)
#         #cmd = 'copy C:\\Users\\jiaxuan7\\Desktop\\Timetable.jpg C:'
#         #os.system('copy "-{0} -{1}"'.format(Folder1, current_directory))
#         print(Folder1, ' Uploaded')
#     else:
#         print('You have selected nothing')

def openimage(imagepath, susNumb):
    print("--- Opening Image ---")
    if imagepath != None:
        path = imagepath[0][len(DCIMpic):]
        path = susNumb + path
        print(path)
        imageabsolutepath = os.path.abspath(path)
        os.system('cmd /c "%SystemRoot%\\System32\\rundll32.exe "%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen ' + imageabsolutepath + '" ')

def GUIdata(sus_number):
    singlylinkedlisty = incriminatingWhatsappText[sus_number]
    if singlylinkedlisty == None:
        return ["No Whatsapp messages"]
    currentnode = singlylinkedlisty.head
    data = []
    time = []
    number = []
    fromMe = []
    datarow = []

    while currentnode != None:
        time.append(currentnode.timestamp)
        data.append(currentnode.data)
        if currentnode.fromMe:
            fromMe.append('From:')
            number.append('Myself')
        else:
            fromMe.append("To:")
            number.append(currentnode.contactNumber)
        currentnode = currentnode.next

    for i in range(len(data)):
        datarow.append(time[i]+" "+data[i]+" "+fromMe[i]+" "+number[i])

    return datarow

def GUIimg(sus_number, top5CalledNumber, path):
    index = 0
    suspect_picture = []
    for i in range(len(top5CalledNumber)):
        if top5CalledNumber[i] == sus_number:
            index = i
            break
        else:
            continue
    if type(whatsappDisplayPic[index]) == str:
        return None
    else:
        singlylinkedlisty = SuspectPic[sus_number]
        currentnode = singlylinkedlisty.head
        currentnode = currentnode.next

        while currentnode != None:
            # print("test")
            # print(currentnode.name)
            suspect_picture.append(path + "/" + currentnode.name)
            currentnode = currentnode.next

    return suspect_picture

        # data_lister = Listbox(img_canvas, yscrollcommand=scrollbar_middle.set, width=100)
        # for line in GUIdata(top5CalledNumber[0]):
        #     data_lister.insert(END, line)
        # data_lister.pack(side=LEFT, fill=BOTH)

        # get linkedist from suspectPic[sus_number]
        # transverse linkedlist get object
        # object.name is absolute path to the image

def imageMaker(frame, imagePath):
    ttk.Label(frame, text='Image matched: %s' % imagePath).pack()
    # my_img_path = PhotoImage(file="%s" % pictures[0])
    # my_img = ImageTk.PhotoImage(file=my_img_path)
    # ttk.Label(frame, image = my_img)

def photoAdder(frame, sus_number, sus_list, path):
    list_sus_pic = GUIimg(sus_number, sus_list, path)
    if list_sus_pic == None:
        ttk.Label(frame, text="NO IMAGES MATCHED").pack()
    else:
        for x in list_sus_pic:
            imageMaker(frame, x)

    #     imagelel = Image.open("%s" % picture1[0])
    #     #imagelel = imagelel.resize((100, 100))
    #     imager = ImageTk.PhotoImage(imagelel)

# print(GUIimg(top5CalledNumber[0], top5CalledNumber, DCIMpic))
# print(GUIimg(top5CalledNumber[3], top5CalledNumber, DCIMpic))

# print(top5CalledNumber)
# print(whatsappDisplayPicPath)

root = tk.Tk()

root.title('WhatsApp Analyzer Tool')
# configuring the size of the window
root.geometry('700x500')

#create tab control
TAB_CONTROL = ttk.Notebook(master=root)

if len(top5CalledNumber) > 0:
    #Tab 1
    TAB1 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB1, text='Suspect 1')

    canvas_tab1 = tk.Canvas(TAB1)
    canvas_tab1.pack()

    top_frame = tk.Frame(TAB1, bg="#57AEC5", bd=5)
    top_frame.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

    number_label_tab1 = Label(top_frame, text=top5CalledNumber[0], font=('Times New Roman', 15))
    number_label_tab1.place(relx=0.08, rely=0.025, anchor='n')

    data_frame = tk.Frame(top_frame, bd=1)
    data_frame.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')
    scrollbar_top = Scrollbar(data_frame, orient='vertical')
    scrollbar_top.pack(side=RIGHT, fill=Y)
    scrollbar_top_x = Scrollbar(data_frame, orient='horizontal')
    scrollbar_top_x.pack(side=BOTTOM, fill=X)

    photoAdder(data_frame, top5CalledNumber[0], top5CalledNumber, DCIMpic)

    displaypic1 = whatsappDisplayPicPath[0]
    if displaypic1 != 'None':
        displaypic1 = Avatar+"/"+displaypic1
        my_img = ImageTk.PhotoImage(Image.open('%s' % displaypic1))
    else:
        my_img = ImageTk.PhotoImage(Image.open('unknown_man.png'))
    my_label = Label(top_frame, image=my_img)
    my_label.place(relx=0.71, relwidth=0.29, relheight=1)

    middle_frame = tk.Frame(TAB1, bg="#57AEC5", bd=10)
    middle_frame.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

    img_canvas = tk.Canvas(middle_frame, bd=1)
    img_canvas.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

    scrollbar_middle = Scrollbar(img_canvas, orient='vertical', command=img_canvas.yview)
    scrollbar_middle.pack(side=RIGHT, fill=Y)
    scrollbar_middle_x = Scrollbar(img_canvas, orient='horizontal', command=img_canvas.xview)
    scrollbar_middle_x.pack(side=BOTTOM, fill=X)

    data_list = Listbox(img_canvas, width=100)
    for line in GUIdata(top5CalledNumber[0]):
        data_list.insert(END, line)
    data_list.pack(side=LEFT, fill=BOTH)

    scrollbar_middle_x.config(command=data_list.xview)
    scrollbar_middle.config(command=data_list.yview)

    bottom_frame = tk.Frame(TAB1, bg="#57AEC5", bd=10)
    bottom_frame.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

    upload_button = tk.Button(bottom_frame, text="View Image", font=('Modern', 18), command=lambda: openimage(GUIimg(top5CalledNumber[0], top5CalledNumber, DCIMpic), "sus1"))
    upload_button.place(relwidth=0.3, relheight=1)

    save_button = tk.Button(bottom_frame, text="Export", font=('Modern', 18), command=lambda: reportGenerator(top5CalledNumber[0], keywords))
    save_button.place(relx=0.7, relwidth=0.3, relheight=1)

    canvas_tab1.pack(side="left", fill='both', expand=True)

    #END OF TAB 1

if len(top5CalledNumber) > 1:
    #Tab 2
    TAB2 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB2, text='Suspect 2')

    canvas_tab2 = tk.Canvas(TAB2)
    canvas_tab2.pack()

    top_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=5)
    top_frame_2.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

    number_label_tab2 = Label(top_frame_2, text=top5CalledNumber[1], font=('Times New Roman', 15))
    number_label_tab2.place(relx=0.08, rely=0.025, anchor='n')

    data_frame_2 = tk.Frame(top_frame_2, bd=1)
    data_frame_2.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

    scrollbar_top_2 = Scrollbar(data_frame_2, orient='vertical')
    scrollbar_top_2.pack(side=RIGHT, fill=Y)
    scrollbar_top_2_x = Scrollbar(data_frame_2, orient='horizontal')
    scrollbar_top_2_x.pack(side=BOTTOM, fill=X)

    photoAdder(data_frame_2, top5CalledNumber[1], top5CalledNumber, DCIMpic)

    displaypic2 = whatsappDisplayPicPath[1]
    if displaypic2 != 'None':
        displaypic2 = Avatar+"/"+displaypic2
        my_img_2 = ImageTk.PhotoImage(Image.open('%s' % displaypic2))
    else:
        my_img_2 = ImageTk.PhotoImage(Image.open('unknown_man.png'))
    my_label_2 = Label(top_frame_2, image=my_img_2)
    my_label_2.place(relx=0.71, relwidth=0.29, relheight=1)

    middle_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=10)
    middle_frame_2.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

    img_canvas_2 = tk.Canvas(middle_frame_2, bd=1)
    img_canvas_2.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

    scrollbar_middle_2 = Scrollbar(img_canvas_2, orient='vertical', command=img_canvas_2.yview)
    scrollbar_middle_2.pack(side=RIGHT, fill=Y)
    scrollbar_middle_2_x = Scrollbar(img_canvas_2, orient='horizontal', command=img_canvas_2.xview)
    scrollbar_middle_2_x.pack(side=BOTTOM, fill=X)

    data_list_2 = Listbox(img_canvas_2, yscrollcommand=scrollbar_top_2.set, width=100)
    for line in GUIdata(top5CalledNumber[1]):
        data_list_2.insert(END, line)
    data_list_2.pack(side=LEFT, fill=BOTH)

    bottom_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=10)
    bottom_frame_2.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

    upload_button_2 = tk.Button(bottom_frame_2, text="View Image", font=('Modern', 18), command=lambda: openimage(GUIimg(top5CalledNumber[1], top5CalledNumber, DCIMpic), "sus2"))
    upload_button_2.place(relwidth=0.3, relheight=1)

    save_button_2 = tk.Button(bottom_frame_2, text="Export", font=('Modern', 18), command=lambda: reportGenerator(top5CalledNumber[1], keywords))
    save_button_2.place(relx=0.7, relwidth=0.3, relheight=1)

    canvas_tab2.pack(side="left", fill='both', expand=True)
    #code for Tab 2 output

if len(top5CalledNumber) > 2:
    #Tab 3
    TAB3 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB3, text='Suspect 3')

    canvas_tab3 = tk.Canvas(TAB3)
    canvas_tab3.pack()

    #code for Tab 3 output
    top_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=5)
    top_frame_3.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

    number_label_tab3 = Label(top_frame_3, text=top5CalledNumber[2], font=('Times New Roman', 15))
    number_label_tab3.place(relx=0.08, rely=0.025, anchor='n')

    data_frame_3 = tk.Frame(top_frame_3, bd=1)
    data_frame_3.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

    scrollbar_top_3 = Scrollbar(data_frame_3, orient='vertical')
    scrollbar_top_3.pack(side=RIGHT, fill=Y)
    scrollbar_top_x_3 = Scrollbar(data_frame_3, orient='horizontal')
    scrollbar_top_x_3.pack(side=BOTTOM, fill=X)

    photoAdder(data_frame_3, top5CalledNumber[2], top5CalledNumber, DCIMpic)

    displaypic3 = whatsappDisplayPicPath[2]
    if displaypic3 != 'None':
        displaypic3 = Avatar+"/"+displaypic3
        my_img_3 = ImageTk.PhotoImage(Image.open('%s' % displaypic3))
    else:
        my_img_3 = ImageTk.PhotoImage(Image.open('unknown_man.png'))
    my_label_3 = Label(top_frame_3, image=my_img_3)
    my_label_3.place(relx=0.71, relwidth=0.29, relheight=1)

    middle_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=10)
    middle_frame_3.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

    img_canvas_3 = tk.Canvas(middle_frame_3, bd=1)
    img_canvas_3.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

    scrollbar_middle_3 = Scrollbar(img_canvas_3, orient='vertical', command=img_canvas_3.yview)
    scrollbar_middle_3.pack(side=RIGHT, fill=Y)
    scrollbar_middle_3_x = Scrollbar(img_canvas_3, orient='horizontal' ,command=img_canvas_3.xview)
    scrollbar_middle_3_x.pack(side=BOTTOM, fill=X)

    data_list_3 = Listbox(img_canvas_3, width=100)
    for line in GUIdata(top5CalledNumber[2]):
        data_list_3.insert(END, line)
    data_list_3.pack(side=LEFT, fill=BOTH)

    bottom_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=10)
    bottom_frame_3.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

    upload_button_3 = tk.Button(bottom_frame_3, text="View Image", font=('Modern', 18), command=lambda: openimage(GUIimg(top5CalledNumber[2], top5CalledNumber, DCIMpic), "sus3"))
    upload_button_3.place(relwidth=0.3, relheight=1)

    save_button_3 = tk.Button(bottom_frame_3, text="Export", font=('Modern', 18), command=lambda: reportGenerator(top5CalledNumber[2], keywords))
    save_button_3.place(relx=0.7, relwidth=0.3, relheight=1)

    canvas_tab3.pack(side="left", fill='both', expand=True)

if len(top5CalledNumber) > 3:
    #Tab 4
    TAB4 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB4, text='Suspect 4')

    #code for Tab 4 output
    canvas_tab4 = tk.Canvas(TAB4)
    canvas_tab4.pack()

    top_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=5)
    top_frame_4.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

    number_label_tab4 = Label(top_frame_4, text=top5CalledNumber[3], font=('Times New Roman', 15   ))
    number_label_tab4.place(relx=0.08, rely=0.025, anchor='n')

    data_frame_4 = tk.Frame(top_frame_4, bd=1)
    data_frame_4.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

    scrollbar_top_4 = Scrollbar(data_frame_4, orient='vertical')
    scrollbar_top_4.pack(side=RIGHT, fill=Y)
    scrollbar_top_4_x = Scrollbar(data_frame_4, orient='horizontal')
    scrollbar_top_4_x.pack(side=BOTTOM, fill=X)

    photoAdder(data_frame_4, top5CalledNumber[3], top5CalledNumber, DCIMpic)

    displaypic4 = whatsappDisplayPicPath[3]
    if displaypic4 != 'None':
        displaypic4 = Avatar+"/"+displaypic4
        my_img_4 = ImageTk.PhotoImage(Image.open('%s' % displaypic4))
    else:
        my_img_4 = ImageTk.PhotoImage(Image.open('unknown_man.png'))

    my_label_4 = Label(top_frame_4, image=my_img_4)
    my_label_4.place(relx=0.71, relwidth=0.29, relheight=1)

    middle_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=10)
    middle_frame_4.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

    img_canvas_4 = tk.Canvas(middle_frame_4, bd=1)
    img_canvas_4.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

    scrollbar_middle_4 = Scrollbar(img_canvas_4, orient='vertical', command=img_canvas_4.yview)
    scrollbar_middle_4.pack(side=RIGHT, fill=Y)
    scrollbar_middle_4_x = Scrollbar(img_canvas_4, orient='horizontal', command=img_canvas_4.xview)
    scrollbar_middle_4_x.pack(side=BOTTOM, fill=X)

    data_list_4 = Listbox(img_canvas_4, width=100)
    for line in GUIdata(top5CalledNumber[0]):
        data_list_4.insert(END, line)
    data_list_4.pack(side=LEFT, fill=BOTH)

    scrollbar_middle_4.config(command=data_list_4.yview)
    scrollbar_middle_4_x.config(command=data_list_4.xview)

    # insert images into this label here

    os.system('cmd /c "%SystemRoot%\\System32\\rundll32.exe "%ProgramFiles%\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen Avatar/6582986382@s.whatsapp.net.jpg" ')

    bottom_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=10)
    bottom_frame_4.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

    upload_button = tk.Button(bottom_frame_4, text="View Image", font=('Modern', 18), command=lambda: openimage(GUIimg(top5CalledNumber[3], top5CalledNumber, DCIMpic), "sus4"))
    upload_button.place(relwidth=0.3, relheight=1)

    save_button_4 = tk.Button(bottom_frame_4, text="Export", font=('Modern', 18), command=lambda: reportGenerator(top5CalledNumber[3], keywords))
    save_button_4.place(relx=0.7, relwidth=0.3, relheight=1)

    canvas_tab4.pack(side="left", fill='both', expand=True)

if len(top5CalledNumber) > 4:
    #Tab 5
    TAB5 = ttk.Frame(TAB_CONTROL)
    TAB_CONTROL.add(TAB5, text='Suspect 5')
    TAB_CONTROL.pack(expand=1, fill='both')

    #code for Tab 5 output
    canvas_tab5 = tk.Canvas(TAB5)
    canvas_tab5.pack()

    #code for Tab 3 output
    top_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=5)
    top_frame_5.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

    number_label_tab5 = Label(top_frame_5, text=top5CalledNumber[4], font=('Times New Roman', 15))
    number_label_tab5.place(relx=0.08, rely=0.025, anchor='n')

    data_frame_5 = tk.Frame(top_frame_5, bd=1)
    data_frame_5.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

    scrollbar_top_5 = Scrollbar(data_frame_5)
    scrollbar_top_5.pack(side=RIGHT, fill=Y)
    scrollbar_top_5_x = Scrollbar(data_frame_5, orient='horizontal')
    scrollbar_top_5_x.pack(side=BOTTOM, fill=X)
    photoAdder(data_frame_5, top5CalledNumber[4], top5CalledNumber, DCIMpic)

    #folder_button = tk.Button(top_frame, text="Upload Folder 1", font=('Modern', 18), command=UploadFolder)
    #folder_button.place(relx=0.41, relwidth=0.29, relheight=1)

    displaypic5 = whatsappDisplayPicPath[4]
    if displaypic5 != 'None':
        displaypic5 = Avatar+"/"+displaypic5
        my_img_5 = ImageTk.PhotoImage(Image.open('%s' % displaypic5))
    else:
        my_img_5 = ImageTk.PhotoImage(Image.open('unknown_man.png'))
    my_label_5 = Label(top_frame_5, image=my_img_5)
    my_label_5.place(relx=0.71, relwidth=0.29, relheight=1)

    middle_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=10)
    middle_frame_5.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

    scrollbar_middle_5 = Scrollbar(middle_frame_5, orient='vertical')
    scrollbar_middle_5.pack(side=RIGHT, fill=Y)
    scrollbar_middle_5_x = Scrollbar(middle_frame_5, orient='horizontal')
    scrollbar_middle_5_x.pack(side=BOTTOM, fill=X)

    data_list_5 = Listbox(middle_frame_5, yscrollcommand=scrollbar_top_5.set, width=100)
    for line in GUIdata(top5CalledNumber[4]):
        data_list_5.insert(END, line)
    data_list_5.pack(side=LEFT, fill=BOTH)

    scrollbar_middle_5.config(command=data_list_5.yview)
    scrollbar_middle_5_x.config(command=data_list_5.xview)

    ###insert the images here

    bottom_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=10)
    bottom_frame_5.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

    upload_button_5 = tk.Button(bottom_frame_5, text="Open Image", font=('Modern', 18), command=lambda: openimage(GUIimg(top5CalledNumber[4], top5CalledNumber, DCIMpic), "sus5"))
    upload_button_5.place(relwidth=0.3, relheight=1)

    save_button_5 = tk.Button(bottom_frame_5, text="Export", font=('Modern', 18), command=lambda: reportGenerator(top5CalledNumber[4], keywords))
    save_button_5.place(relx=0.7, relwidth=0.3, relheight=1)

    canvas_tab5.pack(side="left", fill='both', expand=True)

    ##END OF TAB 5

print("--- Loading Complete ---")
root.mainloop()

