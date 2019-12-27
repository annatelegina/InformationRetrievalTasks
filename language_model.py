import operator
import math
import copy
import sys
import numpy as np
import pymorphy2

from utils import write_stat


def main():

    #for smoothing
    epsilon = float(sys.argv[3])
    morph = pymorphy2.MorphAnalyzer()

    print("===> ENTER LAMBDA... ")
    l = float(input())
    print("===> Request preparing...")
    req_path = sys.argv[2]
    f = open(req_path, 'r')
    words = {}
    req = f.read()
    
    f.close()
    req_words = write_stat(req, morph)

    article = sys.argv[1]
    f = open(article, 'r') 
    name = article.split('/')[1]
    line = f.read()
    
    text = copy.copy(line)
    
    line = line.strip().split('.')
    out = []
    for i in line: 
        a = "".join(c for c in i if c not in (';','(', ')','!',':', '-', ',', '?', '"', '«','»', '%', '—'))
        out.append(a)
    f.close()
    num = len(out)
    
    text_s = "".join(c for c in text if c not in (';','(', ')','!',':', '-', ',', '?', '"', '«','»', '%', '—', '.'))
    
    text_stat = write_stat(text_s, morph)
    
    dicts = [{} for i in range(len(out))]
    lengths = [0. for i in range(len(out))]
    
    i = 0
    print(out)
    for k in out:
        dicts[i] = write_stat(k, morph)
        i += 1
        
    i = 0
    for d in dicts:
        lengths[i] = 0
        for p in list(d.keys()):
            lengths[i] += d[p]
        i += 1
        
    all_dicts_freq = 0
    for k in list(text_stat.keys()):
        all_dicts_freq += text_stat[k]
        
    models = [1. for i in range(len(out))]
    i = 0
    result_dict = {}
    for d in dicts:
        for word in req_words:
            if word in list(d.keys()):
                print(word, ' ', d[word], ' ', lengths[i])
                doc = l * (d[word]/lengths[i])
            else:
                doc = 0.
            if word in list(text_stat.keys()):
                print(word, ' ', text_stat[word], ' ', all_dicts_freq)
                all_d = (1.- l) * text_stat[word]/all_dicts_freq 
            else:
                all_d = 0.
            models[i]*= (doc + all_d + epsilon)
        result_dict[out[i]] = models[i]
        i += 1
        
    sorted_d = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)

    #PRINT RESULTS
    print("Writing results in", 'res_lambda' + str(l) + '_'+ name+'.txt', " file!")
    gen = open('res_lambda' + str(l) + '_'+ name+'.txt' , 'w')
    for k in sorted_d:
        s = k[0] + ' ' + str(k[1]) + '\n'
        gen.write(s)
    gen.close()
        
        
if __name__ == "__main__":
    main()
        
    

