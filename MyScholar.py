import scholarly
import csv
from collections import Counter
import string
import re
import json
from os import listdir
blacklist=[
    'the','a','and','of','to','in','is','for','we','with','our','no','most',
    'this','on','class="gsc_vcd_value"','id="gsc_vcd_descr"><div',
    'can','are','that','which','by','an','however','has','…</div></div><div','as','.','class="gsh_small"><div',
    'idgsc_vcd_descrdiv','classgsc_vcd_value','classgsh_smallThe','classgsh_smalldiv','classgsh_smallSleep','there',
    'from','be','based','or','have','been','at','using','it','also','many','their',
    'one','not','its','into'
]

def GenIndex():
    index=[]
    for f in listdir('Data'):
        if f=='People.json':
            continue
        with open('Data/'+f)as r:
            p=json.loads(r.read())
        r.close()
        index.append([p['author']['id'],p['author']['name'],p['author']['affiliation']])
    with open("Data/People.json",'w')as f:
        f.write(json.dumps(index))
    f.close()
def Get(name):

    abstracts=""
    publisher={}
    publication=[]
    authordata={}    
    words=[]

    search=scholarly.search_author(name)                 # data
    authorinfo=next(search).fill()                               # 作者信息
            
    authordata["name"]=authorinfo.name
    authordata["affiliation"]=authorinfo.affiliation
    authordata["citedby"]=authorinfo.citedby
    authordata["cites_per_year"]=authorinfo.cites_per_year
    authordata["hindex"]=authorinfo.hindex
    authordata["i10index"]=authorinfo.i10index
    authordata["picture"]=authorinfo.url_picture
    authordata["id"]=authorinfo.id
    authordata['publictaion_count']=len(authorinfo.publications)

    pub_id=0
    pub_count=len(authorinfo.publications)
    for i in authorinfo.publications:                           # 遍历作者所有发表物体
        pub=i.fill()                                        # 获取当前发表物信息
        pub_id+=1
        print("Analyze ("+str(pub_id)+"/"+str(pub_count)+") ["+pub.bib['title']+"]")
        if('abstract' in pub.bib):
            abstracts+=str(pub.bib['abstract'])                 # 储存 abstract
        if 'publisher' in pub.bib:
            if pub.bib['publisher'] in publisher.keys():       # 检测是否保存过当前publisher
                publisher[pub.bib['publisher']]+=1              
            else:
                publisher[pub.bib['publisher']]=0
        elif 'other' in publisher.keys():
            publisher['other']+=1     
        else:
            publisher['other']=0  
        if len(publication)<5:
            publication.append([pub.bib['title'], pub.citedby if hasattr(pub,'citedby') else 0,pub.bib['year']])


    #************************************                   # Debug Purpose
    # with open("D:/data.txt",'w')as f:
    #     f.write(abstracts)
    # f.close()
    #************************************   
    # with open("D:/data.txt",'r')as f:
    #     abstracts=f.read()
    #************************************                          
    counts = dict(Counter(re.sub(r'[^\w\s]','',abstracts).split()))  # 去除标点符号并分割         
    for i in list(counts.keys()):
        if i.lower() in blacklist or int(counts[i])<=2:
            del counts[i]
    for i in counts.keys():
        words.append([i,int(counts[i])])
    words.sort(key=lambda x:x[1],reverse=True)

    factor=200/(words[0][1])
    for i in words:
        i[1]*=factor
    words=words[:100]

    DATA={
    'words':words,
    'author':authordata,
    'publication':publication,
    'publisher':publisher
    }   
    with open("Data/"+name.replace(" ", "")+".json",'w')as f:
        f.write(json.dumps(DATA))
    f.close()
    print("ALL DONE")
    GenIndex()



# def Fix():
#     with open("D:/WenyaoXu2.json",'r')as f:
#         js=f.read()
#     f.close()
#     a=json.loads(js)
#     factor=200/(a['words'][0][1]/5)


#     for i in list(a['words']):
#         if i[0] in blacklist:
#              a['words'].remove(i)
#     for i in a['words']:
#         i[1]=int(i[1]/5*factor)

#     a['words']=a['words'][:100]
#     with open("D:/WenyaoXu2_FIXED.json",'w')as f:
#         f.write(json.dumps(a))
#     f.close()



#Save

# Words
# Author
# publications
# publisher

#Get("Zhengxiong Li")

#Fix()

