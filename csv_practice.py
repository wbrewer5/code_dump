import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#load in serratia qpcr data consisting of 3 columns
serratia = pd.read_csv("serratia_qpcr.csv")
print(serratia.head(10))

#split dataframe by molarity of primers
grouped = serratia.groupby(serratia.microMolar)
uM_100 = grouped.get_group(100)
template = uM_100['microgram template'].values.tolist()
print(template)
uM_100 = uM_100['Ct'].values.tolist()
print(uM_100)

uM_200 = grouped.get_group(200)
uM_200 = uM_200['Ct'].values.tolist()
print(uM_200)

uM_300 = grouped.get_group(300)
uM_300 = uM_300['Ct'].values.tolist()
print(uM_300)

serratia_fig, ax = plt.subplots()
ax.plot(template, uM_100, color='k', marker='+', label="100 uM")
ax.plot(template, uM_200, color='r', marker='2',label="200 uM")
ax.plot(template, uM_300, color='b', marker='.',label="300 uM")
ax.set_xscale('log')
ax.set_xlabel('micrograms of template')
ax.set_ylabel('Ct value')
ax.set_title('Efficiency Curves of Serratia Primers')
ax.legend()

plt.tight_layout()
plt.show()
#plt.plot(template, uM_100, label='100 uM')
#plt.plot(template, uM_200, label='200 uM')
#plt.plot(template, uM_300, label= '300 uM')

#plt.legend()
#plt.xlabel('microgram template')
#plt.ylabel('Ct')
#plt.title('Serratia Primer Efficiency')
#plt.tight_layout()
#plt.show()


