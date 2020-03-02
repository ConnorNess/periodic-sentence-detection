import tkinter as tk 
from tkinter import *
from tkinter import messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
#PunktSentenceTokenizer #Punkt is trained but can be retrained on data, going to use for ML later on
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()

#trainingfile = open("C:\\Users\\Connorrness\\Documents\\Hons\\periodic-sentence-detection\\TrainingBase.txt")
stop_words = set(stopwords.words("english"))
ps = PorterStemmer()

def inputFile():
    text = open("C:\\Users\\Connorrness\\Documents\\Hons\\periodic-sentence-detection\\TrainingBase.txt", "r")
    userFile = text.read()
    tokens = nltk.sent_tokenize(userFile) #Tokenize each sentence in the input, means we aren't reading by line or something inefficient or blatantly useless like that
    print (len(tokens))
    for i in range(0, len(tokens)):
        input = tokens [i]
        sentenceChecks(input)

def inputTextbox():
    input = sentenceInput.get("1.0", END) #1.0==input read from line1-char0 && END==reads until end of textbox
    sentenceChecks(input)

def sentenceChecks(input):
    #words = word_tokenize(input)
    #filteredInput = [w for w in words if not w in stop_words] #Iterates through words in sentence, if a word is a stop_word, it is not included in the filtered sentence
    #stemmedInput = [ps.stem(w) for w in filteredInput]
    #TODO: Stem incoming input further after stop_words filter
    naiveCheckCommaByLength(input) #Naive checks use unfiltered inputs, they aren't very accurate either way.

def naiveCheckCommaByLength(input):
        chkLength = len(input.split())
        #print(sent_tokenize(input))
        #print(word_tokenize(input))

        words = nltk.word_tokenize(input)
        tagged = nltk.pos_tag(words)
        #print(tagged)

        basicCheck = 18
        sentencePosition = 1
        commaPosition = 0

        if (chkLength > basicCheck):
            for word in input.split():
                sentencePosition += 1
                if ',' in word:
                    commaPosition = sentencePosition
            if (((commaPosition/sentencePosition)*100) > 20):
                print("lul")
        else:
            print("pog")

###---------------------------------------------------WINDOW---------------------------------------------------###
root = tk.Tk() #root==mainwindow
root.title("GUI Base")
root.geometry('500x300')

frameTextInput = Frame(root)
frameFileUpload = Frame(root)

sentenceInput = tk.Text(frameTextInput, height=5, width=70)
sentenceInput.pack()
btnChkSntnc = tk.Button(frameTextInput, text="Process", command=inputTextbox)
btnChkSntnc.pack()
frameTextInput.pack()

fileInput = tk.Text(frameTextInput, height=5, width=70)
fileInput.pack()
btnTrainingFile = tk.Button(frameFileUpload, text="Test With File", command=inputFile)
btnTrainingFile.pack()
frameFileUpload.pack()

root.mainloop()