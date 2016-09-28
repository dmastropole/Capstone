
# coding: utf-8

# In[14]:

#for plotting
import numpy as np
import scipy.special
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

#for saving data
import pickle


# In[3]:

#pickle party paths
f = open('data.p', 'r')
df = pickle.load(f) 
f.close() 


# In[9]:

#output_notebook()


# In[12]:

#p = bp.figure(title="Price-Bedroom Comparison", x_axis_label='Number of Bedrooms', y_axis_label='Price [$/month]')
#r = p.scatter(df['br'], df.index, color='#2222aa')

#bp.show(p)


# In[17]:

plt.scatter(df['br'], df.index, color="blue", linewidth=3.0, linestyle="-")
plt.title('Sample Craigslist Data',fontsize=15,fontweight='bold')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Price [$/month]')
plt.show()


# In[20]:

plt.savefig('price_bdr.png')


# In[ ]:



