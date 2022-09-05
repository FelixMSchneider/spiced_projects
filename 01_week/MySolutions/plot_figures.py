import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



df_gapminder=pd.read_csv('GAPMINDER_INT.csv')


# get global minima and maxima values
popmax=df_gapminder["population"].max()
lifemax=df_gapminder["life_expectancies"].max()
fertmax=df_gapminder["fertility_rates"].max()
popmin=df_gapminder["population"].min()
lifemin=df_gapminder["life_expectancies"].min()
fertmin=df_gapminder["fertility_rates"].min()


allyears=df_gapminder["years"].unique()

outfolder="./figs/"


for i,year in enumerate(allyears):
    fig=plt.figure(figsize=(8,5))
    ax=fig.add_subplot(111)
    yearstr=str(year)
    if i%10==0: print(yearstr)
    df_gapminder_tmp = df_gapminder.loc[df_gapminder['years'] == year]

    sns.scatterplot(x='life_expectancies', y='fertility_rates', hue='continent',
            size='population',size_norm=(popmin,popmax), data=df_gapminder_tmp, alpha=0.6, ax=ax)
    
    ax.set_xlim(lifemin-lifemin*0.05,lifemax+lifemax*0.05)
    ax.set_ylim(fertmin-fertmin*0.05,fertmax+fertmax*0.05)
    

    handels,labels=ax.get_legend_handles_labels()
    plt.legend(handels[0:7],labels[0:7],loc=2, bbox_to_anchor=(1, 1)) # only show handels and labels for colours and suppress sizes 

    plt.title(yearstr)
    plt.tight_layout()
    plt.savefig(outfolder+"/"+ yearstr+"_gapminder.png", dpi=150)

    plt.clf()
    plt.close();


