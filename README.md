# Development of a Spoken Language Understanding module 

Student: Andrea Montagner  
ID:189514

Spring 2018

This is the mid-term project of the Language Understanding System course, the aim is to develop o Spoken Language Understanding module for the Movie Domain capable of performing PoS tagging.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To succesfully run the project you need to download two external tool:  
   
* OpenFST library, see [OpenFST](http://www.openfst.org/twiki/bin/view/FST/WebHome)
* OpenGrm Ngrm library [OpenNgrm](http://www.opengrm.org)


### Make the project run

Different approaches have been implemented, to run them:  

* Move to the /src folder from terminal 
```
cd src
```

* Choose which approach to run between word2IOB, w2IOB_without_O and lemma2IOB and launch the respective script
```
./<method_name>.sh  -- <method_name> from word2IOB, w2IOB_without_O, lemma2IOB
```

* The bash script will perform all necessary actions, results are stored in:

```
/src/<method_name>/results/evaluations
```

## Deployment

* Base Project: 
  * word2IOB  
   First part of the project, used as baseline for the others. Main operations are:  
   
    * Creation of necessary files, like lexicon, automaton performed by the W2IOB_processor.py script. Files are in:

```
/src/<method_name>/files  
```
  
   * Compute the likelihood, also performed by the python script
using the training set,
    * Train the WFST and the LM,taking care about unknown words and with the possibility of using a frequency cut-off on the likelihood,
    * Evaluate the trained model on the provided test set.

  * w2IOB_without_O  
   First part of the project, where 'O' tags are generalized in the train phase. Main operations are:  
   
    * Creation of necessary files, like lexicon, automaton performed by the W2IOB_processor_without_O.py script. Files are in:
```
/src/<method_name>/files
```
 
    * Compute the likelihood, also performed by the python script
using the training set,
    * Train the WFST and the LM,taking care about unknown words and with the possibility of using a frequency cut-off on the likelihood,
    * Evaluate the trained model on the provided test set.

  * lemma2IOB  
   Last try of the project, useds lemmas instead of words. Main operations are:  
   
    * Creation of necessary files, like lexicon, automaton performed by the Lemma2IOB_processor.py script. Files are in:
```
/src/<method_name>/files
```
  
    * Compute the likelihood, also performed by the python script
using the training set,
    * Train the WFST and the LM,taking care about unknown words and with the possibility of using a frequency cut-off on the likelihood,
    * Evaluate the trained model on the provided test set.

## Authors

* **Andrea Montagner** 

