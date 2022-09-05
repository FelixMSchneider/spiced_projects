import pandas as pd
import seaborn as sns
import pylab as plt
import numpy as np

titanic=pd.read_csv("../../../02_week/data/train.csv")


survived=len(titanic[titanic["Survived"]==1])
dead=len(titanic[titanic["Survived"]==0])


print("")
print("number of passangers survived: "+ str(survived))
print("number of passangers that died: "+ str(dead))


fig=plt.figure()
ax=fig.add_subplot(111)

ax = sns.countplot(x="Survived", data=titanic)


plt.savefig("survived_vs_dead.png")
