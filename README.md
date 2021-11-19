# Information Retrieval System For Boolean Queries 
A search system which can preprocess, build an inverted index for a folder of text data and performs a boolean query processing for information retrieval from Reuters files. Python3 was used. 

Index is built with: 

python3 index_build.py ./reuters21578/ ./stopwords.txt 


Query processing module is called with:

python3 query_process.py


Query processing module takes single word query arguments with AND OR and NOT operators.
Please press E for exiting the query processing module.


P.S:

System may need BS4 library. If so, please run following line on terminal:

python3 -m pip install -r requirements.txt