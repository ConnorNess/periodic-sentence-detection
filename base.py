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
lines_seen = set() #Checking for duplicate lines

if os.path.exists(os.path.join('TrainingCleaned.txt')): #Deleting and remaking cleaned training data
    os.remove(os.path.join(sys.path[0],'TrainingCleaned.txt'))
cleantrain_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'w') 

sentenceTraining = nltk.sent_tokenize(train_file)
punctuationremover = RegexpTokenizer(r'\w+')

for sentence in sentenceTraining:
    if sentence not in lines_seen:
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
        lines_seen.add(sentence)
    
cleantrain_file.close()

###---------------------------------------------------TRAINING---------------------------------------------------###
training_PoS_file = open(os.path.join(sys.path[0],'TrainingCleaned.txt'), 'r')
PoS_frequency = []
#PoS_frequency_no_punctuation = numpy.array([])
comma_length_to_end = []
PoS_order_frequency = []

tree_array = []
tree_array_no_punctuation = []

for line in training_PoS_file:
    words_after_comma = 0 
    word_counter = 1
    comma_present = False
    characters_length = 0

    if line[0:3] == "#: ":
        trimmed_line = line[3:-3] #Takes off identifier and newline straggler
        sentence_length = len(trimmed_line.split())

        #Comma-To-End checker - Counts distance from last comma to end of sentence to calculate occurances
        for word in word_tokenize(trimmed_line):
            if word == "," and comma_present == False:
                comma_present = True
            if word == "," and comma_present == True:
                words_after_comma = 0
            if word != "," and comma_present == True:
                words_after_comma += 1

            #if ((sentence_length - word_counter) >= 3): #Trends can't really be one or two elements long can they tho
            PoS_order_frequency.append(trimmed_line[characters_length:]) #Checks frequencies of orders of parts of speech

            characters_length += len(word) 
            characters_length += 1 #For spaces

            word_counter += 1

        if words_after_comma != 0:
            comma_length_to_end.append(words_after_comma)

    if line[0:3] == "%: ":
        trimmed_line = line[3:-3]
        
        for word in word_tokenize(trimmed_line):
            PoS_frequency.append(word) #Part of Speech checker - Counts each instance of parts of speech to count occurances//independant of order


###---------------------------------------------------FILLING TEST DATA---------------------------------------------------###
#How many words after comma frequency
(unique, counts) = numpy.unique(comma_length_to_end, return_counts=True)
comma_frequencies = numpy.asarray((unique, counts)).T
#print(comma_frequencies[:,0]) #https://stackoverflow.com/questions/4455076/how-to-access-the-ith-column-of-a-numpy-multidimensional-array
top_num_commas = numpy.array(comma_frequencies[:,1])
num_of_rows_comma = numpy.size(comma_frequencies, 0) #Number of rows == how many comma-to-end lengths there are

num_of_commas_highest_elements = 0 #Used to get the top 10% (or top 3) of comma frequency
if ((int(num_of_rows_comma/10)) < 3): #3 arbitrarilly chosen for trends in scenarios 10% of unique data is less than 3 elements, int(x) rounds down
    num_of_commas_highest_elements = 3
else:
    num_of_commas_highest_elements = (int(num_of_rows_comma/10))

num_of_commas_highest_elements_sort = num_of_commas_highest_elements * -1
comma_indexes = top_num_commas.argsort()[num_of_commas_highest_elements_sort:][::-1] #https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array#comment67430875_6910672

most_common_comma_lengths = []

top_commas = numpy.array(comma_frequencies[:,0])

i = 0
for each in comma_indexes: #Fills array with top commas as corresponding to highest value
    most_common_comma_lengths.append(top_commas[comma_indexes[i]])
    i += 1

#print(most_common_comma_lengths)


#Checks part of speech frequencies and occurances
(unique, counts) = numpy.unique(PoS_frequency, return_counts=True)
PoS_frequencies = numpy.asarray((unique, counts)).T
top_num_PoS = numpy.array(PoS_frequencies[:,1])
num_of_rows_PoS = numpy.size(PoS_frequencies, 0) #Number of rows == how many PoS-to-end lengths there are

num_of_Pos_highest_elements = 0 #Used to get the top 10% (or top 3) of PoS frequency
if ((int(num_of_rows_PoS/10)) < 3): #3 arbitrarilly chosen for trends in scenarios 10% of unique data is less than 3 elements, int(x) rounds down
    num_of_Pos_highest_elements = 3
else:
    num_of_Pos_highest_elements = (int(num_of_rows_PoS/10))

num_of_Pos_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_indexes = top_num_PoS.argsort()[num_of_Pos_highest_elements_sort:][::-1] #https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array#comment67430875_6910672

most_common_PoS_lengths = []

top_Pos = numpy.array(PoS_frequencies[:,0])

i = 0
for each in PoS_indexes: #Fills array with top Pos as corresponding to highest value
    most_common_PoS_lengths.append(top_Pos[PoS_indexes[i]])
    i += 1

#print(most_common_PoS_lengths)


#Order of PoS ordered frequency
(unique, counts) = numpy.unique(PoS_order_frequency, return_counts=True)
PoS_ordered_frequencies = numpy.asarray((unique, counts)).T
top_num_PoS_ordered = numpy.array(PoS_ordered_frequencies[:,1])
num_of_rows_PoS_ordered = numpy.size(PoS_ordered_frequencies, 0) #Number of rows == how many PoS_ordered-to-end lengths there are

num_of_PoS_ordereds_highest_elements = 0 #Used to get the top 10% (or top 3) of PoS_ordered frequency
if ((int(num_of_rows_PoS_ordered/10)) < 3): #3 arbitrarilly chosen for trends in scenarios 10% of unique data is less than 3 elements, int(x) rounds down
    num_of_PoS_ordereds_highest_elements = 3
else:
    num_of_PoS_ordereds_highest_elements = (int(num_of_rows_PoS_ordered/10))

num_of_PoS_ordereds_highest_elements_sort = num_of_PoS_ordereds_highest_elements * -1
PoS_ordered_indexes = top_num_PoS_ordered.argsort()[num_of_PoS_ordereds_highest_elements_sort:][::-1] #https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array#comment67430875_6910672

most_common_PoS_ordered_lengths = []

top_PoS_ordereds = numpy.array(PoS_ordered_frequencies[:,0])

i = 0
for each in PoS_ordered_indexes: #Fills array with top PoS_ordereds as corresponding to highest value
    most_common_PoS_ordered_lengths.append(top_PoS_ordereds[PoS_ordered_indexes[i]])
    i += 1

#print(most_common_PoS_ordered_lengths)

###---------------------------------------------------INPUT---------------------------------------------------###
text = open(os.path.join(sys.path[0], 'input.txt'), 'r')
user_file = text.read()
sentenceTokens = nltk.sent_tokenize(user_file)
    
for sentence in sentenceTokens:
    word_counter = 0
    sentencePoS = ""
    sentencePoS_no_punctuation = ""
    comma_present = False
    words_after_comma = 0 

    words = nltk.word_tokenize(sentence)
    filtered_sentence = [w for w in words if not w in stop_words]
    tagged_sentence = nltk.pos_tag(filtered_sentence)

    for word in filtered_sentence:
        sentencePoS += (tagged_sentence_trainer[word_counter][1])
        sentencePoS += " "

        if punctuationremover.tokenize(word):
            sentencePoS_no_punctuation += (tagged_sentence_trainer[word_counter][1])
            sentencePoS_no_punctuation += " "

        word_counter += 1

        #Comma-To-End checker - Counts distance from last comma to end of sentence to calculate occurances
        if word == "," and comma_present == False:
            comma_present = True
        if word == "," and comma_present == True:
            words_after_comma = 0
        if word != "," and comma_present == True:
            words_after_comma += 1
    
    #Comma test
    for commma_indexes in comma_frequencies[:,0]:
        if (words_after_comma == commma_indexes):
            print(sentence + " Passes comma test!")



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