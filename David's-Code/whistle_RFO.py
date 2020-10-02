#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 13:08:40 2019
@author: never
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

#each value represents the number of shared connections (i.e. users) between a source and a target user
#we model a fake user, like a spambot or troll, as someone who has lots connections to other users
#but very few users follow/connect to him

n_users=1000
user_data=[] #matrix representation of shared connections
user_target=[] #real identity fake or real
prop_fakes=.3 #proportion of fake users in whole data sample

#create random training data with connectivity matrices for real and fake sources
for i in range(n_users):
    flip=np.random.random(1)
    if flip>prop_fakes:
       this_data=(np.tril(np.random.randint(0,10,[5,5]))+np.triu(np.random.randint(0,10,[5,5])))
       user_target.append(1)
    else:
        this_data=(np.tril(np.random.randint(0,10,[5,5]))+np.triu(np.random.randint(0,2,[5,5])))        
        user_target.append(0)
    user_data.append(this_data.flatten())

#create training sets for ML model
Xtrain, Xtest, ytrain, ytest = train_test_split(user_data, user_target,
                                                random_state=0)
#create a random forest classifier and train it
model = RandomForestClassifier(n_estimators=1000)
model.fit(Xtrain, ytrain)

#test accuracy of model classifications
ypred = model.predict(Xtest) #after a model has been training you can submit here new patterns for classification
mat = confusion_matrix(ytest, ypred)
sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False)
plt.xlabel('true label')
plt.ylabel('predicted label');

print(metrics.classification_report(ypred, ytest))



