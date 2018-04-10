#################################################################################################
#																								#
#										INSTRUCTIONS 											#
#																								#
#	this script is the main script of the baseline project, to launch it, use ./word2IOB.sh 	#
#	with the following parameters:   															#
#																								#
#																								#
#	@param $TRAIN_FILE the training file 														#
#	@param $TEST_FILE the testing file 															#
#	@param $threshold the cut-off threshold to apply 											#
#																								#	
#																								#
#	The script will generate all necessary files/directories and perform both training and 		#
#	testing for all possible smoothing methods and ngram order 									#
#																								#
#																								#
#################################################################################################

#!/bin/bash

TRAIN_FILE="../data/data/NLSPARQL.train.data" #$1
TEST_FILE="../data/data/NLSPARQL.test.data" #$2
METHOD_LIST="methods_list.txt"
threshold=$1

if [[ "$threshold" = "0" ]]; then
	#statements
	folder="w2IOB_without_O"
else
	folder="w2IOB_without_O_cutoff"
fi
### Creates folders to store important files
mkdir $folder
mkdir "$folder"/results
mkdir "$folder/results"/evaluations
mkdir "$folder/results"/predictions
mkdir "$folder"/files
mkdir "$folder"/methods
### Call the python script which outputs necessary
### .txt files
python scripts/W2IOB_processor_without_O.py $threshold

LEXICON=$folder"/files/lexicon.txt"
AUTOMATON=$folder"/files/automaton.txt"
TRAIN_IOB=$folder"/files/train_IOB_by_sentence.txt"
TEST_SENTENCE=$folder"/files/test_words_by_sentence.txt"
MAX_NGRAM_ORDER=5

counter=0

### Generates the transducer
fstcompile --isymbols=$LEXICON --osymbols=$LEXICON $AUTOMATON > $folder/word2IOB.fst
farcompilestrings --symbols=$LEXICON --unknown_symbol='<unk>' $TRAIN_IOB > $folder/train_IOBs.far
### Perform the testing for each possible smoothing method and for each ngram order
while read -r method
do
	mkdir "$folder/methods"/$method
	for i in $(seq 1 $MAX_NGRAM_ORDER)
	do
		echo "Method: $method - Ngram_order: $i"
		echo "Processing..."
		mkdir "$folder/methods/$method"/ngramOrder$i
		ngramcount --order=$i --require_symbols=false $folder/train_IOBs.far > $folder/methods/$method/ngramOrder$i/train_IOBs.cnt
		ngrammake --method=$method $folder/methods/$method/ngramOrder$i/train_IOBs.cnt > $folder/methods/$method/ngramOrder$i/language_model.lm
		### Iterate on all test sentences
		while read -r line
		do
			echo $line | farcompilestrings --symbols=$LEXICON --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst' 		
			fstcompose 1.fst $folder/word2IOB.fst | fstcompose - $folder/methods/$method/ngramOrder$i/language_model.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=$LEXICON --osymbols=$LEXICON >> $folder/methods/$method/ngramOrder$i/automa.txt
			# if [[ counter == 271 ]]; then
			# 	echo "Status: 25%"
			# else if [[ counter == 542 ]]; then
			# 	echo "Status: 50%"
			# else if [[ counter == 813 ]]; then
			# 	echo "Status: 75%"
			# fi
			 ((counter++))
			echo "Processed the $counter line: $line"
		done < $TEST_SENTENCE

		awk '{print $4}' < $folder/methods/$method/ngramOrder$i/automa.txt | awk -v RS= -v ORS="\n\n" "1" > tmp_output.txt

		python scripts/cleaner.py tmp_output.txt

		paste $TEST_FILE new_tmp_output.txt > "$folder/results/predictions"/prediciton_$method"_ngramOrder"$i.txt
		### Launch the script to perform the evaluation
		perl ../data/scripts/conlleval.pl -d "\t" < "$folder/results/predictions"/prediciton_$method"_ngramOrder"$i.txt > "$folder/results/evaluations"/evaluation_$method"_ngramOrder"$i.txt
		#echo "Status: 100%"
		echo "Ngram_order: $i done"
		((counter = 0))
	done 
	echo "Method: $method done"
done < $METHOD_LIST
echo "Everything has been processed. Evalutations are in $folder/results/evalutations and visual results are in $folder/results/predictions"
echo "Cleaning useless files"
rm 1.fst
rm tmp_output.txt
rm new_tmp_output.txt
echo 'Done! Program finished successfully!'
