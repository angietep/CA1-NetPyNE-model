
import json
import numpy as np
from netpyne import sim,specs
from matplotlib import pyplot as plt


#fname =  'onlyBCS-20180131_185432.json'

fname = 'noINHs--2200-20180201_205056.json'
# fname = 'fullnet-20180201_130603.json'
# fname = 'noEC-20180131_183336.json'

CA3patt = [1, 2, 7, 11, 21, 28, 35, 38, 39, 43, 46, 49, 56, 57, 59, 62, 78, 81, 88, 90]

# Index of neurons types
pyr = [0,99]
olm = 100
bs = 101
b = [102,103]
aa = 104
ec = [105,124]
ca3 = [125,224]
sep = [225,244]


xtick = np.arange(200,2200,200) #tick labels

# simConfig = sim.loadSimCfg(fname) # not working
# netParams = sim.loadNetParams(fname) #not working

#Loading json file
json_data=open(fname).read()
data = json.loads(json_data)

simConfig = data['simConfig'] # loading simConfig
netParams = data['net'] # loading netParams
data = data['simData'] # loading simData

# Splinting data spks, spks ids, voltages on the soma
spkt = data['spkt']
spkid = data['spkid']
v_soma = data['V_soma']

# Creating lists np
neurons = np.unique(spkid)
neuron= []
vneurons = v_soma.keys()
vneuron = []

for n in neurons:
	neuron.append( [ii for ii, nr in enumerate(spkid) if nr==n])
for v in vneurons:	
	vneuron.append(v_soma[v])


# Plotting rasters
plt.scatter(spkt,spkid,c='k',s=1)
plt.xticks(xtick)
plt.xlim(200,2250)
plt.ylim(0,250)

# Plotting voltages
plt.figure(figsize= [20,8],facecolor= 'w')

plt.subplot(5,1,1)
plt.subplots_adjust(hspace=0.5) 
plt.plot(v_soma['cell_1'],color='k')
plt.title('(a) Pattern pyramidal cell')
plt.yticks([-80,-60,-40,-20,0,20])
plt.ylabel('V(mV)')
plt.xticks(xtick)
plt.xlim(200,2250)


plt.subplot(5,1,2)
plt.plot(v_soma['cell_104'],color='k')
plt.title('(b) Axo-Axonic cell')
plt.yticks([-50,0,50])
plt.xticks(xtick)
plt.ylabel('V(mV)')
plt.xlim(200,2250)

plt.subplot(5,1,3)
plt.plot(v_soma['cell_102'],color='k')
plt.title('(c) Basket cell')
plt.yticks([-50,0,50])
plt.xticks(xtick)
plt.ylabel('V(mV)')
plt.xlim(200,2250)

plt.subplot(5,1,4)
plt.plot(v_soma['cell_101'],color='k')
plt.title('(d) Bistratified cell')
plt.yticks([-50,0,50])
plt.xticks(xtick)
plt.ylabel('V(mV)')
plt.xlim(200,2250)

plt.subplot(5,1,5)
plt.plot(v_soma['cell_100'],color='k')
plt.title('(e) OLM cell')
plt.yticks([-50,0,50])
plt.xlabel('Time(msec)') 
plt.xticks(xtick)
plt.ylabel('V(mV)')
plt.xlim(200,2250)
# count = 1
# for v in range(len(vneuron)):
# 	plt.subplot(len(vneuron),1,v+1)
# 	plt.plot(vneuron[v])
# 	count = count +1 

plt.show()

