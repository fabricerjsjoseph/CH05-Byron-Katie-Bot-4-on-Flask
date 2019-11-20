
# CATEGORY A & B STATEMENTS ONLY:
#(1) Descriptive: x=y where x/y represents the self and/or other and the operator describing the relationship
#(2) Self & Other relationship: (i) Self & Self (ii) Self & Other (iii) Other & Other
#(3) Begin and end with a proper noun and/or pronoun.



# Turnaround Three - Generate opposite of statement
def turnaround_three_generator(user_statement):
    
    # import required libaries
    import spacy
    import contractions
    import pyinflect

    # Create an nlp object
    nlp=spacy.load('en')

    # Disable NER in nlp pipeline
    with nlp.disable_pipes('ner'):

        
        # Create a Spacy Document to parse
        doc=nlp(contractions.fix(user_statement))

        # Create a list of tokens from document i.e tokenize words
        # Expanding english language contractions
        token_list=[token.text for token in doc]
            

        try:

            # Create a list of indices for the verbs present in the token_list
            verb_index=[str(token.i) for token in doc if token.pos_ in ['VERB','AUX']]
            
            # Create list of plural pronoun ( including "I")
            sing_pronoun_list=['I','They','We']
            
            # If sentence does not have 'not', insert 'not' after 1st verb
            if token_list.count('not')==0:
                insert_at_index=int(verb_index[0])
                
                
                # CATEGORY B STATEMENTS
                
                if doc[1].lemma_=='be':
                    token_list.insert(2,'not')
                    
                    
                
                
                # CATEGORY A STATEMENTS 
                else:
                    
                    for token in doc:
                        # Past tense
                        if token.tag_=="VBD":
                            token_list[insert_at_index]=token.lemma_
                            token_list.insert(insert_at_index,'did not')

                        # 3rd person singular present tense
                        elif token.tag_=="VBZ": #and token_list[0] not in sing_pronoun_list :
                            token_list[insert_at_index]=token.lemma_
                            token_list.insert(insert_at_index,'does not')

                        # Non-3rd person singular present tense  and 3rd person plural present tense
                        elif token.tag_=="VBP": #and token_list[0] in sing_pronoun_list :
                            token_list[insert_at_index]=token.lemma_
                            token_list.insert(insert_at_index,'do not')  
                        
            # If sentence has 'not', remove it    
            else:
                token_list.remove('not')
                
            # Creating a string from new tokens    
            turnaround_three=' '.join(token_list)

        except:
            turnaround_three='Error - Turnaround Three statement could not be generated'

        
        # Return new string as output of function
        return turnaround_three