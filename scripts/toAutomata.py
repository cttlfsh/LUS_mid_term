'''

LUS mid_term project, Spring 2018
Student: Andrea Montagner, id:189514

Main file of the project, it computes sequence labeling using words
and labels.
It start from computing the unigram probabilities and frequencies up 
unitl the bigram probabilities and frequencies, creating at the end
the automaton as 'automata.txt'
'''

from collections import Counter
import math
import sys
#import file_generator

def frequency_unigram(uni_list):
	sorted_unigr = Counter(uni_list)
	return sorted_unigr
def probability_unigram(freq_unig):
	prob_unig = []
	l = len(freq_unig)
	for word in freq_unig:
		prob_unig.append([word, freq_unig[word], (float(float(freq_unig[word])/l))])
	return prob_unig
def frequency_bigram(bi_list):
	### Map bigram elements in tuple, so I can use Counter
	### to count them
	itemDict = map(tuple, bi_list)
	return Counter(itemDict)
def probability_bigram(freq_unig, freq_bigr):
	prob_bigr = []
	for tup in freq_bigr:
		prob_bigr.append([tup, freq_bigr[tup], float(float(freq_couple[tup])/freq_IOB[tup[1]])])
	return prob_bigr 

### Lists needed to compute frequency and probabilities of dataset
sentence = []
words = []
IOB = []
word_list_final = []
IOB_list_final = []
### All necessary initializations
cut_off = []
automaton = []
remove_sentence = []
to_be_deleted = []
nbr_to_delete = []

### Input requests 
### Train file
#train_file = sys.argv[1]
### Test_file
#test_file = sys.argv[2]
### Threshold for the cut-off
#threshold = sys.argv[3]
threshold = 5

with open("../data/data/NLSPARQL.train.data", "r") as f:
	for line in f:
		if(line != "\n"):
			### Create a list of tuple (word, IOB)
 			sentence.append([line.split("\t")[0], line.split("\t")[1][:-1]])
 			### Create a list of words
 			words.append(line.split("\t")[0])
 			IOB.append(line.split("\t")[1][:-1])
 		else:
 			continue

'''
 Compute the frequency of each word.
 
 @param: freq_words is a dictionary where for each word there is the 
 		 number of occurrences.
 @param: freq_IOB is a dictionary where for each word there is the 
 		 number of occurrences.

 		 {"word":occurrences} 
 		 {"IOB":occurences}
'''
freq_words = frequency_unigram(words)
freq_IOB = frequency_unigram(IOB)
# print(freq_IOB)
# print("\n\n\n")
for el in sentence:
	if (threshold != 0):
		if (freq_words[el[0]] < threshold):
			to_be_deleted.append(el[1])
			remove_sentence.append(el)
	else:
		continue
### Count how many times an IOB needs to be
### removed
nbr_to_delete = Counter(to_be_deleted)
### Remove the cut-off IOB from the total count
for key,value in nbr_to_delete.items():
	freq_IOB[key] -= value
### Remove the cut-off from the sentence
for el in remove_sentence:
	sentence.remove(el)

'''
 Compute the frequency for each bigram

 If there is no cut-off --> sentence is the whole train file with pairs (word, IOB)
 If there is cut-off --> sentence does not contain the pair below the threshold

 @param: freq_cuple is a dictionary where there are the occurrences for each couple

 	{(word, IOB), frequency}

'''
freq_couple = frequency_bigram(sentence)

'''
 Compute the probability for each couple (word, IOB).
 @param: prob_couple is a list, where each object is in the form:

	[(word, IOB), frequency, probability]

'''
prob_couple = probability_bigram(freq_IOB, freq_couple)

'''
 Create the automaton with the probabilities
 taking care also of unknown words.

 <unk> can be of two types:
 	- if no cut-off is applied then the probability is 1/#<unk>
 	- if cut-off is applied the probability is computed over the total number
 	  of deleted concepts, meaning #deleted_concept/#total_deletion

'''
for element in prob_couple:
	automaton.append([element[0], str(-math.log(element[2]))])

for iob in freq_IOB:
	if (threshold == 0):
		automaton.append([("<unk>", iob), str(-math.log(float(1)/float(len(freq_IOB))))])
	else:
		### Find probability of each IOB and give to the <unk> the prob of 1-p(IOB)
		prob_IOB = float(freq_IOB[iob])/float(sum(val for key,val in freq_IOB.items()))
		automaton.append([("<unk>", iob), str(-math.log(1-prob_IOB))])

### Keep track of words and IOB in order to create the lexicon
for element in automaton:
	word_list_final.append(element[0][0]) 
	IOB_list_final.append(element[0][1])
word_list_final = set(word_list_final)
IOB_list_final = set(IOB_list_final)


with open("../files/words.txt", "w") as f:
	for element in word_list_final:
		f.write(element+"\n")
with open("../files/IOB.txt", "w") as f:
	for element in IOB_list_final:
		f.write(element+"\n")
with open("../files/automaton.txt", "w") as f:
	for element in automaton:
		f.write("0\t0\t"+element[0][0]+"\t"+element[0][1]+"\t"+element[1]+"\n")




