
import pandas as pd


PATH="../../garlic-boosting-encounter-notes/01_week/data/"

# Read Data
df_life_expecancy = pd.read_excel(PATH + "gapminder_lifeexpectancy.xlsx")
df_population     = pd.read_excel(PATH + "gapminder_population.xlsx")
df_fertility      = pd.read_csv(  PATH + "gapminder_total_fertility.csv")
df_continents     = pd.read_csv(  PATH + "continents.csv", sep=";")

for df in [df_fertility, df_population,df_life_expecancy]:
    df.set_index(df.columns[0], inplace=True)  # set index to first column
    df.index.name="country"                    # set index name to "country"
    df.columns=df.columns.astype(int)          # ensure datatype int for years
    df.reset_index(inplace=True)               # reset index


# melt wide to long format
df_fertility_long      =      df_fertility.melt(id_vars = "country", var_name = "year", value_name = "fertility rate" )
df_life_expecancy_long = df_life_expecancy.melt(id_vars = "country", var_name = "year", value_name = "life expectancy")
df_population_long     =     df_population.melt(id_vars = "country", var_name = "year", value_name = "population"     )


# merge datasets
df_gapminder = df_fertility_long.merge( df_life_expecancy_long, on= ["country", "year"])
df_gapminder =      df_gapminder.merge(     df_population_long, on= ["country", "year"], how="outer")  # use "outer" in order not to loose resolution in years
df_gapminder =      df_gapminder.merge(          df_continents, on= ["country"]        , how="left")


# Interpolation (since population has 10 year gaps before year 1950)
# do interpolation using groupby and apply

Groups=df_gapminder.groupby("country")
df_int=Groups.apply(pd.DataFrame.interpolate, limit_area="inside")

# sort and save
df_int.sort_values(by=["country", "year"], inplace=True)
df_int.to_csv("GAPMINDER_INT.csv")



###
# do interpolation using groupby and for loop (instead of apply --> doing apply manually)
# --> result is the same
#
#cdict={}
#for country,sub_df in Groups:
#    cdict[country]=sub_df
#
#
#
#for i, country in enumerate(cdict.keys()):
#    cur_df=cdict[country]
#    cur_df.interpolate(limit_area="inside", inplace=True)
#    if i==0: final_df=cur_df
#    if i>0:
#        final_df=pd.concat([final_df, cur_df])
#
#final_df.to_csv("GAPMINDER_INT.csv")
###
