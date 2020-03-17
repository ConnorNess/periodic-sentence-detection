import tkinter as tk 
from tkinter import *
from tkinter import messagebox
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()
import os

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

###---------------------------------------------------TRAINING---------------------------------------------------###
training_file = open(os.path.join(sys.path[0],'TrainingBase.txt'))
train_file = training_file.read()

if os.path.exists(os.path.join('TrainingCleaned.txt')): #Deleting and remaking cleaned training data
    os.remove(os.path.join(sys.path[0],'TrainingCleaned.txt'))
cleantrain_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'w') 

sentenceTraining = nltk.sent_tokenize(train_file)
punctuationremover = RegexpTokenizer(r'\w+')

part_of_speech_trends = []
#TODO add tokenizer which includes punctuation, could also be a trend
for sentence in sentenceTraining:
    sentencePoS = ""
    wordCounter = 0

    words = punctuationremover.tokenize(sentence)
    filtered_trainer = [w for w in words if not w in stop_words] #Takes out punctuation then stop words from each sentence
    tagged_sentence_trainer = nltk.pos_tag(filtered_trainer)

    for word in filtered_trainer: #stems each word in sentence and writes each sentence to a new line
        cleantrain_file.write(ps.stem(word))
        cleantrain_file.write(" ")
        sentencePoS += (tagged_sentence_trainer[wordCounter][1])
        sentencePoS += " "
        wordCounter += 1
    cleantrain_file.write("\n")
    
    cleantrain_file.write(sentencePoS)
    cleantrain_file.write("\n")
    
cleantrain_file.close()

training_PoS_Tags = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'r')
train_PoS_frequency = []


# for line in training_PoS_Tags:
#     word_count = len(line.split())
#     print(word_count)
#     current_word = 1
#     main_clause_position = round(((len(line.split())/100)*31.4))
    
#     for word in line.split():
#         if current_word >  main_clause_position:
#             train_PoS_frequency = [nltk.pos_tag(word)]
#     print(train_PoS_frequency)

#training_tag_rate = nltk.FreqDist(tag for (word, tag) in )



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