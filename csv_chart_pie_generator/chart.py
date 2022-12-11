
# %%
import matplotlib.pylab as plt
import numpy as np

# %% 

def generate_pie_chart(labels, values):
  fig, ax = plt.subplots()
  ax.pie(values, labels = labels)
  ax.axis('equal')
  plt.show()

