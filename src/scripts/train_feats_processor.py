
feats_file = "../data/data/NLSPARQL.train.feats.txt"
postag_file = "additional_features/train_PoSTags.txt"
lemma_file = "additional_features/train_lemmas.txt"

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

with open(postag_file, "w") as f:
	for line in PoSTags:
		f.write(str(line)+"\n")
with open(lemma_file, "w") as f:
	for line in lemmas:
		f.write(str(line)+"\n")