
# %%
import matplotlib.pylab as plt
import numpy as np

# %% 

def generate_bar_chart(labels, values):
  fig, ax = plt.subplots()
  ax.bar(labels, values)
  plt.show()

