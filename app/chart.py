
import matplotlib.pylab as plt
import numpy as np


def generate_pie_chart(name, labels, values):
  fig, ax = plt.subplots()
  ax.pie(values, labels = labels)
  plt.title('World Population Percentage')
  plt.savefig(f'./imgs/{name}.png')
