import boto3
import os
import mediapipe as mp
import time
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import cv2
from tkinter import filedialog


# def xuly(event):
#     global root
#     root.filename = filedialog.askopenfilename(initialdir="", title="Select A File",
#                                                filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
#     print(root.filename)
# root = Tk()
# root.title("Nhận diện khuôn mặt")
# root.geometry('400x300')
# bt=tk.Button(root,text='OPEN',fg='black')
# bt.pack(side=TOP,fill=BOTH)
# bt.bind('<Button-1>',xuly)
# root.mainloop()
access_key_id = 'ASIA4AO7KQFMJX434X6G'
secret_access_key = 'PTngEyUqZi0EOA7GqPIQQwuVseI4V7KpVOW8elA8'
session_token = 'FwoGZXIvYXdzEAIaDAAIK2So8tPMi1SvWiLPAb2tMaeDetD7Muy32aDAOUbC7Z8uU6zec8r1A4JXZyZhS1CS21Sl3jvJcVoxXh06NgJoSu5cTcjZKD9ROb2CGZ7g4Rx5XjAStJ6oA1FuW3n+vVUvNhQIsMQYTexInF1b8vRCkTXJhL04OAOg9jRU3M57HvpSk1YOV6hhsNgG0VVmwSSo2HMl9THiPvJQzwRLXEu9Jswccc9JrCS0EHxKq95VLM8lD+iEeTG+6jnjJCzQyghyUeXRnvZpqkPZwuKv0PIYnRY/U+KqkbN/lvAYUyizhI2NBjItV6yWAF6gyjpBKZkDOmip/QJmeGQ3NduCyOyRfXr2EP6LHx3khGwdyM4u90f9'
region = 'us-east-1'
client=boto3.client('rekognition',
                    region_name=region,
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    aws_session_token=session_token)
photo='SonTung.jpg'
photo2='frame69.jpg'
s3 = boto3.resource(
    service_name='s3',
    region_name=region,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token
)

currentframe=0;
def Chuyendoi(anh):
    with open(anh, 'rb') as source_image:
        source_bytes = source_image.read()
        return source_bytes
def Sosanh(source_bytes):
    index = 0
    while (index<6):
        anh = './celebs' + str(index) + '.jpg'
        with open(anh, 'rb') as source_image:
            source_bytes2 = source_image.read()
        response = client.compare_faces(SourceImage={'Bytes': source_bytes}, TargetImage={'Bytes': source_bytes2})
        if(response['FaceMatches']!=[]):
            if(response['FaceMatches'][0]['Similarity']>70):
                return index
        index += 1
    return -1
def kiemTraNgheSi(index):
    switcher={
        0: 'Châu Bùi',
        1: 'Sơn Tùng M-TP',
        2: 'Elon Musk',
        3: 'Chi Pu',
        4: 'Đông Nhi',
        5: 'Ông Cao Thắng',
        6: 'Karik',
        7: 'Mai Phương Thúy',
        8: 'Trường Giang',
        9: 'Nhã Phương',
        10: 'Trấn Thành',
        11: 'Hari Won',
        12: 'Erik',
        13: 'Đức Phúc',
        14: 'Hòa Minzy',
    }
    return switcher.get(index,"Không nhận dạng được")
win = Tk()
win.geometry("600x600+200+30")
win.resizable(False, False)
win.configure(bg ='white')
w = 400
h = 300

color = "#00406e"
frame_1 = Frame(win,width = 600,height =330,bg = color).place(x=0,y=0)
frame_2 = Frame(win,width = 600,height =320,bg = color).place(x=0,y=350)

v = Label(frame_1, width=w, height=h)
v.place(x=10, y=10)
cap = cv2.VideoCapture("C:\\Users\\Admin\\Downloads\\QC.mp4")

labl = Label(win, text="", width=25, height=2).place(x=350, y=400)
frm = Label(frame_2,bg="black", width=43, height=13, borderwidth=1).place(x=10, y=370)
def take_copy(im):
    la = Label(frame_2, width=w-100, height=h-100)
    la.place(x=10, y=370)
    copy = im.copy()
    copy = cv2.resize(copy, (w-100, h-100))
    rgb = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(copy)
    imgtk = ImageTk.PhotoImage(image)
    la.configure(image=imgtk)
    la.image = imgtk
    name = './data/frame' + str(currentframe) + '.jpg'
    cv2.imwrite(name, rgb)
    vitri = Sosanh(Chuyendoi(name))
    ketqua=kiemTraNgheSi(vitri)
    print(ketqua)
    save = Label(win, text=ketqua, width=25, height=2).place(x=350, y=400)

def select_img():
    global rgb
    _, img = cap.read()
    img = cv2.resize(img, (w, h))
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image)
    v.configure(image=imgtk)
    v.image = imgtk
    v.after(30, select_img)


select_img()
snap = Button(win, text="capture", command=lambda:[take_copy(rgb)])
snap.place(x=450, y=150, width=60, height=50)

win.mainloop()