# Language Understanding System: mid-term project

Student: Andrea Montagner  
ID:189514

Spring 2018


### DESCRIPTION
              
* Base Project: 
  * Words_IOB  
   First part of the project, used as baseline for the others. Main operations are:  
   
    * Create the lexicon,
    * Compute the likelihoods with one of the implementation proposed 
using the training set,
    * Train the WFST and the LM (generated using opengram),taking care about unknown words and with the possibility of using a frequency cut-off on the likelihood,
    * Evaluate the trained model on the provided test set.
  
  * TODO: Lemma_IOB, POSTAG_IOB
  
### HOW TO USE

Do not move or modify any file. 

To run the code:
	* Navigate to the /src folder
	* Choose which approach to run
		* Word to IOB
		*
	* run the respective bash script as:
		*name_of_the script*.sh *threshold*
	* The script will take care of everything, from the creation of the lexicon to the evaluation of the results
