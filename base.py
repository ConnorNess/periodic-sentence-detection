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

if os.path.exists(os.path.join('TrainingCleaned.txt')): #Deleting and remaking cleaned training data
    os.remove(os.path.join(sys.path[0],'TrainingCleaned.txt'))
cleantrain_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'w') 

sentenceTraining = nltk.sent_tokenize(train_file)
train_pos = [] #Part-of-Speech base check build from training
stemmed_train = []

for sentence in sentenceTraining:
    words = nltk.word_tokenize(sentence)
    filtered_train = [w for w in words if not w in stop_words] #Adds token words provided they are not stop words
    
    for word in filtered_train: #stems each word in sentence and writes each sentence to a new line
        cleantrain_file.write(ps.stem(word))
        cleantrain_file.write(" ")
    cleantrain_file.write("\n")
cleantrain_file.close()

# training_PoS_Tags = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'r')
# train_PoS_frequency = []



# for line in training_PoS_Tags:
#     word_count = len(line.split())
#     print(word_count)
#     current_word = 1
#     main_clause_position = round(((len(line.split())/100)*31.4))
    
#     for word in line.split():
#         if current_word >  main_clause_position:
#             train_PoS_frequency = [nltk.pos_tag(word)]
#     print(train_PoS_frequency)

training_tag_rate = nltk.FreqDist(tag for (word, tag) in )

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