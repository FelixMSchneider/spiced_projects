import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df=pd.read_csv("../../../02_week/data/train.csv")

X = final_df[['Sex','Pclass','Age']]   # <=== features/independent variables
y = final_df['Survived']    

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=12)


           


def encode_sex(df)
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



def impose_group_means(cdict,meandict)
    for i, key in enumerate(cdict.keys()):
        cur_df=cdict[key]
        cur_df["new_Age"]=cur_df["Age"].fillna(meandict[key])
    
        if i==0: final_df=cur_df
        if i>0:
            final_df=pd.concat([final_df, cur_df])
        
    return final_df        
        


df=encode_sex(df)

cdict_train,meandict_train=get_group_means(Group)


# In[24]:


final_df


# In[25]:


final_df["class_sex"]=final_df["Pclass"].apply(str) + "_" +final_df["Sex"]


# In[26]:


final_df


# In[27]:


final_df.groupby("class_sex")["Age"].apply("mean")


# In[28]:


final_df["new_Age_2"]=final_df["Age"].fillna(final_df.groupby("class_sex")["Age"].transform("mean"))


# In[29]:


# check if new_Age and new_Age_2 are the same
len(final_df[(final_df["new_Age"]!=final_df["new_Age_2"])])==0


# In[30]:




# In[31]:




# In[32]:


#dropna=Xtrain["Age"].isna()==False


# In[33]:


m = LogisticRegression() 


# In[34]:


Xtrain


# In[35]:



m.fit(Xtrain, ytrain) 


# In[36]:


m.score(Xtrain,ytrain)


# In[37]:


m.score(Xtest,ytest)


# In[38]:


ypred=m.predict(Xtest)
ypred_train=m.predict(Xtrain)


# In[39]:


from sklearn import metrics


# In[40]:


metrics.accuracy_score(ytest,ypred)


# In[41]:


metrics.precision_score(ytest,ypred)


# In[42]:


metrics.recall_score(ytest,ypred)


# In[43]:


metrics.f1_score(ytest,ypred),metrics.f1_score(ytrain,ypred_train)


# In[44]:


metrics.confusion_matrix(ytest,ypred)


# In[45]:


metrics.plot_confusion_matrix(m, Xtest,ytest)


# In[46]:


metrics.plot_roc_curve(m, Xtest,ytest)


# In[ ]:




