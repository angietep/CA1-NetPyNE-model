import json
import numpy as np
from netpyne import sim,specs
from matplotlib import pyplot as plt


#fname =  'onlyBCS-20180131_185432.json'

fname = 'halfECs--2200-20180202_140402.json'

# fname = 'noEC-20180131_183336.json'

# fname = 'fullnet-20180201_130603.json'
# fname = 'noEC-20180131_183336.json'

CA3patt = [1, 2, 7, 11, 21, 28, 35, 38, 39, 43, 46, 49, 56, 57, 59, 62, 78, 81, 88, 90]
CA3patt = np.array(CA3patt) + 105



# Index of neurons types
pyr = [0,99]
olm = 100
bs = 101
b = [102,103]
aa = 104
ec = [105,124]
ca3 = [125,224]
sep = [225,234]


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


#------------------#

spkt = np.array(spkt)
spkid = np.array(spkid)

pyr = np.array(range(0,100))
olm = np.array(100)
bs = np.array(101)
b = np.array(range(102,104))
aa = np.array(104)
ec = np.array(range(105,125))
ca3 = np.array(range(125,225))
sep = np.array(range(225,235))


Index=[[None] for i in range(235)]
for i in range(235):
	Index[i]=np.where(spkid==i)[0]

IndexT=[[None] for i in range(235)]
for i in range(235):
	IndexT[i]=spkt[Index[i]]

import matplotlib.pyplot as plt


plt.figure(figsize= [20,8],facecolor= 'w')
for n in range(105+99,125+99):
	for t in IndexT[n]:
		plt.subplot(3,1,1)
		plt.subplots_adjust(hspace=0.5) 
		plt.plot(t,n,'.',color='k')
		plt.xticks(xtick)
		plt.title('(a) Input spikes',fontweight='bold')
		plt.ylabel('Cell no.',fontweight='bold')
		plt.xlim(200,2000)
		plt.ylim(100,234)
for n in CA3patt:
	for t in IndexT[n]:
		plt.subplot(3,1,1)
		plt.plot(t,n,'.',color='k')
		plt.xticks(xtick)
		plt.xlim(200,2000)
		plt.ylim(100,234)
for n in range(225,235):
	for t in IndexT[n]:
		plt.subplot(3,1,1)
   		plt.plot(t,n,'.',color='k')
   		plt.xticks(xtick)
		plt.xlim(200,2000)
		plt.ylim(100,234)

for n in range(1,99):
	for t in IndexT[n]:
		plt.subplot(3,1,2)
		plt.plot(t,n,'.',color='k')
		plt.title('(b) Pyramidal cell spikes',fontweight='bold')
		plt.ylabel('Cell no.',fontweight='bold')
   		plt.xticks(xtick)
		plt.xlim(200,2000)
		plt.ylim(0,100)
		plt.yticks([0,50])
		
		

n = []
spks = []
neur = []
for i in range(0,99):
	spks.extend(IndexT[i])
plt.subplot(3,1,3)
plt.subplots_adjust(hspace=0.5) 
plt.hist(spks,bins = 300,histtype='step',color='k')
plt.xlim([200,2000])
plt.title('(c) PC spike count',fontweight='bold')
plt.ylabel('Spike count',fontweight='bold')
plt.xticks(xtick)
plt.yticks([0,50,100])
plt.ylim(0,100)	

plt.show()
# bins = 300
# pat = np.ones(bins) * len(CA3patt)
# a,b = np.histogram(spks,bins)

# c =np.ones(bins)
# for p in range(1,bins):
# 	c[p] = a[p]/pat[p]

# t = np.arange(0,2200,(2200/bins))
# t = t[0:300]

# plt.xlabel('Time(msecs)',fontweight='bold')
# plt.subplot(4,1,4)
# plt.plot(t,c,color='k')
# plt.xlim([200,2000])
# plt.title('(d) Recall quality',fontweight='bold')
# plt.ylabel('Quality',fontweight='bold')
# plt.xticks(xtick)
# plt.yticks([0,0.5,1])
# plt.ylim(0,1)	
# plt.show()
