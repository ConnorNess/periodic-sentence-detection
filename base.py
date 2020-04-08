import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
#nltk.download()
import numpy
import os
import sys

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
comma_length_to_end = []

PoS_three_frequency = []
PoS_four_frequency = []
PoS_five_frequency = []
PoS_three_frequency_no_punctuation = []
PoS_four_frequency_no_punctuation = []
PoS_five_frequency_no_punctuation = []

for line in training_PoS_file:
    words_after_comma = 0 
    comma_present = False
    characters_length = 0

    three_words = []
    four_words = []
    five_words = []
    first_word = 0
    second_word = 1
    third_word = 2
    fourth_word = 3
    fifth_word = 4

    if line[0:3] == "#: ":
        trimmed_line = line[3:-3] #Takes off identifier and newline straggler
        sent_length = len(word_tokenize(line))
        all_words = word_tokenize(line)

        #Comma-To-End checker - Counts distance from last comma to end of sentence to calculate occurances
        for word in word_tokenize(trimmed_line):
            if word == "," and comma_present == False:
                comma_present = True
            if word == "," and comma_present == True:
                words_after_comma = 0
            if word != "," and comma_present == True:
                words_after_comma += 1

        #Fills arrays of part of speech orderings
        while fifth_word != sent_length:
            three_words = [all_words[first_word], all_words[second_word], all_words[third_word]]
            PoS_three_frequency.append(three_words)

            four_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word]]
            PoS_four_frequency.append(four_words)

            five_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word], all_words[fifth_word]]
            PoS_five_frequency.append(five_words)

            first_word += 1
            second_word += 1
            third_word += 1
            fourth_word += 1
            fifth_word += 1

        if words_after_comma != 0:
            comma_length_to_end.append(words_after_comma)

    if line[0:3] == "%: ":
        trimmed_line = line[3:-3]
        sent_length = len(word_tokenize(line))
        all_words = word_tokenize(line)
        
        for word in word_tokenize(trimmed_line):
            PoS_frequency.append(word) #Part of Speech checker - Counts each instance of parts of speech to count occurances//independant of order

        #Fills arrays of part of speech orderings
        while fifth_word != sent_length:
            three_words = [all_words[first_word], all_words[second_word], all_words[third_word]]
            PoS_three_frequency_no_punctuation.append(three_words)

            four_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word]]
            PoS_four_frequency_no_punctuation.append(four_words)

            five_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word], all_words[fifth_word]]
            PoS_five_frequency_no_punctuation.append(five_words)

            first_word += 1
            second_word += 1
            third_word += 1
            fourth_word += 1
            fifth_word += 1

###---------------------------------------------------FILLING TEST DATA---------------------------------------------------###
#WORDS AFTER COMMA OCCURANCES
(unique, counts) = numpy.unique(comma_length_to_end, return_counts=True)
comma_frequencies = numpy.asarray((unique, counts)).T
comma_frequencies = numpy.delete(comma_frequencies, numpy.where(comma_frequencies[:,1]==1),0)  #Delete single occurances

top_num_commas = numpy.array(comma_frequencies[:,1])
num_of_rows_comma = numpy.size(comma_frequencies, 0) #Number of rows == how many comma-to-end lengths there are

num_of_commas_highest_elements = 0 #Used to get the top 10% (or top 3) of comma frequency
if ((int(num_of_rows_comma/10)) < 3): #3 arbitrarilly chosen for trends in scenarios 10% of unique data is less than 3 elements, int(x) rounds down
    num_of_commas_highest_elements = 3
else:
    num_of_commas_highest_elements = (int(num_of_rows_comma/10))

num_of_commas_highest_elements_sort = num_of_commas_highest_elements * -1 #Gets indicies of max values (number chosen by num_of_commas_highest_elements)
comma_indexes = top_num_commas.argsort()[num_of_commas_highest_elements_sort:][::-1]

most_common_comma_lengths = []

top_commas = numpy.array(comma_frequencies[:,0])

i = 0
for each in comma_indexes: #Fills array with top commas as corresponding to highest value
    most_common_comma_lengths.append(top_commas[comma_indexes[i]])
    i += 1

#print(most_common_comma_lengths)


#PART OF SPEECH OCCURANCES
(unique, counts) = numpy.unique(PoS_frequency, return_counts=True)
PoS_frequencies = numpy.asarray((unique, counts)).T
PoS_frequencies = numpy.delete(PoS_frequencies, numpy.where(PoS_frequencies[:,1]=="1"),0)
top_num_PoS = numpy.array(PoS_frequencies[:,1])
num_of_rows_PoS = numpy.size(PoS_frequencies, 0)

num_of_Pos_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_highest_elements = 3
else:
    num_of_Pos_highest_elements = (int(num_of_rows_PoS/10))

num_of_Pos_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_indexes = top_num_PoS.argsort()[num_of_Pos_highest_elements_sort:][::-1]

most_common_PoS_lengths = []

top_Pos = numpy.array(PoS_frequencies[:,0])

i = 0
for each in PoS_indexes:
    most_common_PoS_lengths.append(top_Pos[PoS_indexes[i]])
    i += 1

#print(most_common_PoS_lengths)


#THREE WORDS NO PUNCTUATION OCCURANCES
(unique, counts) = numpy.unique(PoS_three_frequency_no_punctuation, return_counts=True)
PoS_three_frequencies_no_punctuation = numpy.asarray((unique, counts)).T
PoS_three_frequencies_no_punctuation = numpy.delete(PoS_three_frequencies_no_punctuation, numpy.where(PoS_three_frequencies_no_punctuation[:,1]=="1"),0)
top_num_PoS_three_frequencies_no_punctuation = numpy.array(PoS_three_frequencies_no_punctuation[:,1])
num_of_rows_PoS_three_frequencies_no_punctuation = numpy.size(PoS_three_frequencies_no_punctuation, 0)

num_of_Pos_three_frequencies_no_punctuation_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_three_frequencies_no_punctuation_highest_elements = 3
else:
    num_of_Pos_three_frequencies_no_punctuation_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_three_frequencies_no_punctuation_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_three_frequencies_no_punctuation_indexes = top_num_PoS.argsort()[num_of_PoS_three_frequencies_no_punctuation_highest_elements_sort:][::-1]

most_common_PoS_three_frequencies_no_punctuation_lengths = []

top_Pos_three_frequencies_no_punctuation = numpy.array(PoS_three_frequencies_no_punctuation[:,0])

i = 0
for each in PoS_three_frequencies_no_punctuation_indexes:
    most_common_PoS_three_frequencies_no_punctuation_lengths.append(top_Pos[PoS_three_frequencies_no_punctuation_indexes[i]])
    i += 1

#print(most_common_PoS_three_frequencies_no_punctuation_lengths)


#FOUR WORDS NO PUNCTUATION OCCURANCES
(unique, counts) = numpy.unique(PoS_four_frequency_no_punctuation, return_counts=True)
PoS_four_frequencies_no_punctuation = numpy.asarray((unique, counts)).T
PoS_four_frequencies_no_punctuation = numpy.delete(PoS_four_frequencies_no_punctuation, numpy.where(PoS_four_frequencies_no_punctuation[:,1]=="1"),0)
top_num_PoS_four_frequencies_no_punctuation = numpy.array(PoS_four_frequencies_no_punctuation[:,1])
num_of_rows_PoS_four_frequencies_no_punctuation = numpy.size(PoS_four_frequencies_no_punctuation, 0)

num_of_Pos_four_frequencies_no_punctuation_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_four_frequencies_no_punctuation_highest_elements = 3
else:
    num_of_Pos_four_frequencies_no_punctuation_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_four_frequencies_no_punctuation_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_four_frequencies_no_punctuation_indexes = top_num_PoS.argsort()[num_of_PoS_four_frequencies_no_punctuation_highest_elements_sort:][::-1]

most_common_PoS_four_frequencies_no_punctuation_lengths = []

top_Pos_four_frequencies_no_punctuation = numpy.array(PoS_four_frequencies_no_punctuation[:,0])

i = 0
for each in PoS_four_frequencies_no_punctuation_indexes:
    most_common_PoS_four_frequencies_no_punctuation_lengths.append(top_Pos[PoS_four_frequencies_no_punctuation_indexes[i]])
    i += 1

#print(most_common_PoS_four_frequencies_no_punctuation_lengths)


#FIVE WORDS NO PUNCTUATION OCCURANCES
(unique, counts) = numpy.unique(PoS_five_frequency_no_punctuation, return_counts=True)
PoS_five_frequencies_no_punctuation = numpy.asarray((unique, counts)).T
PoS_five_frequencies_no_punctuation = numpy.delete(PoS_five_frequencies_no_punctuation, numpy.where(PoS_five_frequencies_no_punctuation[:,1]=="1"),0)
top_num_PoS_five_frequencies_no_punctuation = numpy.array(PoS_five_frequencies_no_punctuation[:,1])
num_of_rows_PoS_five_frequencies_no_punctuation = numpy.size(PoS_five_frequencies_no_punctuation, 0)

num_of_Pos_five_frequencies_no_punctuation_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_five_frequencies_no_punctuation_highest_elements = 3
else:
    num_of_Pos_five_frequencies_no_punctuation_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_five_frequencies_no_punctuation_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_five_frequencies_no_punctuation_indexes = top_num_PoS.argsort()[num_of_PoS_five_frequencies_no_punctuation_highest_elements_sort:][::-1]

most_common_PoS_five_frequencies_no_punctuation_lengths = []

top_Pos_five_frequencies_no_punctuation = numpy.array(PoS_five_frequencies_no_punctuation[:,0])

i = 0
for each in PoS_five_frequencies_no_punctuation_indexes:
    most_common_PoS_five_frequencies_no_punctuation_lengths.append(top_Pos[PoS_five_frequencies_no_punctuation_indexes[i]])
    i += 1

#print(most_common_PoS_five_frequencies_no_punctuation_lengths)


#THREE WORDS OCCURANCES
(unique, counts) = numpy.unique(PoS_three_frequency, return_counts=True)
PoS_three_frequencies = numpy.asarray((unique, counts)).T
PoS_three_frequencies = numpy.delete(PoS_three_frequencies, numpy.where(PoS_three_frequencies[:,1]=="1"),0)
top_num_PoS_three_frequencies = numpy.array(PoS_three_frequencies[:,1])
num_of_rows_PoS_three_frequencies = numpy.size(PoS_three_frequencies, 0)

num_of_Pos_three_frequencies_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_three_frequencies_highest_elements = 3
else:
    num_of_Pos_three_frequencies_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_three_frequencies_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_three_frequencies_indexes = top_num_PoS.argsort()[num_of_PoS_three_frequencies_highest_elements_sort:][::-1]

most_common_PoS_three_frequencies_lengths = []

top_Pos_three_frequencies = numpy.array(PoS_three_frequencies[:,0])

i = 0
for each in PoS_three_frequencies_indexes:
    most_common_PoS_three_frequencies_lengths.append(top_Pos[PoS_three_frequencies_indexes[i]])
    i += 1

#print(most_common_PoS_three_frequencies_lengths)


#FOUR WORDS OCCURANCES
(unique, counts) = numpy.unique(PoS_four_frequency, return_counts=True)
PoS_four_frequencies = numpy.asarray((unique, counts)).T
PoS_four_frequencies = numpy.delete(PoS_four_frequencies, numpy.where(PoS_four_frequencies[:,1]=="1"),0)
top_num_PoS_four_frequencies = numpy.array(PoS_four_frequencies[:,1])
num_of_rows_PoS_four_frequencies = numpy.size(PoS_four_frequencies, 0)

num_of_Pos_four_frequencies_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_four_frequencies_highest_elements = 3
else:
    num_of_Pos_four_frequencies_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_four_frequencies_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_four_frequencies_indexes = top_num_PoS.argsort()[num_of_PoS_four_frequencies_highest_elements_sort:][::-1]

most_common_PoS_four_frequencies_lengths = []

top_Pos_four_frequencies = numpy.array(PoS_four_frequencies[:,0])

i = 0
for each in PoS_four_frequencies_indexes:
    most_common_PoS_four_frequencies_lengths.append(top_Pos[PoS_four_frequencies_indexes[i]])
    i += 1

#print(most_common_PoS_four_frequencies_lengths)


#FIVE WORDS OCCURANCES
(unique, counts) = numpy.unique(PoS_five_frequency, return_counts=True)
PoS_five_frequencies = numpy.asarray((unique, counts)).T
PoS_five_frequencies = numpy.delete(PoS_five_frequencies, numpy.where(PoS_five_frequencies[:,1]=="1"),0)
top_num_PoS_five_frequencies = numpy.array(PoS_five_frequencies[:,1])
num_of_rows_PoS_five_frequencies = numpy.size(PoS_five_frequencies, 0)

num_of_Pos_five_frequencies_highest_elements = 0 
if ((int(num_of_rows_PoS/10)) < 3):
    num_of_Pos_five_frequencies_highest_elements = 3
else:
    num_of_Pos_five_frequencies_highest_elements = (int(num_of_rows_PoS/10))

num_of_PoS_five_frequencies_highest_elements_sort = num_of_Pos_highest_elements * -1
PoS_five_frequencies_indexes = top_num_PoS.argsort()[num_of_PoS_five_frequencies_highest_elements_sort:][::-1]

most_common_PoS_five_frequencies_lengths = []

top_Pos_five_frequencies = numpy.array(PoS_five_frequencies[:,0])

i = 0
for each in PoS_five_frequencies_indexes:
    most_common_PoS_five_frequencies_lengths.append(top_Pos[PoS_five_frequencies_indexes[i]])
    i += 1

#print(most_common_PoS_five_frequencies_lengths)

###---------------------------------------------------INPUT---------------------------------------------------###
text = open(os.path.join(sys.path[0], 'input.txt'), 'r')
user_file = text.read()
sentenceTokens = nltk.sent_tokenize(user_file)

sent_PoS_three_frequency = []
sent_PoS_four_frequency = []
sent_PoS_five_frequency = []
sent_PoS_three_frequency_no_punctuation = []
sent_PoS_four_frequency_no_punctuation = []
sent_PoS_five_frequency_no_punctuation = []

for sentence in sentenceTokens:
    word_counter = 0
    sentencePoS = ""
    sentencePoS_no_punctuation = ""
    comma_present = False
    words_after_comma = 0 

    words = nltk.word_tokenize(sentence)
    filtered_sentence = [w for w in words if not w in stop_words]
    tagged_sentence = nltk.pos_tag(filtered_sentence)

    three_words = []
    four_words = []
    five_words = []
    three_words_no_punctuation = []
    four_words_no_punctuation = []
    five_words_no_punctuation = []
    first_word = 0
    second_word = 1
    third_word = 2
    fourth_word = 3
    fifth_word = 4
    sent_length = len(word_tokenize(line))
    all_words = word_tokenize(line)
    all_words_no_punctuation = punctuationremover.tokenize(line)

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

    print(sentence)
    #Comma test
    if (comma_present == True):
        for each in most_common_comma_lengths:
            if (words_after_comma == each):
                print("Passes comma test")
    
    #Fill order arrays for testing
    while fifth_word != sent_length:
        three_words = [all_words[first_word], all_words[second_word], all_words[third_word]]
        sent_PoS_three_frequency.append(three_words)

        four_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word]]
        sent_PoS_four_frequency.append(four_words)

        five_words = [all_words[first_word], all_words[second_word], all_words[third_word], all_words[fourth_word], all_words[fifth_word]]
        sent_PoS_five_frequency.append(five_words)

        first_word += 1
        second_word += 1
        third_word += 1
        fourth_word += 1
        fifth_word += 1

    #Punctuation Tests
    #3 words
    three_passes = 0
    for each in most_common_PoS_three_frequencies_lengths:
        for orders in sent_PoS_three_frequency:
            if orders == each:
                three_passes += 1
    print("3 PoS Similarities: " + str(three_passes))

    four_passes = 0
    #4 words
    for each in most_common_PoS_four_frequencies_lengths:
        for orders in sent_PoS_four_frequency:
            if orders == each:
                four_passes += 1
    print("4 PoS Similarities: " + str(four_passes))

    five_passes = 0
    #5 words
    for each in most_common_PoS_five_frequencies_lengths:
        for orders in sent_PoS_five_frequency:
            if orders == each:
                five_passes += 1
    print("5 PoS Similarities: " + str(five_passes))

    #Non-Punctuation Tests
    #3 words
    three_passes_no_punctuation = 0
    for each in most_common_PoS_five_frequencies_no_punctuation_lengths:
        for orders in sent_PoS_five_frequency:
            if orders == each:
                three_passes_no_punctuation += 1
    print("3 PoS Similarities (No punctuation): " + str(three_passes_no_punctuation))

    four_passes_no_punctuation = 0
    #4 words
    for each in most_common_PoS_five_frequencies_no_punctuation_lengths:
        for orders in sent_PoS_five_frequency:
            if orders == each:
                four_passes_no_punctuation += 1
    print("4 PoS Similarities (No punctuation): " + str(four_passes_no_punctuation))

    five_passes_no_punctuation = 0
    #5 words
    for each in most_common_PoS_five_frequencies_no_punctuation_lengths:
        for orders in sent_PoS_five_frequency:
            if orders == each:
                five_passes_no_punctuation += 1
    print("5 PoS Similarities (No punctuation): " + str(five_passes_no_punctuation))
    
    #Calculate chances of being periodic

    #Output sentences