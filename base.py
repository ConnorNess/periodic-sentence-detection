import tkinter as tk 
from tkinter import *
from tkinter import messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
#PunktSentenceTokenizer #Punkt is trained but can be retrained on data, going to use for ML later on
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()
import os

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

###---------------------------------------------------TRAINING---------------------------------------------------###
training_file = open(os.path.join(sys.path[0],'TrainingBase.txt'))
train_file = training_file.read()
open(os.path.join(sys.path[0],'TrainingCleaned.txt', 'w"').close())
cleantrain_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'))
sentenceTraining = nltk.sent_tokenize(train_file)
train_pos = [] #Part-of-Speech base check build from training
stemmed_train = []

for sentence in sentenceTraining:
    words = nltk.word_tokenize(sentence)
    filtered_train = [w for w in words if not w in stop_words] #Adds token words provided they are not stop words
    
    for word in filtered_train:
        stemmed_train.append(ps.stem(word))



    # for w in stemmed_train:
    #     if (i > (round(((len(stemmed_train)/100)*31.4)))):
    #         train_pos.append(nltk.pos_tag(w))



###---------------------------------------------------INPUT---------------------------------------------------###
def input_file(): #Takes in input file and tokenizes sentences
    text = open("C:\\Users\\Connorrness\\Documents\\Hons\\periodic-sentence-detection\\input.txt", "r")
    user_file = text.read()
    sentenceTokens = nltk.sent_tokenize(user_file)
    
    for sentence in sentenceTokens:
        words = nltk.word_tokenize(sentence)
        filtered_sentence = [w for w in words if not w in stop_words]
        stemmed_sentence = []
        for w in filtered_sentence:
            stemmed_sentence.append(ps.stem(w))
        print(stemmed_sentence)


###---------------------------------------------------WINDOW---------------------------------------------------###
root = tk.Tk() #root==mainwindow
root.title("GUI Base")
root.geometry('500x300')

frameFileUpload = Frame(root)

fileInput = tk.Text(frameFileUpload, height=5, width=70)
fileInput.pack()
btnTrainingFile = tk.Button(frameFileUpload, text="Test With File", command=input_file)
btnTrainingFile.pack()
frameFileUpload.pack()

root.mainloop()