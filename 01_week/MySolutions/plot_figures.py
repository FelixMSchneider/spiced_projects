import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



df_gapminder=pd.read_csv('GAPMINDER_INT.csv')


drop_India_China = False

if drop_India_China:
    df_drop_China =  df_gapminder.drop(index =  df_gapminder[ df_gapminder["country"]=="China"].index)
    df_drop_India = df_drop_China.drop(index = df_drop_China[df_drop_China["country"]=="India"].index)
    df_gapminder  = df_drop_India

    outfolder="./figs_drop_China_India/"
else:
    outfolder="./figs/"



df_gapminder["population"]=(df_gapminder["population"])**(1/2)


# get global minima and maxima values
popmax  = df_gapminder["population"].max()
popmin  = df_gapminder["population"].min()
lifemax = df_gapminder["life expectancy"].max()
lifemin = df_gapminder["life expectancy"].min()
fertmax = df_gapminder["fertility rate"].max()
fertmin = df_gapminder["fertility rate"].min()


allyears=df_gapminder["year"].unique()

for i,year in enumerate(allyears):
    fig = plt.figure(figsize=(8,5))
    ax  = fig.add_subplot(111)

    yearstr=str(year)
    if i%10==0: print(yearstr)

    df_gapminder_tmp = df_gapminder.loc[df_gapminder['year'] == year]

    sns.scatterplot(  x = 'life expectancy', 
                      y = 'fertility rate', 
                    hue = 'continent',
                   size = 'population',
                  sizes = (1,1000),
              size_norm = (popmin,popmax),
                   data = df_gapminder_tmp,
                  alpha = 0.6,
                     ax = ax)
    
    ax.set_xlim(lifemin-lifemin*0.05, lifemax+lifemax*0.05)
    ax.set_ylim(fertmin-fertmin*0.05, fertmax+fertmax*0.05)
    
    handels,labels = ax.get_legend_handles_labels()
    plt.legend(handels[0:7],labels[0:7],loc=2, bbox_to_anchor=(1, 1)) # only show handels and labels for colours and suppress sizes 

    plt.title(yearstr)
    plt.tight_layout()
    plt.savefig(outfolder+"/"+ yearstr+"_gapminder.png", dpi=150)

    plt.clf()
    plt.close()
