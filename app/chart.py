
import matplotlib.pylab as plt

def generate_bar_chart(name, labels, values):
  fig, ax = plt.subplots()
  ax.bar(labels, values)
  plt.title(name)
  plt.savefig(f'./imgs/{name}.png')
  plt.close()  

