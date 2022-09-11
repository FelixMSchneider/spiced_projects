import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

kaggle=False
#kaggle=True

##
## Despite this simple logistic regression results in about 0.8 score in train, validation and test datasets (using random_state=12)
## the kaggle score is only 0.756 
##


datapath="/home/felix/spiced/02_week/data/"

df=pd.read_csv(datapath + "train.csv")

if not kaggle:
    # split data if not using whole test.csv for kaggle
    df_tmp, df_test  = train_test_split(df    ,test_size=0.2, random_state=12)
    df_train, df_val = train_test_split(df_tmp,test_size=0.2, random_state=12)
else:
    df_train=df
    df_test=pd.read_csv(datapath + "test.csv")

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

# define test and train dataset

Xtrain = df_train[['male','Pclass','new_Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','new_Age', 'SibSp']] 

ytrain = df_train["Survived"]

m=LogisticRegression()

m.fit(Xtrain,ytrain)

train_score=m.score(Xtrain,ytrain)
print("Training score :" , train_score)

if not kaggle: 
    Xval  =  df_val[['male','Pclass','new_Age', 'SibSp']] 
    yval  =  df_val["Survived"]
    ytest  =  df_test["Survived"]
    val_score=m.score(Xval,yval)
    test_score=m.score(Xtest,ytest)
    print("Testing  score :" , test_score)
    print("Validation  score :" , val_score)
else:
    # prepare result.csv file  for submission to kaggle

    pred=m.predict(Xtest)
    df_result=pd.DataFrame()
    df_result["PassengerId"]=df_test["PassengerId"]
    df_result.reset_index(inplace=True)
    df_result["Survived"]=pd.Series(pred)
    df_result.set_index("PassengerId", inplace=True)
    df_result.drop("index", axis=1, inplace=True) 
    df_result.to_csv("result_LR.csv")
