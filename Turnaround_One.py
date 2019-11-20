
# CATEGORY A & B STATEMENTS ONLY:
#(1) Descriptive: x=y where x/y represents the self and/or other and the operator describing the relationship
#(2) Self & Other relationship: (i) Self & Self (ii) Self & Other (iii) Other & Other
#(3) Begin and end with a proper noun and/or pronoun.


# Turnaround one - Creating self to self relationship
def turnaround_one_generator(user_statement):


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
        
            # CATEGORY B STATEMENTS
            
            # 
            if doc[-1].pos_ != 'PROPN' and doc[-1].pos_ != 'PRON':
                
                if token_list[0]=='I':
                    turnaround_one="Statement is already directed to self"
                    
                else:
                    token_list[0]='I'
                    token_list[1]=doc[1]._.inflect('VBP')
                    turnaround_one=' '.join(token_list)
                    
                    
            # CATEGORY A STATEMENTS        
                
            else:
                
                # If statement already contains 'I' and 'myself', turnaround one not required
                if all(x in token_list for x in ['I', 'myself'])==True:        
                    turnaround_one="Statement is already directed to self"

                # Else generate turnaround one  
                else:
                    # Change 1st word to 'I'
                    token_list[0]="I"
                    
                    if doc[1].tag_ !='VBD':
                    # Change verb to be non-3rd person singular present
                        token_list[1]=doc[1]._.inflect('VBP')
                        
                    token_list[-1]='myself'
                        
                    # Generate turnaround statement string 
                    turnaround_one=' '.join(token_list)

        except:
            turnaround_one='Error - Turnaround One statement could not be generated'        
                         
        return turnaround_one




# In[ ]:




