import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os


def UploadFolder(event=None):
    Folder1 = None
    Folder1 = filedialog.askopenfilename()

    if Folder1 != "":
        current_directory = os.getcwd()
        print(Folder1)
        print(current_directory)
        #cmd = 'copy "-{0} -{1}"'.format(Folder1, current_directory)
        #cmd = 'copy C:\\Users\\jiaxuan7\\Desktop\\Timetable.jpg C:'
        #os.system('copy "-{0} -{1}"'.format(Folder1, current_directory))
        print(Folder1, ' Uploaded')
    else:
        print('You have selected nothing')

root = tk.Tk()
root.title('WhatsApp Analyzer Tool')
# configuring the size of the window
root.geometry('700x500')

#create tab control
TAB_CONTROL = ttk.Notebook(root)

#Tab 1
TAB1 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB1, text='Suspect 1')

canvas_tab1 = tk.Canvas(TAB1)
canvas_tab1.pack()

# def printPhoto():
#     image = tk.PhotoImage(file=Folder1)
#     imagelabel = tk.Label(middle_frame, image=image)
#     imagelabel.place(relwidth=0.3, relheight=0.3)

top_frame = tk.Frame(TAB1, bg="#57AEC5", bd=5)
top_frame.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

number_label_tab1 = Label(top_frame, text="12345678", font=('Times New Roman', 15   ))
number_label_tab1.place(relx=0.08, rely=0.025, anchor='n')

data_frame = tk.Frame(top_frame, bd=1)
data_frame.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

scrollbar_top = Scrollbar(data_frame)
scrollbar_top.pack(side=RIGHT, fill=Y)

data_list = Listbox(data_frame, yscrollcommand=scrollbar_top.set)
for line in range(100):
    data_list.insert(END, "this is line number " + str(line))
data_list.pack(side=LEFT, fill=BOTH)
scrollbar_top.config(command=data_list.yview)

data_label = Label(top_frame)
data_label.place(relx=0.08, rely=0.025, anchor='n')

#folder_button = tk.Button(top_frame, text="Upload Folder 1", font=('Modern', 18), command=UploadFolder)
#folder_button.place(relx=0.41, relwidth=0.29, relheight=1)

my_img = ImageTk.PhotoImage(Image.open("Avatar/6591864789@s.whatsapp.net.jpg"))
my_label = Label(top_frame, image=my_img)
my_label.place(relx=0.71, relwidth=0.29, relheight=1)

middle_frame = tk.Frame(TAB1, bg="white", bd=10)
middle_frame.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

img_canvas = tk.Canvas(middle_frame, bd=1)
img_canvas.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

scrollbar_middle = Scrollbar(img_canvas, command=img_canvas.yview)
scrollbar_middle.pack(side=RIGHT, fill=Y)
scrollable_frame = Frame(middle_frame)

scrollable_frame.bind(
    "<Configure>",
    lambda e: img_canvas.configure(
        scrollregion=img_canvas.bbox("all")
    )
)

img_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
img_canvas.configure(yscrollcommand=scrollbar_middle.set)

### insert the images here for image canvas

bottom_frame = tk.Frame(TAB1, bg="#57AEC5", bd=10)
bottom_frame.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

upload_button = tk.Button(bottom_frame, text="Upload", font=('Modern', 18), command=UploadFolder)
upload_button.place(relwidth=0.3, relheight=1)

save_button = tk.Button(bottom_frame, text="Export", font=('Modern', 18))
save_button.place(relx=0.7, relwidth=0.3, relheight=1)

canvas_tab1.pack(side="left", fill='both', expand=True)

#END OF TAB 1


#Tab 2
TAB2 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB2, text='Suspect 2')

#tk.Label(TAB1, text="this is tab 1").grid(column=0, row=0, padx=10, pady=10)
canvas_tab2 = tk.Canvas(TAB2)
canvas_tab2.pack()

top_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=5)
top_frame_2.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

number_label_tab2 = Label(top_frame_2, text="12345678", font=('Times New Roman', 15   ))
number_label_tab2.place(relx=0.08, rely=0.025, anchor='n')

data_frame_2 = tk.Frame(top_frame_2, bd=1)
data_frame_2.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

scrollbar_top_2 = Scrollbar(data_frame_2)
scrollbar_top_2.pack(side=RIGHT, fill=Y)

data_list_2 = Listbox(data_frame_2, yscrollcommand=scrollbar_top_2.set)
for line in range(100):
    data_list_2.insert(END, "this is line number " + str(line))
data_list_2.pack(side=LEFT, fill=BOTH)
scrollbar_top_2.config(command=data_list_2.yview)

data_label_2 = Label(top_frame_2)
data_label_2.place(relx=0.08, rely=0.025, anchor='n')

#folder_button = tk.Button(top_frame, text="Upload Folder 1", font=('Modern', 18), command=UploadFolder)
#folder_button.place(relx=0.41, relwidth=0.29, relheight=1)

my_img_2 = ImageTk.PhotoImage(Image.open("Avatar/6591864789@s.whatsapp.net.jpg"))
my_label_2 = Label(top_frame_2, image=my_img_2)
my_label_2.place(relx=0.71, relwidth=0.29, relheight=1)

middle_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=10)
middle_frame_2.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

img_canvas_2 = tk.Canvas(middle_frame_2, bd=1)
img_canvas_2.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

scrollbar_middle_2 = Scrollbar(img_canvas_2, command=img_canvas_2.yview)
scrollbar_middle_2.pack(side=RIGHT, fill=Y)
scrollable_frame_2 = Frame(middle_frame_2)

scrollable_frame_2.bind(
    "<Configure>",
    lambda e: img_canvas_2.configure(
        scrollregion=img_canvas_2.bbox("all")
    )
)

img_canvas_2.create_window((0, 0), window=scrollable_frame_2, anchor='nw')
img_canvas_2.configure(yscrollcommand=scrollbar_middle_2.set)

for i in range(50):
    Label(scrollable_frame_2, text="Sample scrolling label").pack()

bottom_frame_2 = tk.Frame(TAB2, bg="#57AEC5", bd=10)
bottom_frame_2.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

upload_button_2 = tk.Button(bottom_frame_2, text="Upload", font=('Modern', 18), command=UploadFolder)
upload_button_2.place(relwidth=0.3, relheight=1)

save_button_2 = tk.Button(bottom_frame_2, text="Export", font=('Modern', 18))
save_button_2.place(relx=0.7, relwidth=0.3, relheight=1)

canvas_tab2.pack(side="left", fill='both', expand=True)
#code for Tab 2 output

#Tab 3
TAB3 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB3, text='Suspect 3')

#tk.Label(TAB1, text="this is tab 1").grid(column=0, row=0, padx=10, pady=10)
canvas_tab3 = tk.Canvas(TAB3)
canvas_tab3.pack()

#code for Tab 3 output
top_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=5)
top_frame_3.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

number_label_tab3 = Label(top_frame_3, text="12345678", font=('Times New Roman', 15))
number_label_tab3.place(relx=0.08, rely=0.025, anchor='n')

data_frame_3 = tk.Frame(top_frame_3, bd=1)
data_frame_3.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

scrollbar_top_3 = Scrollbar(data_frame_3)
scrollbar_top_3.pack(side=RIGHT, fill=Y)

data_list_3 = Listbox(data_frame_3, yscrollcommand=scrollbar_top_3.set)
for line in range(100):
    data_list_3.insert(END, "this is line number " + str(line))
data_list_3.pack(side=LEFT, fill=BOTH)
scrollbar_top_3.config(command=data_list_3.yview)

data_label_3 = Label(top_frame_3)
data_label_3.place(relx=0.08, rely=0.025, anchor='n')

my_img_3 = ImageTk.PhotoImage(Image.open("Avatar/6591864789@s.whatsapp.net.jpg"))
my_label_3 = Label(top_frame_3, image=my_img_3)
my_label_3.place(relx=0.71, relwidth=0.29, relheight=1)

middle_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=10)
middle_frame_3.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

img_canvas_3 = tk.Canvas(middle_frame_3, bd=1)
img_canvas_3.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

scrollbar_middle_3 = Scrollbar(img_canvas_3, command=img_canvas_3.yview)
scrollbar_middle_3.pack(side=RIGHT, fill=Y)
scrollable_frame_3 = Frame(middle_frame_3)

scrollable_frame_3.bind(
    "<Configure>",
    lambda e: img_canvas_3.configure(
        scrollregion=img_canvas_3.bbox("all")
    )
)

img_canvas_3.create_window((0, 0), window=scrollable_frame_3, anchor='nw')
img_canvas_3.configure(yscrollcommand=scrollbar_middle_3.set)

for i in range(50):
    Label(scrollable_frame_3, text="Sample scrolling label").pack()

bottom_frame_3 = tk.Frame(TAB3, bg="#57AEC5", bd=10)
bottom_frame_3.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

upload_button_3 = tk.Button(bottom_frame_3, text="Upload", font=('Modern', 18), command=UploadFolder)
upload_button_3.place(relwidth=0.3, relheight=1)

save_button_3 = tk.Button(bottom_frame_3, text="Export", font=('Modern', 18))
save_button_3.place(relx=0.7, relwidth=0.3, relheight=1)

canvas_tab3.pack(side="left", fill='both', expand=True)

#Tab 4
TAB4 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB4, text='Suspect 4')

#code for Tab 4 output
#tk.Label(TAB1, text="this is tab 1").grid(column=0, row=0, padx=10, pady=10)
canvas_tab4 = tk.Canvas(TAB4)
canvas_tab4.pack()

#code for Tab 3 output
top_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=5)
top_frame_4.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

number_label_tab4 = Label(top_frame_4, text="12345678", font=('Times New Roman', 15   ))
number_label_tab4.place(relx=0.08, rely=0.025, anchor='n')

data_frame_4 = tk.Frame(top_frame_4, bd=1)
data_frame_4.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

scrollbar_top_4 = Scrollbar(data_frame_4)
scrollbar_top_4.pack(side=RIGHT, fill=Y)

data_list_4 = Listbox(data_frame_4, yscrollcommand=scrollbar_top_4.set)
for line in range(100):
    data_list_4.insert(END, "this is line number " + str(line))
data_list_4.pack(side=LEFT, fill=BOTH)
scrollbar_top_4.config(command=data_list_4.yview)

data_label_4 = Label(top_frame_4)
data_label_4.place(relx=0.08, rely=0.025, anchor='n')

#folder_button = tk.Button(top_frame, text="Upload Folder 1", font=('Modern', 18), command=UploadFolder)
#folder_button.place(relx=0.41, relwidth=0.29, relheight=1)

my_img_4 = ImageTk.PhotoImage(Image.open("Avatar/6591864789@s.whatsapp.net.jpg"))
my_label_4 = Label(top_frame_4, image=my_img_4)
my_label_4.place(relx=0.71, relwidth=0.29, relheight=1)

middle_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=10)
middle_frame_4.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

img_canvas_4 = tk.Canvas(middle_frame_4, bd=1)
img_canvas_4.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

scrollbar_middle_4 = Scrollbar(img_canvas_4, command=img_canvas_4.yview)
scrollbar_middle_4.pack(side=RIGHT, fill=Y)
scrollable_frame_4 = Frame(middle_frame_4)

scrollable_frame_4.bind(
    "<Configure>",
    lambda e: img_canvas_4.configure(
        scrollregion=img_canvas_4.bbox("all")
    )
)

img_canvas_4.create_window((0, 0), window=scrollable_frame_4, anchor='nw')
img_canvas_4.configure(yscrollcommand=scrollbar_middle_4.set)

### insert images into this label here
for i in range(50):
    Label(scrollable_frame_4, text="Sample scrolling label").pack()

bottom_frame_4 = tk.Frame(TAB4, bg="#57AEC5", bd=10)
bottom_frame_4.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

upload_button = tk.Button(bottom_frame, text="Upload", font=('Modern', 18), command=UploadFolder)
upload_button.place(relwidth=0.3, relheight=1)

save_button = tk.Button(bottom_frame, text="Export", font=('Modern', 18))
save_button.place(relx=0.7, relwidth=0.3, relheight=1)

canvas_tab4.pack(side="left", fill='both', expand=True)

#Tab 5
TAB5 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB5, text='Suspect 5')
TAB_CONTROL.pack(expand=1, fill='both')

#code for Tab 5 output
#tk.Label(TAB1, text="this is tab 1").grid(column=0, row=0, padx=10, pady=10)
canvas_tab5 = tk.Canvas(TAB5)
canvas_tab5.pack()

#code for Tab 3 output
top_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=5)
top_frame_5.place(relx=0.5, rely=0.01, relwidth=0.75, relheight=0.3, anchor='n')

number_label_tab5 = Label(top_frame_5, text="12345678", font=('Times New Roman', 15))
number_label_tab5.place(relx=0.08, rely=0.025, anchor='n')

data_frame_5 = tk.Frame(top_frame_5, bd=1)
data_frame_5.place(relx=0.35, rely=0.3, relwidth=0.7, relheight=0.7, anchor='n')

scrollbar_top_5 = Scrollbar(data_frame_5)
scrollbar_top_5.pack(side=RIGHT, fill=Y)

data_list_5 = Listbox(data_frame_5, yscrollcommand=scrollbar_top_5.set)
for line in range(100):
    data_list_5.insert(END, "this is line number " + str(line))
data_list_5.pack(side=LEFT, fill=BOTH)
scrollbar_top_5.config(command=data_list_5.yview)

data_label_5 = Label(top_frame_5)
data_label_5.place(relx=0.08, rely=0.025, anchor='n')

#folder_button = tk.Button(top_frame, text="Upload Folder 1", font=('Modern', 18), command=UploadFolder)
#folder_button.place(relx=0.41, relwidth=0.29, relheight=1)

my_img_5 = ImageTk.PhotoImage(Image.open("Avatar/6591864789@s.whatsapp.net.jpg"))
my_label_5 = Label(top_frame_5, image=my_img_5)
my_label_5.place(relx=0.71, relwidth=0.29, relheight=1)

middle_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=10)
middle_frame_5.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.5, anchor='n')

img_canvas_5 = tk.Canvas(middle_frame_5, bd=1)
img_canvas_5.place(relx=0.5, rely=0.01, relwidth=1, relheight=1, anchor='n')

scrollbar_middle_5 = Scrollbar(img_canvas_5, command=img_canvas_5.yview)
scrollbar_middle_5.pack(side=RIGHT, fill=Y)
scrollable_frame_5 = Frame(middle_frame_5)

scrollable_frame_5.bind(
    "<Configure>",
    lambda e: img_canvas_5.configure(
        scrollregion=img_canvas_5.bbox("all")
    )
)

img_canvas_5.create_window((0, 0), window=scrollable_frame_5, anchor='nw')
img_canvas_5.configure(yscrollcommand=scrollbar_middle_5.set)

###insert the images here
for i in range(50):
    Label(scrollable_frame_5, text="Sample scrolling label").pack()

bottom_frame_5 = tk.Frame(TAB5, bg="#57AEC5", bd=10)
bottom_frame_5.place(relx=0.5, rely=0.8, relwidth=0.75, relheight=0.1, anchor='n')

upload_button_5 = tk.Button(bottom_frame_5, text="Upload", font=('Modern', 18), command=UploadFolder)
upload_button_5.place(relwidth=0.3, relheight=1)

save_button_5 = tk.Button(bottom_frame_5, text="Export", font=('Modern', 18))
save_button_5.place(relx=0.7, relwidth=0.3, relheight=1)

canvas_tab5.pack(side="left", fill='both', expand=True)

##END OF TAB 5

root.mainloop()