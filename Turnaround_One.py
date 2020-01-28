
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

    # Add merge_noun_chunks to pipeline
    merge_noun_chunks = nlp.create_pipe("merge_noun_chunks")
    nlp.add_pipe(merge_noun_chunks)

    # Disable NER
    with nlp.disable_pipes('ner'):

        # Normalise text
        normalised_string=contractions.fix(user_statement)

        # Create a Spacy Document Object
        doc=nlp(normalised_string)

        # Generate list of tokens
        token_list=[token.text for token in doc]

        # CATEGORY A STATEMENT - 2 Key Criteria:

        # Sentence has at least 1 pronoun or proper noun AND # Sentence has both an object and a subject
        if  any(person in [ token.pos_ for token in doc] for person in ['PRON','PROPN'])==True and\
        all(dependency_label in [token.dep_ for token in doc] for dependency_label in ['nsubj','dobj'])==True:

                for token in doc:

                # CAT A Statements - Type 1
                    if token.dep_ =='nsubj' and token.text.upper() =='I':
                        object_index=int(''.join([str(token.i) for token in doc if token.dep_ == 'dobj']))
                        token_list[object_index]='myself'
                        turnaround_one= ' '.join(token_list)

                # CAT A Statements - Type 2
                    elif token.dep_ =='nsubj' and token.text.upper() !='I':

                        subject_index=int(''.join([str(token.i) for token in doc if token.dep_ == 'nsubj']))
                        object_index=int(''.join([str(token.i) for token in doc if token.dep_ == 'dobj']))

                        token_list[subject_index]='I'
                        token_list[object_index]='myself'

                        turnaround_one= ' '.join(token_list)
    return turnaround_one







# In[ ]:
