from tkinter import *          
from PIL import ImageTk,Image  #to insert image and resize it we use this module
from tkinter import filedialog  #to get the address of file from system 
from tkinter import messagebox  #to genrate a popup message box
from pandas import * 
from matplotlib import pyplot as plt


root = Tk()
root.geometry("1000x768+0+0")
root.title("Expense Tracker")
root.iconbitmap('logo.ico')

#Title for the main page
    #rectangular background with a solid colour
frame = Frame(root, width=1000, height=75, bg="#092532")
frame.grid(row=0, column=0, columnspan=5, sticky=W)
frame.grid_propagate(0)
Main_label = Label(frame, text="Personal Expense Tracker", bg="#092532", font=("calibri", 35, "bold"), fg="light yellow")
Main_label.grid(row=0, column=0, columnspan=5, padx=20,pady=5)

#Instruction grid
    #opening all the images that are to be used
img1=ImageTk.PhotoImage(Image.open("1.png"))
img2=ImageTk.PhotoImage(Image.open("2.png"))
img3=ImageTk.PhotoImage(Image.open("3.png"))
img4=ImageTk.PhotoImage(Image.open("4.png"))
img5=ImageTk.PhotoImage(Image.open("5.png"))
img6=ImageTk.PhotoImage(Image.open("6.png")) 

ins_list=[img1, img2, img3, img4, img5, img6]

img_label=Label(root,image=img1,height=200,width=1000)
img_label.grid(row=1,column=0,columnspan=5,pady=5)

def ins(x):
    global image
    
    image+=x           
    
    img_label=Label(root,image=ins_list[image],height=200,width=1000)
    img_label.grid(row=1,column=0,columnspan=5,pady=5)
    
    if(image==0):
        pre['state']=DISABLED
    elif(image==5):
        next['state']=DISABLED
        skip.config(text="Next",padx=81)
    else:
        pre['state']=NORMAL
        next['state']=NORMAL    
           
    return 

# Input dialog-box
def skipcmd():
    global name
    name=Entry(root,width=50,borderwidth=3) 
    name.grid(row=3,column=1,columnspan=3,pady=50) 
    name.insert(0,"Enter Your Name")  
    
    skip.destroy()
    
    next1.grid(row=4,column=1,columnspan=3)
    
    
    return

def next_fun():
    next1.destroy()
    
    file.grid(row=5,column=1,columnspan=2)
    cont.grid(row=5,column=2,columnspan=2)
    
    return

global skip, pre, next
image=0
pre=Button(root,text="<<",padx=50,pady=5,borderwidth=3, state=DISABLED,command=lambda: ins(-1))
next=Button(root,text=">>",padx=50,pady=5,borderwidth=3, command=lambda: ins(1))  
skip=Button(root,text="Skip Instructions",padx=50,pady=5,borderwidth=5,command=skipcmd)
next1=Button(root,text="Next",padx=50,pady=5,borderwidth=3,command=next_fun)
 
pre.grid(row=2,column=1)
skip.grid(row=2,column=2)
next.grid(row=2,column=3)


def open():
    
    global address, add_label
    root.filename=filedialog.askopenfilename(initialdir="Desktop",title="Select a file", filetype=(("Excel File","*.csv"),("All","*.*")))
    address=root.filename

    add_label= Label(root,text="File Location : "+address)
    
    add_label.grid(row=6,column=1,columnspan=3,pady=15)    
    cont['state']=NORMAL
    file['state']=DISABLED
    
    reset.grid(row=5,column=2)
    
    
    return
    
def reset_fun():
    cont['state']=DISABLED
    file['state']=NORMAL
    add_label.grid_forget()
     
     
def track():
    #opration on the file
    global earning, spend, saving, amo, date,D,E,S,avgE,avgS
    csvfile=read_csv(address)
    amo=csvfile['Amount'].tolist()
    date=csvfile['Date'].tolist()
    earning=0
    spend=0
    for i in range(len(amo)):
        if (amo[i]>0):
            earning=earning+amo[i]
        elif(amo[i]<0):
            spend=spend-amo[i]
        
           
    saving=earning-spend
    
    D = []  #days
    E = []  #earning
    S = []  #spenind
    avgE = []
    avgS = []    
    for i in range(32):
        D.append(i)
        E.append(0)
        S.append(0)
        avgE.append(earning/30)
        avgS.append(spend/30)
    
    for i in range(len(amo)):  
        
        temp=str(date[i])     
        j=int(temp[0:2])-1

        if(amo[i]>0):
            E[j] = E[j] + amo[i]
        else:
            S[j] = S[j] - amo[i]
    
    return     
    
def graph1():
    #piechart
    SAVING=[saving]
    SPEND=[spend]
    activities=['Saving','Spending']
    slices=[saving,spend]
    cols=['red','blue']
    plt.pie(slices,labels=activities,colors=cols,explode=(0.3,0.0),autopct="%1.1f%%")
    plt.show()
        
    return

def graph2():
    SAVING=[saving]
    SPEND=[spend]
    activities=['Per Day Saving','Per Day Spending']
    slices=[saving/30,spend/30]
    cols=['red','blue']
    
    plt.pie(slices,labels=activities,colors=cols,explode=(0.3,0.0),autopct="%1.1f%%")
    plt.show()
    
    return

def graph3():
    
    plt.bar(D,E)
    plt.plot(D,avgE,color='red')
    plt.show()
    
    return

def graph4():
    
    plt.bar(D,S,color='orange')
    plt.plot(D,avgS,color='red')
    plt.show()
        
    return

def graph():
    b1=Button(window,text=" Month Pi-Chart ",padx=10,pady=10,borderwidth=3,command=graph1)
    b2=Button(window,text="  Day Pi-Chart  ",padx=12,pady=10,borderwidth=3,command=graph2)
    b3=Button(window,text="Day wise Earning",padx=12,pady=10,borderwidth=3,command=graph3)
    b4=Button(window,text="Day wise Spending",padx=12,pady=10,borderwidth=3,command=graph4  )
        
    but1.destroy()
    b1.grid(row=6,column=2,pady=5,padx=10)
    b2.grid(row=7,column=2,pady=5,padx=10)
    b3.grid(row=8,column=2,pady=5,padx=10)
    b4.grid(row=9,column=2,pady=5,padx=10)
    
    return
    
     
window=""

def new_window():
    if(address==""):
        messagebox.showwarning("Warning","No file selected. Please select a file") #popup messgae for no file selected
        return
    elif(address[-4:]!=".csv"):
        messagebox.showerror("Error","The file type is not supported") #popup messgae for the wrong file
        return 
    elif(name.get()=="Enter Your Name"):
        messagebox.showerror("Error","Please Enter Your Name.") #popup messgae to enter the name
        return 
    
    track()
    
    global window
    window = Toplevel()
    window.geometry("1366x768+0+0")
    window.title("Expense Tracker")
    window.iconbitmap('logo.ico')

    #Title for the 2nd window
        #rectangular background with a solid colour
    frame = Frame(window, width=1366, height=75, bg="#092532")
    frame.grid(row=0, column=0, columnspan=5, sticky=W)
    frame.grid_propagate(0)
    Main_label = Label(frame, text="Personal Expense Tracker", bg="#092532", font=("calibri", 35, "bold"), fg="light yellow")
    Main_label.grid(row=0, column=0, columnspan=5, padx=20,pady=5)

    intro_label=Label(window,text="Hello! "+name.get()+", Welcome to the Expense Tracker",font=("calibri", 20, "bold"))
    intro_label.grid(row=1,column=1,columnspan=3,pady=15)
    
    info1=Label(window,text="Total Earning of the month : " + str(earning),font=("calibri", 20))
    info1.grid(row=2,column=1,columnspan=3,pady=15)
    info2=Label(window,text="Total money Spend in this month : " + str(spend),font=("calibri", 20))
    info2.grid(row=3,column=1,columnspan=3,pady=15)
    info3=Label(window,text="Total money Savings in this month : " + str(saving),font=("calibri", 20))
    info3.grid(row=4,column=1,columnspan=3,pady=15)

    global but1
    but1=Button(window,text="See in graph",padx=50,pady=5,borderwidth=3,command=graph)
    but2=Button(window,text="Exit",padx=50,pady=5,borderwidth=3,command=lambda: root.destroy())
    
    but1.grid(row=5,column=1,columnspan=2)
    but2.grid(row=5,column=2,columnspan=2)
    

    return




global file, cont, reset

file=Button(root,text="Import File",padx=50,pady=5,borderwidth=3, command=open)
cont=Button(root,text="Continue",state=DISABLED,padx=50,pady=5,borderwidth=3, command=new_window)
reset=Button(root,text="Reset",padx=50,pady=5,borderwidth=3,command=reset_fun)


root.mainloop()