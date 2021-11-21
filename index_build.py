"""
Built by Maral Dicle Maral 18.11.2021

Indexing file. Works with: python3 index_build.py folder_directory stop_words_directory
Drops a index.pkl file to the current directory.
Contains processor(), indxer(), fileHandler() functions.

"""

from bs4 import BeautifulSoup
import os
import time
from multiprocessing import Process, Manager
import pickle
import sys

start_time = time.time()

"""
Reads an individual file and the stop_words file, tokenizes, cleans stop words and punctuations of the docs. 
Changes result to a list of tokenized words. 

"""

def processor(dir, stops, input, result):

    stop_words = open(stops).read().split()
    punct = '''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~''' #From string.punctuation list

    file_handler = open(dir + input, 'r', encoding='latin1').read()
    soup = BeautifulSoup(file_handler, 'html.parser')

    reuters = soup.find_all('reuters')

    #Reads reuters documents, tokenizes, cleans stop words and punctuations
    for r in reuters:
        id = r['newid']
        if r.body == None:
            result[id] = []
            continue
        text = r.text.lower()
        for t in text:
            if t in punct:
                text = text.replace(t, " ")

        text = text.replace('\n', ' ')
        tokens = text.replace('\t', ' ')

        tokenized = tokens.split()
        tokenized1 = []
        for t in tokenized:
            if not t in stop_words:
                tokenized1.append(t)

        result[id] = tokenized1

"""

Builds the inverted index and saves the inverted index dictionary as a file.

"""
def idxer(docs):
    inverted_idx = {}
    for key in docs:
        ID = int(key)
        words = docs[key]
        for word in words:
            if not word in inverted_idx:
                inverted_idx[word] = [ID]
            else:
                if inverted_idx[word][-1] == ID: # If docID is already added to the inverted index, continue
                    continue
                inverted_idx[word].append(ID)
    for word in inverted_idx:
        inverted_idx[word].sort()

    #Saves the inverted index into current file.
    idx_dump = open("index.pkl", "wb")
    pickle.dump(inverted_idx, idx_dump)
    idx_dump.close()
    return inverted_idx
"""

Creates a new process for each file in reuters directory calls processor() for each file. 
A common dictionary for ID: words is kept for processes.
idxer() is called to create word: IDs 

"""
def fileHandler(dir, stops):
    files = os.listdir(dir)
    input_starter = 'reut'
    manager = Manager()
    w_dict = manager.dict()
    processes = []
    results = []
    count = 0

    for f in files:
        if input_starter in f:
            temp_dict = {}
            process = Process(target=processor, args=(dir, stops, f, w_dict))
            results.append(temp_dict)
            processes.append(process)
            process.start()
            count += 1
    for i in range(len(processes)):
        processes[i].join()

    idxer(w_dict)


def main():
    dir = sys.argv[1]
    stops = sys.argv[2]
    fileHandler(dir,stops)


if __name__ == '__main__':
    main()
    run_time = time.time() - start_time	
    print("- Index is created in %.6f seconds -" % run_time)

