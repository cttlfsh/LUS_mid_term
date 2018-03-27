train_pos = []
words = []
labels = []

with open("P1_data/data/NLSPARQL.test.data", "r") as f:
	train_pos = f.readlines()
	#print(train_pos)

for line in train_pos:
	if(len(line)>1):
		words.append(line.split("\t")[0])
		labels.append(line.split("\t")[1])
unique_wrd = list(set(words))
unique_lab = list(set(labels))

### Create the file of the words
with open("words.txt", "w") as f:
	for l in unique_wrd:
		f.write(l + "\n")
	
### Create the file of the labels
with open("labels.txt", "w") as f:
	for l in unique_lab:
		f.write(l)


	