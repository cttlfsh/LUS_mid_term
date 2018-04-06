#################################################################################################
#																								#
#										INSTRUCTIONS 											#
#																								#
#	this script is the main script of the baseline project, to launch it, use ./word2IOB.sh 	#
#	with the following parameters:   															#
#																								#
#																								#
#	@param train_file the training file 														#
#	@param test_file the testing file 															#
#	@param threshold the cut-off threshold to apply 											#
#																								#	
#																								#
#	The script will generate all necessary files/directories and perform both training and 		#
#	testing for all possible smoothing methods and ngram order 									#
#																								#
#																								#
#################################################################################################

#!/bin/bash

train_file="../data/data/NLSPARQL.train.data" #$1
test_file="../data/data/NLSPARQL.test.data" #$2
threshold=0 #$3
method_list="methods_list.txt"

if [[ "$threshold" = "0" ]]; then
	#statements
	folder="Lemma2IOB_without_O_no_cutoff"
else
	folder="Lemma2IOB_without_O_cutoff"
fi
### Creates folders to store important files
mkdir $folder

mkdir "$folder"/files
#mkdir "$folder"/methods
### Call the python script which outputs necessary
### .txt files
python scripts/Lemma2IOB_processor.py $threshold 

lexicon=$folder"/files/lexicon.txt"
automaton=$folder"/files/automaton.txt"
train_IOB=$folder"/files/train_IOB_by_sentence.txt"
test_sentence=$folder"/files/test_words_by_sentence.txt"
max_ngram_order=5

counter=0

### Generates the transducer
fstcompile --isymbols=$lexicon --osymbols=$lexicon $automaton > $folder/word2IOB.fst
farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' $train_IOB > $folder/train_IOBs.far
### Perform the testing for each possible smoothing method and for each ngram order
ngramcount --order=3 --require_symbols=false $folder/train_IOBs.far > $folder/train_IOBs.cnt
ngrammake --method=witten_bell $folder/train_IOBs.cnt > $folder/language_model.lm
### Iterate on all test sentences
while read -r line
do
	echo $line | farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst' 		
	fstcompose 1.fst $folder/word2IOB.fst | fstcompose - $folder/language_model.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=$lexicon --osymbols=$lexicon >> $folder/automa.txt
	#echo " " >> $folder/automa.txt
	((counter++))
	echo "Processed the $counter line: $line"
done < $test_sentence
### 
awk '{print $4}' < $folder/automa.txt | awk -v RS= -v ORS="\n\n" "1" > tmp_output.txt

#python scripts/cleaner.py tmp_output.txt

paste $test_file tmp_output.txt > "$folder"/results.txt
### Launch the script to perform the evaluation
perl ../data/scripts/conlleval.pl -d "\t" < "$folder/"results.txt > "$folder"/evaluation.txt