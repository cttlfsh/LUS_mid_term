from collections import Counter
import math
import lexicon

def frequency_unigram(uni_list):
	sorted_unigr = Counter(uni_list)
	return sorted_unigr
def probability_unigram(prob_unig, freq_unig):
	l = len(freq_unig)
	for word in freq_unig:
		prob_unig.append([word, freq_unig[word], (float(float(freq_unig[word])/l))])
	return prob_unig
def frequency_bigram(bi_list):
	### Map bigram elements in tuple, so I can use Counter
	### to count them
	itemDict = map(tuple, bi_list)
	return Counter(itemDict)
def probability_bigram(freq_unig, prob_bigr, freq_bigr):
	for tup in freq_bigr:
		if tup[0] in freq_unig:
			prob_bigr.append([tup, freq_bigr[tup], float(float(freqB[tup])/freqU[tup[1]])])
	return prob_bigr
	pass 

### Lists needed to compute frequency and probabilities of datset
sentence = []
unigrams = []
probU = []
probB = []
bigrams = []


labels_list = []

with open("P1_data/data/NLSPARQL.test.data", "r") as f:
	for line in f:
 		sentence.append(line)
 		### list[-1] prende l'ultimo inserito
 		for word in sentence[-1].split():
 			unigrams.append(word)
### Compute the frequency of each unigram ###
freqU = frequency_unigram(unigrams)
### Compute the probability of each unigram ###
probU = probability_unigram(probU, freqU)

###									  ###
###  Now lets do the same for bigrams ###
###									  ###

length = len(sentence)
i = 0
while i < length - 1:
	### Bigram list filled
	bigrams.append([unigrams[i], unigrams[i+1]])
	i = i + 2
### Compute the frequency for each bigram
freqB = frequency_bigram(bigrams)
### Compute the probability for each bigram
probB = probability_bigram(freqU, probB, freqB)

### Create the graph with the probabilities
### taking care also of unknown words
with open("automa.txt", "w") as f:
	for element in probB:
		if (element[0][1] not in labels_list):
			labels_list.append(element[0][1])
		f.write("0\t0\t"+element[0][0]+"\t"+element[0][1]+"\t"+str(-math.log(element[2]))+"\n")
	for elements in labels_list:
		f.write("0\t0\t<unk>\t"+ elements +"\t"+str(-math.log(float(1)/float(len(labels_list)))) + "\n")




