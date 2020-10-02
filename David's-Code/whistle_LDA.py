#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:14:52 2019

@author: never
"""

#IMPORT MODULES AND ONLINE RESOURCES
import gensim
from gensim import corpora
import string
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from scipy.stats.stats import pearsonr
import pandas as pd
import numpy as np

#HYPOTHETICAL TWEETER DATA
#I created here some tipical tweeters data. The real packets are streams of tweets or any piece of news.
#Grouped by user/source.

#user 1 - each doc is a tweet
doc1a = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2a = "My father spends a lot of time driving my sister around to dance practice."
doc3a = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4a = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5a = "Health experts say that Sugar is not good for your lifestyle."

#user 2 - each doc is a tweet
doc1b = "Politics is bad for your health, doctors say. It increases stress."
doc2b = "My father says all politicians lie. I agree that some lie, but not all of them."
doc3b = "Doctors suggest that eating too much pasta is bad for your health."
doc4b = "I think politics is a major part of life and everyone should care about it."
doc5b = "A healthy lifestyle is what drives growth in society."

#user 3 - each doc is a tweet
doc1c = "All doctors lie as all politicians."
doc2c = "When I read news, I find my stress increases."
doc3c = "All politicians are liars and are not to be trusted."
doc4c = "When I read news, I always find politics hard to believe."
doc5c = "Experts say it's bad for your health to engage in politics."

# compile documents
doc_complete1 = [doc1a, doc2a, doc3a, doc4a, doc5a]
doc_complete2 = [doc1b, doc2b, doc3b, doc4b, doc5b]
doc_complete3 = [doc1c, doc2c, doc3c, doc4c, doc5c]

#clean documents
stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean1 = [clean(doc).split() for doc in doc_complete1]  
doc_clean2 = [clean(doc).split() for doc in doc_complete2]  
doc_clean3 = [clean(doc).split() for doc in doc_complete3]  

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary1 = corpora.Dictionary(doc_clean1)
dictionary2 = corpora.Dictionary(doc_clean2)
dictionary3 = corpora.Dictionary(doc_clean3)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix1 = [dictionary1.doc2bow(doc) for doc in doc_clean1]
doc_term_matrix2 = [dictionary2.doc2bow(doc) for doc in doc_clean2]
doc_term_matrix3 = [dictionary3.doc2bow(doc) for doc in doc_clean3]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel1 = Lda(doc_term_matrix1, num_topics=3, id2word = dictionary1, passes=50)
ldamodel2 = Lda(doc_term_matrix2, num_topics=3, id2word = dictionary2, passes=50)
ldamodel3 = Lda(doc_term_matrix3, num_topics=3, id2word = dictionary3, passes=50)

print(ldamodel1.print_topics(num_topics=3, num_words=3))
print(ldamodel2.print_topics(num_topics=3, num_words=3))
print(ldamodel3.print_topics(num_topics=3, num_words=3))

topics1=ldamodel1.print_topics(num_topics=3, num_words=3)
topics2=ldamodel2.print_topics(num_topics=3, num_words=3)
topics3=ldamodel3.print_topics(num_topics=3, num_words=3)

#compute similarity matrix for each topic and each user
t1a=str.split(topics1[0][1])
t2a=str.split(topics1[1][1])
t3a=str.split(topics1[2][1])

t1b=str.split(topics2[0][1])
t2b=str.split(topics2[1][1])
t3b=str.split(topics2[2][1])

t1c=str.split(topics3[0][1])
t2c=str.split(topics3[1][1])
t3c=str.split(topics3[2][1])

#extract single words plus weights
def create_matrix(user_topics):
    user_M=[]
    for i in range(len(user_topics)):
        #split topics in terms and weights
        t=user_topics[i][1].split('+')     
        word_vec=[]
        weight_vec=[]
        topic_vec=[]     
        for j in range(len(t)):
            weight,word=t[j].split('*')
            word_vec.append(weight)
            weight_vec.append(word)
            topic_vec.append(i)
        user_M.append([topic_vec,weight_vec,word_vec])
    return user_M
        
user_topic1=create_matrix(topics1)
user_topic2=create_matrix(topics2)
user_topic3=create_matrix(topics3)

#compute the global similarity matrix    
all_topics=np.unique([user_topic1[0][1],user_topic1[1][1],user_topic1[2][1],
           user_topic2[0][1],user_topic2[1][1],user_topic2[2][1],
           user_topic3[0][1],user_topic3[1][1],user_topic3[2][1]])

def get_topic_scores(user_topics,all_topics):
    user_scores=[]
    for t in range(len(user_topics)):
        topic_scores=[]
        for itopic in all_topics:
            idx=[user_topics[t][1].index(i) for i in user_topics[t][1] if itopic in i]
            if idx:
                topic_scores.append(float(user_topic1[0][2][idx[0]]))
            else:
                topic_scores.append(0.0)
        user_scores.append(topic_scores)
    return user_scores

#get topic scores per user per topic
user1=get_topic_scores(user_topic1,all_topics)    
user2=get_topic_scores(user_topic2,all_topics)    
user3=get_topic_scores(user_topic3,all_topics)    
all_users=[user1,user2,user3]

#now compute pearsons correlations among all users and topics
n_users=3
n_topics=3
source_user=[]
target_user=[]
source_topic=[]
target_topic=[]
topic_corr=[]
topic_pval=[]
for s_user in range(n_users):
    for s_topic in range(n_topics):
        for t_user in range(n_users): 
            for t_topic in range(n_topics):
                source_user.append(s_user)
                target_user.append(t_user)
                source_topic.append(s_topic)
                target_topic.append(t_topic)                
                corr_score=pearsonr(all_users[s_user][s_topic],all_users[t_user][t_topic])
                topic_corr.append(corr_score[0])
                topic_pval.append(corr_score[1])

#organize results in data frame format
all_scores=pd.DataFrame([source_user,source_topic,target_user,target_topic,topic_corr,topic_pval])        
all_scores=pd.DataFrame.transpose(all_scores) 
all_scores.columns=['sUser','sTopic','tUser','tTopic','Pcorr','Pval']

#print topic/users with significant similarity
best_peers=all_scores[all_scores['sUser']!=all_scores['tUser']]
best_peers=best_peers[best_peers['Pval']<0.05 ]

print(best_peers)
       
        