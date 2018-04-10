from collections import Counter
import sys

feats_file = "../data/data/NLSPARQL.train.feats.txt"
postag_file = sys.argv[1] #"additional_material/additional_features/train_PoSTags.txt"
lemma_file = sys.argv[2] #"additional_material/additional_features/train_lemmas.txt"

words = []
PoSTags = []
lemmas = []

with open(feats_file, "r") as f:
	for line in f:
		if (line != '\n'):
			PoSTags.append(line.split("\t")[1])
			lemmas.append(line.split("\t")[2][:-1])
		else:
			PoSTags.append('\n')
			lemmas.append('\n')

uniq_lem = Counter(lemmas)
sort = uniq_lem.most_common()
print(sort)

with open(postag_file, "w") as f:
	for line in PoSTags:
		if (line != '\n'):
			f.write(str(line)+"\n")
		else:
			f.write("\n")
with open(lemma_file, "w") as f:
	for line in lemmas:
		if (line != '\n'):
			f.write(str(line)+"\n")
		else:
			f.write("\n")