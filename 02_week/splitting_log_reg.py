import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("../../../02_week/data/train.csv")

df_tmp, df_test  = train_test_split(df    ,test_size=0.2, random_state=12)
df_train, df_val = train_test_split(df_tmp,test_size=0.2, random_state=12)



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

def preprocessing(df,trainmeandict=None):
    df = encode_sex(df)
    cdict, meandict = get_group_means(df)
    if trainmeandict != None:
        df = impose_group_means(cdict, trainmeandict)
        return df
    else:
        df = impose_group_means(cdict, meandict)
        return df, meandict
        


df_train, trainmeandict = preprocessing(df_train)

df_val  = preprocessing(df_val , trainmeandict)
df_test = preprocessing(df_test, trainmeandict)


#define test and train dataset
Xtrain = df_train[['male','Pclass','new_Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']] 

ytrain = df_train["Survived"]
ytest  =  df_test["Survived"]

m=LogisticRegression()

m.fit(Xtrain,ytrain)

train_score=m.score(Xtrain,ytrain)
test_score=m.score(Xtest,ytest)

print("Training score :" , train_score)
print("Testing  score :" , test_score)

