import tkinter as tk 
from tkinter import *
from tkinter import messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
#PunktSentenceTokenizer #Punkt is trained but can be retrained on data, going to use for ML later on
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()

stop_words = set(stopwords.words("english"))
ps = PorterStemmer()

###---------------------------------------------------TRAINING---------------------------------------------------###
training_file = open("C:\\Users\\Connorrness\\Documents\\Hons\\periodic-sentence-detection\\TrainingBase.txt")
train_file = training_file.read()
sentenceTraining = nltk.sent_tokenize(train_file)

for sentence in sentenceTraining:
    words = nltk.word_tokenize(sentence)
    filtered_train = [w for w in words if not w in stop_words]
    stemmed_train = []
    for w in filtered_train:
        stemmed_train.append(ps.stem(w))
    tagged_train = nltk.pos_tag(stemmed_train)
    print(tagged_train[0][1]) #Its printing element 0 of each input,,,, why

    

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