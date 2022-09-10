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

df_train, trainmean = preprocessing(df_train)
df_val,    dum      = preprocessing(df_val , trainmean)
df_test,   dum      = preprocessing(df_test, trainmean)




#define test and train dataset
Xtrain = df_train[['male','Pclass','new_Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']] 

ytrain = df_train["Survived"]
ytest  =  df_test["Survived"]



import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score




m = RandomForestClassifier(max_depth=3, n_estimators=1000)  # n_estimators is the number of decision trees

m.fit(Xtrain, ytrain)


train_score=m.score(Xtrain,ytrain)
test_score=m.score(Xtest,ytest)
print("Training score :" , train_score)
print("Testing  score :" , test_score)

