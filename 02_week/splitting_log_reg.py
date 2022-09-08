import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("../../../02_week/data/train.csv")

df_train, df_test= train_test_split(df,test_size=0.2, random_state=12)



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



df_train = encode_sex(df_train)
cdict_train, meandict_train = get_group_means(df_train)
df_train = impose_group_means(cdict_train, meandict_train)


df_test  = encode_sex(df_test)
cdict_test , meandict_test  = get_group_means(df_test)
df_test  = impose_group_means(cdict_test , meandict_train)  # impose meandict_train on test dataset

Xtrain = df_train[['male','Pclass','new_Age', 'SibSp']]   # <=== features/independent variables
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']]   # <=== features/independent variables
#Xtrain = df_train[['male','Pclass','new_Age', 'Parch']]   # <=== features/independent variables
#Xtest  =  df_test[['male','Pclass','new_Age', 'Parch']]   # <=== features/independent variables

ytrain = df_train["Survived"]
ytest  =  df_test["Survived"]

m=LogisticRegression()

m.fit(Xtrain,ytrain)

train_score=m.score(Xtrain,ytrain)
test_score=m.score(Xtest,ytest)

print("Training score :" , train_score)
print("Testing  score :" , test_score)

