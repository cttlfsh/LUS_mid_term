'''	
LUS mid_term project, Spring 2018
Student: Andrea Montagner, id:189514

# Simple pyhton script which split the file given as input    
# in two files, one with the words and one with the labels.   
# It was not mandatory but help keep the understanding clear  
# later on.													 
#															 
# Do not run it, it is automatically called when 'toAtuomata.py' 
# is called.                                                  

'''
train_pos = []
words = []
labels = []

with open("../data/data/NLSPARQL.train.data", "r") as f:
	train_pos = f.readlines()
	#print(train_pos)

for line in train_pos:
	if(len(line)>1):
		words.append(line.split("\t")[0])
		labels.append(line.split("\t")[1])
unique_wrd = list(set(words))
unique_lab = list(set(labels))

### Create the file of the words
with open("../text_files/words.txt", "w") as f:
	for l in unique_wrd:
		f.write(l + "\n")
	
### Create the file of the labels
with open("../text_files/labels.txt", "w") as f:
	for l in unique_lab:
		f.write(l)


	