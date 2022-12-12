import chart, util
import pandas as pd

def get_country_wPercentage(data):

    df = pd.read_csv(f"{data}.csv") #Conseguimos el dataframe
    region = 'South America'
    #Iteramos en el dataframe los diccionarios si tienen South America en el key Continent
    df = df[df['Continent'] == region]  
    #Enlistamos los values de los key Country del dataframe
    countries = df['Country/Territory'].values #Similar a map()
    #Enlistamos los values de los key World... del dataframe
    percentages = df['World Population Percentage'].values
    chart.generate_pie_chart(region, countries, percentages)
    
if __name__ == '__main__':
  get_country_wPercentage('world_population')