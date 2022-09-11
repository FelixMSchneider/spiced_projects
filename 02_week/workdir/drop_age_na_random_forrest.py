import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("../../../02_week/data/train.csv")

df=df[df["Age"].isna()==False]

df_tmp  , df_test  = train_test_split(df    ,test_size=0.2, random_state=12)
df_train, df_val   = train_test_split(df_tmp,test_size=0.2, random_state=12)


def encode_sex(df):
    df["male"]=pd.get_dummies(df['Sex'] , drop_first=True)
    return df

def preprocessing(df):
    df = encode_sex(df)
    return df        


df_train = preprocessing(df_train)
df_val  = preprocessing(df_val)
df_test = preprocessing(df_test)


#define test and train dataset
Xtrain = df_train[['male','Pclass','Age', 'SibSp']] 
Xval   =   df_val[['male','Pclass','Age', 'SibSp']] 
Xtest  =  df_test[['male','Pclass','Age', 'SibSp']] 

ytrain = df_train["Survived"]
yval   =   df_val["Survived"]
ytest  =  df_test["Survived"]



import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


m = RandomForestClassifier(max_depth=4, n_estimators=10000)  # n_estimators is the number of decision trees

m.fit(Xtrain, ytrain)


train_score=m.score(Xtrain,ytrain)
val_score=m.score(Xval,yval)
test_score=m.score(Xtest,ytest)
print("Training score :" , train_score)
print("Validation  score :" , val_score)
print("Testing  score :" , test_score)

