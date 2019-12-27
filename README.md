# InformationRetrievalTasks

Implementation of the simple IR models:
1) Vector model (http://www.minerazzi.com/tutorials/term-vector-3.pdf) 

  Every document and request represent as vector in vector space. Relevance ranking of the documents calculates as a cosine the angle between the vector of request and the vector of document.
  
2) Language model (https://en.wikipedia.org/wiki/Language_model)

A statistical language model is a probability distribution over sequences of words. Relevance ranking calculates as a weighted sum of the probability of the request in the docoment and the probability in all documents (I use lambda coefficient to weight them).

#Requirements
python3
pymorphy2

#How to run
1) Vector model:

python stat_model.py  [ARTICLE_PATH] [REQUEST_PATH]

Example: python stat_model.py  ./data/art_2019/art_1.txt ./data/requests/req_2019.txt

2) Language model:

python language_model.py  [ARTICLE_PATH] [REQUEST_PATH] [epsilon]

epsilon - parameter for smoothing

Example:  python language_model.py  ./data/art_2019/art_1.txt ./data/requests/req_2019.txt 1e-3
