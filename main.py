# imports 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pytube import YouTube
import pytube
from PIL import ImageTk,Image
from tkinter import messagebox
from threading import Thread

# list variable for dynamicly updating available qualities
QUALITY_LIST=['720p']


app=ttk.Window("You Tube Downloader")
selected_quality=ttk.StringVar(value=QUALITY_LIST[0])
# app.geometry("400x500+100+100")
app.resizable(False,False)


file='./assets/logo.png'
video:YouTube=None
img=ImageTk.PhotoImage(Image.open(file).resize((400,300),resample=Image.Resampling.NEAREST))

# frame for contaning logo
img_frame=ttk.Frame(master=app)
img_frame.pack(expand=True,fill=BOTH,padx=20,pady=20,side=TOP)

img_label=ttk.Label(master=img_frame,image=img)
img_label.image=img
img_label.pack(expand=True,fill=BOTH,anchor=N)

# frame for the search bar and load button 
info_frame=ttk.Frame(master=app)
info_frame.pack(expand=True,fill=BOTH,anchor=CENTER,padx=10,pady=20)

link_text=ttk.StringVar(value="")
ttk.Label(master=info_frame,style=INFO,text="Enter Link",font=("monospace",14)).grid(row=0,column=0,padx=20)

link=ttk.Entry(master=info_frame,style=INFO,textvariable=link_text,justify='left',width=35)
link.grid(ipadx=10,row=0,column=1,sticky=EW)

load_btn=ttk.Button(master=info_frame,text="Load",style='info-outline')
load_btn.grid(row=1,column=1,ipadx=10,ipady=10,pady=10,sticky=E)

loading=ttk.Progressbar(master=app,maximum=100,mode='determinate',orient='horizontal',
style='success.Horizontal.TProgressbar',value=13)


ttk.Separator(master=app, orient='horizontal')


# video options available 
options_frame=ttk.Frame(master=app,relief='raised',borderwidth=2)
# options_frame.pack(expand=True,fill=BOTH,anchor=CENTER,padx=20,pady=10)

quality=ttk.Combobox(master=options_frame,state=READONLY,textvariable=selected_quality,justify='center',style='info.TCombobox')
quality.pack(padx=20,pady=20,fill=BOTH,side=TOP,expand=True)

meeter=ttk.Meter(master=options_frame,bootstyle=SUCCESS,subtext="Downloaded",
textright='%',stripethickness=4,amountused=0)

meeter.pack(padx=20,pady=20,fill=BOTH,side=TOP,expand=True)

download_btn=ttk.Button(master=options_frame,text="Download",style='success-outline')
download_btn.pack(padx=10,pady=10,ipadx=5,ipady=5,side=TOP)



# utility functions 
def getInfo():
  loading.pack(pady=10,padx=25,fill=BOTH,expand=TRUE)
  QUALITY_LIST.clear()
  video=YouTube(link_text.get(),on_progress_callback=progress_function,on_complete_callback=completed)
  try:
    QL=video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    i:pytube.Stream=None

    for i in QL:
      
      QUALITY_LIST.append(i.resolution)
    
    quality['values']=QUALITY_LIST
    loading.pack_forget()
    load_btn.grid(row=1,column=1,ipadx=10,ipady=10,pady=10,sticky=E)
    options_frame.pack(expand=True,fill=BOTH,anchor=CENTER,padx=20,pady=10)
  except Exception:
    messagebox.showwarning('error',"could not fetch infomation \n Please make sure you are connected to the network")


def progress_function(stream, chunk,file_handle, bytes_remaining,*args,**kwargs):
  size=stream.filesize
  downloaded=size-bytes_remaining
  precentage=downloaded/size*100
  print(precentage)
  meeter['amountused']=int(precentage)
  meeter.update()
    

def completed(*args,**kwargs):
  options_frame.pack_forget()
  load_btn.grid_configure(row=1,column=1,ipadx=10,ipady=10,pady=10,sticky=E)


def load(event):

  if link_text.get()=='':
    return messagebox.showerror(title="error",message="URL Field can not be empty")

  
  
  try:
    # options_frame.pack(expand=True,fill=BOTH,anchor=CENTER,padx=20,pady=10)
    load_btn.grid_forget()
    t=Thread(target=getInfo)
    t.start()
 
  except Exception as e :
    
    messagebox.showerror(title="error",message="Not a valid you tube Link")
    load_btn.grid_configure(row=1,column=1,ipadx=10,ipady=10,pady=10,sticky=E)
    app.update_idletasks()
    return

  

  # try:
  #   Thread(target=updateMeeter).start()
  #   app.update_idletasks()
  # except Exception:
  #   messagebox.showwarning('error',"can not start the downloading proccess!")
    
def downloadT():
  download_btn.pack_forget()
  # video.streams.get_by_resolution(selected_quality.get()).download()
  YouTube(link_text.get(),on_progress_callback=progress_function,on_complete_callback=completed).streams.get_by_resolution(selected_quality.get()).download()


def downloadNow(e):
  try:
    Thread(target=downloadT).start()
  except Exception:
    return messagebox.showerror('error','Error accured!')


# event binding 
load_btn.bind('<Button-1>',load)
download_btn.bind('<Button-1>',downloadNow)


app.mainloop()