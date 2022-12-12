import chart, util

def get_country_wPercentage(data):
  key = list(map(lambda element : element['Country/Territory'], data))
  wPercentage = list(map(lambda element : element['World Population Percentage'],data))
  chart.generate_pie_chart(key, wPercentage)


if __name__ == '__main__':
  data = util.read_csv('world_population.csv')
  get_country_wPercentage(data)