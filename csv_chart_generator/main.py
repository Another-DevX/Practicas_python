import chart, util
import util

def select_country(data):
    search_country = input('Write your country').title()
    country = list(filter(lambda iterator_country: iterator_country['Country/Territory'] == search_country ,data))
    return country

def population_search(country):
    country_items = country[0].items()
    population_history = {key[0:4]:float(item) for (key, item) in country_items if  'Population' in key and 'World' not in key}
    return(population_history)




if __name__ == '__main__':
    data = util.read_csv('../csv_chart_generator/world_population.csv')
    country = select_country(data)
    population = population_search(country)
    chart.generate_bar_chart(list(population.keys()),list(population.values()))
    

