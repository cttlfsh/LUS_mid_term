#!/bin/bash

# train_file=$1
# test_file=$1
# threshold=$3
lexicon="../files/lexicon.txt"
automaton="../files/automaton.txt"
IOB_sentenced="../files/train_IOB_by_sentence.txt "
ngram_order=3

counter=0

### Call the python script which outputs the necessary
### .txt files
#python toAutomata.py $train_file $test_file $threshold 

### Generates the transducer
fstcompile --isymbols=$lexicon --osymbols=$lexicon $automaton > ../files/transducer.fst
farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' $IOB_sentenced > ../files/tagged_sentences.far

while read -r line
	do
		ngramcount --order=$ngram_order --require_symbols=false ../files/tagged_sentences.far > ../files/tagged_sentences.cnt
		ngrammake --method=absolute ../files/tagged_sentences.cnt > ../files/tagged_sentences.lm
		echo "$line" | farcompilestrings --symbols=$lexicon --unknown_symbol='<unk>' --generate_keys=1 --keep_symbols | farextract --filename_suffix='.fst' > tmp.txt 
		fstcompose 1.fst ../files/transducer.fst | fstcompose - ../files/tagged_sentences.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=$lexicon --osymbols=$lexicon >> ../files/w_IOB_absolute.txt

        ((counter++))
        echo "Processed the $counter line: $line "
    done < ../files/test_words_by_sentence.txt

    awk '{print $4}' < ../files/w_IOB_absolute.txt  | awk -v RS= -v ORS="\n\n" "1" > ../files/tmp.txt
    paste ../data/data/NLSPARQL.test.data ../files/tmp.txt > ../files/final.txt
    #perl ../data/scripts/conlleval.pl -d "\t" < ../files/final.txt > ../files/evaluation.txt
