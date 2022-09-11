import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


#split dataset 
df=pd.read_csv("../../../02_week/data/train.csv")

df_test=pd.read_csv("test.csv")

def encode_sex(df):
    df["male"]=pd.get_dummies(df['Sex'] , drop_first=True)
    return df

def add_Pclass_sex(df):
    df["class_sex"]=df["Pclass"].transform(str) + "_" + df["Sex"].str[0]
    return df

def fillna_groups(df,groupmean=None):
    if type(groupmean)==type(None):
        groupmean=df.groupby("class_sex")["Age"].mean()
    df['new_Age'] = df['Age'].fillna(df['class_sex'].map(groupmean))
    return df,groupmean

def preprocessing(df,trainmean=None):
    df = encode_sex(df)
    df=add_Pclass_sex(df)
    df,groupmean=fillna_groups(df, groupmean=trainmean)
    return df,groupmean    

df, trainmean = preprocessing(df)
df_test,   dum      = preprocessing(df_test, trainmean)


#define test and train dataset
X = df[['male','Pclass','new_Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']] 

y = df["Survived"]

m=LogisticRegression()

m.fit(X,y) # use whole dataset for training


pred=m.predict(Xtest)

df_result=pd.DataFrame()
df_result["PassengerId"]=df_test["PassengerId"]
df_result["Survived"]=pd.Series(pred)
df_result.set_index("PassengerId", inplace=True)
df_result.to_csv("result.csv")
