import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


kaggle=False
kaggle=True

datapath="/home/felix/spiced/02_week/data/"

df=pd.read_csv(datapath + "train.csv")

if not kaggle:
    # split data if not using whole test.csv for kaggle
    df_tmp, df_test  = train_test_split(df    ,test_size=0.2, random_state=12)
    df_train, df_val = train_test_split(df_tmp,test_size=0.2, random_state=12)
else:
    df_train=df
    df_test=pd.read_csv(datapath + "test.csv")


# define functions for preprocessing (encoding and na-replacement)

def encode_sex(df):
    df["male"]=pd.get_dummies(df['Sex'] , drop_first=True)
    return df

def add_Pclass_sex(df):
    df["class_sex"]=df["Pclass"].transform(str) + "_" + df["Sex"].str[0]
    return df

def fillna_groups(df,groupmean=None):
    '''
    this function fills na of Age based on mean values for groups
    groups are defined by Passenger class_sex (combination of passenger class and sex)
    if groupmean=None: 
         Groupmeans are derived and imposed to nans
         Groupmeans are returned
    if groupmeans dictionary is passed: groupmeans of dictionary are imposed to nan values 

    for test data give groupmeans of train data 
    '''
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
df_test ,       dum = preprocessing(df_test, trainmean)

if not kaggle: 
    df_val , dum    = preprocessing(df_val , trainmean)


df_test.to_csv("test_PP.csv")

#define test and train dataset
Xtrain = df_train[['male','Pclass','new_Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']] 

ytrain = df_train["Survived"]
if not kaggle: ytest  =  df_test["Survived"]


m = RandomForestClassifier(max_depth=3, n_estimators=1000)  # n_estimators is the number of decision trees

m.fit(Xtrain, ytrain)

train_score=m.score(Xtrain,ytrain)

print("Training score :" , train_score)
if not kaggle:
    test_score=m.score(Xtest,ytest)
    print("Testing  score :" , test_score)
else:
    # prepare result.csv file  for submission to kaggle

    pred=m.predict(Xtest)
    df_result=pd.DataFrame()
    df_result["PassengerId"]=df_test["PassengerId"]
    df_result.reset_index(inplace=True)
    df_result["Survived"]=pd.Series(pred)
    df_result.set_index("PassengerId", inplace=True)
    df_result.drop("index", axis=1, inplace=True) 
    df_result.to_csv("result_RF1.csv")
