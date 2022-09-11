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
plt.savefig("figures/survived_vs_dead.png")


firstclass=len(titanic[titanic["Pclass"]==1])
survived_first_class=len(titanic[(titanic["Pclass"]==1) * (titanic["Survived"]==1)])
percent=round(100*(survived_first_class/ firstclass),1)
print("portion of person survived in the first class: "+ str(percent) + "% ")



