import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("../../../02_week/data/train.csv")

X = df[['Sex','Pclass','Age']]   # <=== features/independent variables
y = df['Survived']

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=12)

def encode_sex(df):
    df["male"]=pd.get_dummies(df['Sex'] , drop_first=True)
    return df

def get_group_means(df):
    Group=df.groupby(["Sex","Pclass"])
    cdict={}
    meandict={}
    for (sex,pclass),sub_df in Group:
        key=sex+"_"+str(pclass)
        cdict[key]=sub_df
        meandict[key]=sub_df["Age"].mean()
    return cdict, meandict

def impose_group_means(cdict,meandict):
    for i, key in enumerate(cdict.keys()):
        cur_df=cdict[key]
        cur_df["new_Age"]=cur_df["Age"].fillna(meandict[key])

        if i==0: final_df=cur_df
        if i>0:
            final_df=pd.concat([final_df, cur_df])

    return final_df


Xtrain = encode_sex(Xtrain)
cdict_train, meandict_train = get_group_means(Xtrain)
Xtrain = impose_group_means(cdict_train, meandict_train)


Xtest  = encode_sex(Xtest)
cdict_test , meandict_test  = get_group_means(Xtest)
Xtest  = impose_group_means(cdict_test , meandict_train)  # impose meandict_train on test dataset





