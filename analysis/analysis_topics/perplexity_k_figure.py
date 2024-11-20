import csv
import numpy as np
import matplotlib.pyplot as plt

# render fonts in latex style
plt.rc('text', usetex=True)

# Read data from csv file
with open('perplexity_k.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

# Convert data to numpy array
data = np.array(data).astype(float)
n_topics = np.linspace(10, 201, 20)

# Plot data
plt.figure(figsize=(8,4))
# perplexity over number of topics
plt.plot(n_topics, data[:,0], label='perplexity')
plt.xlabel('NUMBER OF TOPICS', fontsize=14)
# dashed vertical line at x=100
plt.axvline(x=100, color='k', linestyle='--')
# ticklabels in fontsize 12
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('perplexity_convergence.png')
plt.savefig('perplexity_convergence.eps')



