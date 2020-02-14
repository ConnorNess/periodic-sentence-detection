import tkinter as tk 
from tkinter import *
from tkinter import messagebox

root = tk.Tk() #root==mainwindow
root.title("GUI Base")
root.geometry('500x200')

frameTextInput = Frame(root)
frameFileUpload = Frame(root)

sentenceInput = tk.Text(frameTextInput, height=5, width=70)
sentenceInput.pack()

def checkSentence():
    input = sentenceInput.get("1.0", END) #1.0==input read from line1-char0 || END==reads until end of textbox

    chkLength = len(input.split())
    
    basicCheck = 18
    sentencePosition = 1
    commaPosition = 0

    if (chkLength > basicCheck):
        for word in input.split():
            sentencePosition + 1
            if ',' in word:
                commaPosition = sentencePosition
        if (((commaPosition/sentencePosition)*100) > 20):
            messagebox.showinfo("Check 1", "Likely periodic")
        else:
            messagebox.showinfo("Check 1", "Unlikely periodic")



btnChkSntnc = tk.Button(frameTextInput, text="Process", command=checkSentence)

btnChkSntnc.pack()
frameTextInput.pack()
frameFileUpload.pack()

root.mainloop()