import operator
import math
import numpy as np
import pymorphy2

from utils import write_stat, if_idf, if_idf_request

def check_norm(dic):
    norm = 0.
    for keys in list(dic.keys()):
        norm += dic[keys]**2
    
    return round(math.sqrt(norm)) == 1
    
def cos_dist(sent, request):
    s = 0.
    for keys in list(request.keys()):
        if keys in list(sent.keys()):
            s += request[keys]*sent[keys]
    if math.isnan(s):
        return 0.
    else:
        return s


def main():
    print("With idf? 1 or 0")
    idf = int(input())
    print("===> Request preparing...")
    f = open('./requests/req_viet.txt', 'r')
    words = {}
    for i in f:
        k = i.strip().split()
        words[k[0]] = float(k[1])
    f.close()
    keys = list(words.keys())
    
    print("===> Enter the path to the article....")
    article = input()
    f = open(article, 'r')
    name = article.split('/')[1]
    line = f.read()
    line = line.strip().split('.')
    out = []
    for i in line: 
        a = "".join(c for c in i if c not in (';','(', ')','!',':', '-', ',', '?', '"', '«','»', '%', '—'))
        out.append(a)
    f.close()
    num = len(out)
    
    morph = pymorphy2.MorphAnalyzer()
    if idf:
        d = if_idf(out, morph)
        d_req = if_idf_request(words, out, morph)
        print(d_req)
        print(words)
        for i in list(words.keys()):
            if i in list(d_req.keys()):
                a = words[i] * np.log10(num/d_req[i])
            else:
                a = 0
            words.update({i:a})
        
    vec = []       
    for k in list(words.keys()):
        vec.append(words[k])
        
    #normalizing vector of request
    v = np.array(vec)
    norm = np.linalg.norm(v)
    
    for key in list(words.keys()):
        p = words[key]/norm
        words.update({key:p})
    print(words)
    count = 0
    res = {}
    for sent in out:
        sentence = {}
        aft = {}
        aft = write_stat(sent, morph)
        if aft == {}:
            continue
        vect = []
        for i in list(aft.keys()):
            a = float(aft[i]) if not idf else float(aft[i])*np.log10(num/d[i])
            vect.append(a)
            if idf:
                aft.update({i:a})
                
        #normalize of document vector
        vect  = np.array(vect)
        norm_2 = np.linalg.norm(vect)

        for key in list(aft.keys()):
            p = aft[key]/norm_2
            aft.update({key:p})

        s1 = check_norm(aft)
        d1 = check_norm(words)
        assert s1 and d1
       
        for word in list(aft.keys()):
            if word in keys:
                sentence[word] = aft[word]
                
        cos = cos_dist(sentence, words)
        res[count] = cos
        count += 1
    sorted_d = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
    
    #PRINT RESULTS
    gen = open('res_idf' + str(idf) + '_'+ name , 'w')
    for k in sorted_d:
        se = out[int(k[0])]
        line = se
        g = k[1] if not math.isnan(k[1]) else 0.
        s = line.strip() + ' ' + str(g) + '\n'
        gen.write(s)
    gen.close()
        
        
if __name__ == "__main__":
    main()
        
    

