# CATEGORY A & B STATEMENTS ONLY:
#(1) Descriptive: x=y where x/y represents the self and/or other and the operator describing the relationship
#(2) Self & Other relationship: (i) Self & Self (ii) Self & Other (iii) Other & Other
#(3) Begin and end with a proper noun and/or pronoun.


# Turnaround Two - Switch position of self & Other in sentence. Subject becomes object, vice-versa

def turnaround_two_generator(user_statement):
	
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
            
                if doc[0].text !='I':
                    turnaround_two='Statement already directed to other'
                    
                else:
                    token_list[0]='Other people'
                    
                    if doc[-1].pos_=='NOUN' and doc[1].lemma_=='be':
                        token_list[-1]=doc[-1]._.inflect('NNS')
                        token_list[1]='are'
                        token_list.remove('a')
                        
                        
                    turnaround_two=' '.join(token_list)
                        
            else:
                
                # CATEGORY A STATEMENTS

                # Assigning subject and object of the statement to respective variables
                initial_subject=token_list[0]
                initial_object=token_list[-1]

                # Making the object, the subject
                if initial_object in ['me','myself']:
                    token_list[0]='I'
                else:
                    token_list[0]=initial_object

                # Making the initial subject, the object
                if initial_subject =='I':
                    token_list[-1]='myself'
                else:
                    token_list[-1]=initial_subject

                # Creating a string from new tokens
                turnaround_two=' '.join(token_list)

        except:
            turnaround_two='Error - Turnaround Two statement could not be generated'
        
        # Return new string as output of function
        return turnaround_two