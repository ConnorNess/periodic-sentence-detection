import tkinter as tk 
from tkinter import *
from tkinter import messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()
import numpy
import os

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

###---------------------------------------------------CLEANING---------------------------------------------------###
training_file = open(os.path.join(sys.path[0],'TrainingBase.txt'))
train_file = training_file.read()

if os.path.exists(os.path.join('TrainingCleaned.txt')): #Deleting and remaking cleaned training data
    os.remove(os.path.join(sys.path[0],'TrainingCleaned.txt'))
cleantrain_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'w') 

sentenceTraining = nltk.sent_tokenize(train_file)
punctuationremover = RegexpTokenizer(r'\w+')

for sentence in sentenceTraining:
    word_counter = 0
    sentencePoS = ""
    sentencePoS_no_punctuation = ""

    words = word_tokenize(sentence)
    filtered_trainer = [w for w in words if not w in stop_words] #cleaning stop words
    tagged_sentence_trainer = nltk.pos_tag(filtered_trainer)
    cleantrain_file.write("@: ") #Marks source sentence

    for word in filtered_trainer:
        cleantrain_file.write(ps.stem(word))
        cleantrain_file.write(" ")

        sentencePoS += (tagged_sentence_trainer[word_counter][1])
        sentencePoS += " "

        if punctuationremover.tokenize(word):
            sentencePoS_no_punctuation += (tagged_sentence_trainer[word_counter][1])
            sentencePoS_no_punctuation += " "

        word_counter += 1
    cleantrain_file.write("\n")
    cleantrain_file.write("#: " + sentencePoS) #Marks punctuated parts of speech
    cleantrain_file.write("\n")
    cleantrain_file.write("%: " + sentencePoS_no_punctuation) #Marks non-punctuated parts of speech
    cleantrain_file.write("\n")
    
cleantrain_file.close()

###---------------------------------------------------TRAINING---------------------------------------------------###
training_PoS_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'r')
PoS_frequency = []
#PoS_frequency_no_punctuation = numpy.array([])
comma_length_to_end = []


for line in training_PoS_file:
    words_after_comma = 0
    comma_present = False

    if line[0:3] == "#: ":
        trimmed_line = line[3:-3] #Takes off identifier and newline straggler
        PoS_frequency.append(trimmed_line)
        for word in line:
            if word == "," and comma_present == False:
                comma_present = True
            if word == "," and comma_present == True:
                words_after_comma = 0
            if word != "," and comma_present == True:
                words_after_comma += 1
        
        if words_after_comma != 0:
            comma_length_to_end.append(words_after_comma)

    #if line[0:3] == "%: ":
        #trimmed_line = line[3:-3]
        #numpy.append(PoS_frequency_no_punctuation, line)

(unique, counts) = numpy.unique(PoS_frequency, return_counts=True)
frequencies = numpy.asarray((unique, counts)).T
#print(frequencies)

(unique, counts) = numpy.unique(comma_length_to_end, return_counts=True)
frequencies = numpy.asarray((unique, counts)).T
print(frequencies)

###---------------------------------------------------INPUT---------------------------------------------------###
def input_file(): #Takes in input file and tokenizes sentences
    text = open(os.path.join(sys.path[0], 'input.txt', 'r'))
    user_file = text.read()
    sentenceTokens = nltk.sent_tokenize(user_file)
    
    for sentence in sentenceTokens:
        words = nltk.word_tokenize(sentence)
        filtered_sentence = [w for w in words if not w in stop_words]
        stemmed_sentence = []
        for w in filtered_sentence:
            stemmed_sentence.append(ps.stem(w))
        print(stemmed_sentence)


###---------------------------------------------------GUI---------------------------------------------------###
# root = tk.Tk() #root==mainwindow
# root.title("GUI Base")
# root.geometry('500x300')

# frameFileUpload = Frame(root)

# fileInput = tk.Text(frameFileUpload, height=5, width=70)
# fileInput.pack()
# btnTrainingFile = tk.Button(frameFileUpload, text="Test With File", command=input_file)
# btnTrainingFile.pack()
# frameFileUpload.pack()

# root.mainloop()