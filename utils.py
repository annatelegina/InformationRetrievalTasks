import pymorphy2
import math

def write_stat(sent, morph):
    words = sent.split()
    d = {}
    for word in words:
        w = morph.parse(word)[0]
        word = w.normal_form
        if word in list(d.keys()):
            d[word] += 1
        else:
            d[word] = 1
    return d
    
def if_idf(sent, morph):
    d = {}
    for i in sent:
        f = i.split()
        marked = []
        for wor in f:
            w = morph.parse(wor)[0]
            word = w.normal_form
            if word not in marked:
                if word in list(d.keys()):
                    d[word] += 1
                else:
                    d[word] = 1
                marked.append(word)
    return d
    
def if_idf_request(request, sent, morph):
    request = list(request.keys())
    res = {}
    d = {}
    for i in sent:
        f = i.split()
        marked = []
        for line in f:
            w = morph.parse(line)[0]
            word = w.normal_form
            if word in request and word not in marked:
                if word in list(d.keys()):
                    d[word] += 1
                else:
                    d[word] = 1
                marked.append(word)
    return d

def print_statistics(name, sorted_d, out):  
    gen = open(name, 'w')
    for k in sorted_d:
        sent = out[int(k[0])]
        g = k[1] if not math.isnan(k[1]) else 0.
        s = sent.strip() + ' ' + str(g) + '\n'
        gen.write(s)
    gen.close()
