"""
Built by Maral Dicle Maral 18.11.2021

Query Processing and Search. Works with: python3 query_process.py
Please enter a query (You can use AND OR NOT operators). Enter E to exit.

Reads the index.pkl file as the inverted index. Contains conjuction(), disjunction(), negation()
and query_process() functions.

"""

import pickle
import time
start_time = time.time()

"""
Conjunction function. Processes the conjunction (AND) operation for search words.

"""
def conjunction (doc1, doc2):
    i,j = 0,0
    cach = []
    if len(doc1) <= len(doc2):
        doc_long = doc2
        doc_short = doc1
    else:
        doc_long = doc1
        doc_short = doc2

    while i < len(doc_long) and j < len(doc_short):
        if doc_long[i] == doc_short[j]:
            cach.append(doc_long[i])
            j += 1
            i += 1
        elif doc_long[i] > doc_short[j]:
            j += 1
        else:
            i += 1
    return cach

"""
Disjunction function. Processes the disjunction (OR) operation for search words.

"""
def disjunction (doc1, doc2):

    i,j = 0,0
    cach = []

    if len(doc1) <= len(doc2):
        doc_long = doc2
        doc_short = doc1
    else:
        doc_long = doc1
        doc_short = doc2

    while  i < len(doc_long) and j < len(doc_short):
        if doc_long[i] == doc_short[j]:
            cach.append(doc_short[j])
            j += 1
            i += 1
        elif doc_long[i] < doc_short[j]:
            cach.append(doc_short[j])
            j += 1
        else:
            cach.append(doc_long[i])
            i += 1
    cach.extend(doc_long[i:])
    return cach
"""
Negation function. Processes the negation (NOT) operation for search words.

"""
def negation (doc1, doc2):

    cach = []
    conj = conjunction(doc1,doc2)
    #Excludes the docs of conjunction from the current list.
    for d in doc1:
        if d not in conj:
            cach.append(d)
    return cach

"""

Processes queries into machine readable form and performs conjunction() disjunction() and negation() operations
for search words entered by the user.

"""
def query_process(query, index):

    q = query.split()
    operations = ['OR', 'AND', 'NOT']
    word_list = []
    query_op = []
    for word in q:
        if word not in operations:
            if word.lower() not in index:
                word_list.append([])
            else:
                word_list.append(index[word.lower()]),
        else:
            query_op.append(word)

    word_count = 1
    op_cach = word_list[0]
    if not len(query_op) == 0:
        for op in query_op:
            if op == 'AND':
                result = conjunction(op_cach, word_list[word_count])
            elif op == 'OR':
                result = disjunction(op_cach, word_list[word_count])
            else:
                result = negation(op_cach, word_list[word_count])
            word_count += 1
    else:
        result = word_list[0]

    return result

def main():

    try:
        idx_file = open("index.pkl", "rb")
        index = pickle.load(idx_file)
        print('Index is succesfully loaded!')
    except(FileNotFoundError):
        index = None
        print('INDEX IS NOT CREATED. Please first run the following command to create an index file:')
        print('python3 index_build.py folder_directory stop_words_directory')
        exit(0)

    print('Please enter a query (You can use AND OR NOT operators). Enter ''E'' to exit.')

    while True:
        query = input("Please enter a query(''E'' for exit):")
        print(query)
        if query == 'E':
            print('Thank you for using my search engine!')
            break
        result = query_process(query, index)
        if len(result) == 0:
            print(query + '  is not found.')
        else:
            print(query + ' is found at: ')
            print(result)


if __name__ == '__main__':

    main()
