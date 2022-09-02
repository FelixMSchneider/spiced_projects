
import pandas as pd


PATH="../../garlic-boosting-encounter-notes/01_week/data/"

# Read Data
df_life_expecancy = pd.read_excel(PATH + "gapminder_lifeexpectancy.xlsx")
df_population     = pd.read_excel(PATH + "gapminder_population.xlsx")
df_fertility      = pd.read_csv(PATH + "gapminder_total_fertility.csv")
df_continents     = pd.read_csv(PATH + "continents.csv", sep=";")




df_fertility.set_index(df_fertility.columns[0], inplace=True)
df_population.set_index(df_population.columns[0], inplace=True)
df_life_expecancy.set_index(df_life_expecancy.columns[0], inplace=True)

df_fertility.index.name="countries"
df_population.index.name="countries"
df_life_expecancy.index.name="countries"

df_fertility.columns=df_fertility.columns.astype(int)

for df in [df_fertility, df_population,df_life_expecancy]:
    df.reset_index(inplace=True)


df_fertility_long      = df_fertility.melt(id_vars="countries", var_name="years", value_name="fertility_rates")
df_life_expecancy_long = df_life_expecancy.melt(id_vars="countries", var_name="years", value_name="life_expectancies")

df_population_long=df_population.melt(id_vars="countries", var_name="years", value_name="population")

df_continents.rename({"country":"countries"}, axis=1, inplace=True)

df_gapminder=df_fertility_long.merge(df_life_expecancy_long, on= ["countries", "years"])
df_gapminder=df_gapminder.merge(df_population_long, on= ["countries", "years"], how="outer")
df_gapminder=df_gapminder.merge(df_continents, on= ["countries"], how="left")


Groups=df_gapminder.groupby("countries")
cdict={}
for country,sub_df in Groups:
    cdict[country]=sub_df



for i, country in enumerate(cdict.keys()):
    cur_df=cdict[country]
    cur_df.interpolate(limit_area="inside", inplace=True)
    if i==0: final_df=cur_df
    if i>0:
        final_df=pd.concat([final_df, cur_df])

final_df.to_csv("GAPMINDER_INT.csv")
