from netpyne import sim, specs
from neuron import gui
import matplotlib.pyplot as plt
import numpy as np

netParams = specs.NetParams()
simConfig = specs.SimConfig()

# In [7]: import json
# In [8]: print(json.dumps(netParams.cellParams,indent=4))


#############################################
####		POPULATION PARAMETERS		#####
#############################################

#I tried this because the plotshape plotting is giving me an error (populations' ranges are invalid), but it doesn't disappear with this either
#Anyway, the plot is shown correctly
netParams.sizeX=2700
netParams.sizeY=100
netParams.sizeZ=100

PATTi=0 #pattern to be read

#Amount of cells in the network
nPYR=100
nCA3=100
nEC=20 #must be equal to the active pyr cells in the pattern
nSEP=10
nOLM=1
nBS=1
nB=2
nAA=1

STARTDEL = 50.	# msecs
THETA = 250.	 # msecs (4 Hz)
GAMMA = 25.	 # msecs (40 Hz)
ECCA3DEL = 9.	# msecs


# Population parameters
netParams.popParams['PYR'] = {'cellType': 'PYRcell', 'numCells': nPYR, 'cellModel': 'PYR_model', 'xRange':[2100, 2100], 'yRange':[0, 100], 'zRange':[0, 100]}#100cells
netParams.popParams['OLM'] = {'cellType': 'OLMcell', 'numCells': nOLM, 'cellModel': 'OLM_model', 'xRange':[2700, 2700], 'yRange':[0, 100], 'zRange':[0, 100]}
netParams.popParams['BS'] = {'cellType': 'BScell', 'numCells': nBS, 'cellModel': 'BS_model', 'xRange':[1600, 1600], 'yRange':[0, 100], 'zRange':[0, 100]}
netParams.popParams['B'] = {'cellType': 'Bcell', 'numCells': nB, 'cellModel': 'B_model', 'xRange':[900, 900], 'yRange':[0, 100], 'zRange':[0, 100]}
netParams.popParams['AA'] = {'cellType': 'AAcell', 'numCells': nAA, 'cellModel': 'AA_model', 'xRange':[0, 0], 'yRange':[0, 100], 'zRange':[0, 100]}

#'cellModel': 'RegnStim' ##they use this other model (not NetStim) in their EC and CA3 cells.
netParams.popParams['EC']={'cellModel': 'RegnStim', 'numCells': nEC, 'number': 1000, 'interval': GAMMA,'start': STARTDEL, 'noise': 0.2,\
'xRange':[0, 500], 'yRange':[100, 150], 'zRange':[0, 100] }
netParams.popParams['CA3']={'cellModel': 'RegnStim', 'numCells': nCA3,  'number': 1000, 'interval': GAMMA,'start': STARTDEL+ECCA3DEL, 'noise': 0.2,\
'xRange':[500, 1000], 'yRange':[100, 150], 'zRange':[0, 100]}
netParams.popParams['SEP']={'cellModel': 'BurstStim2', 'numCells': nSEP, 'interval':20, 'number': 1000, 'start': STARTDEL+(THETA/12.), 'noise': 0.4,\
'burstint':2.*THETA/3.,'burstlen':THETA/3.,'xRange':[1000, 1500], 'yRange':[100, 150], 'zRange':[0, 100]}

#Due to 40% noise in the interspike intervals,
#the 10 spike trains in the septal population are asynchronous.


#############################################
####		IMPORT CELL PARAMETERS  #####
#############################################
netParams.importCellParams(label='PYRcell', conds={'cellType': 'PYRcell', 'cellModel': 'PYR_model'}, \
fileName='pyramidal_cell_14Vb.hoc', cellName='PyramidalCell', importSynMechs=False)

netParams.importCellParams(label='OLMcell', conds={'cellType': 'OLMcell', 'cellModel': 'OLM_model'}, \
fileName='olm_cell2.hoc', cellName='OLMCell', importSynMechs=False)
#netParams.cellParams['OLMcell'].globals.Rm=20000.

netParams.importCellParams(label='BScell', conds={'cellType': 'BScell', 'cellModel': 'BS_model'}, \
fileName='bistratified_cell13S.hoc', cellName='BistratifiedCell', importSynMechs=False)

netParams.importCellParams(label='Bcell', conds={'cellType': 'Bcell', 'cellModel': 'B_model'}, \
fileName='basket_cell17S.hoc', cellName='BasketCell', importSynMechs=False)

netParams.importCellParams(label='AAcell', conds={'cellType': 'AAcell', 'cellModel': 'AA_model'}, \
fileName='axoaxonic_cell17S.hoc', cellName='AACell', importSynMechs=False)

##Setting thresholds

cells=['PYRcell','OLMcell','BScell','Bcell','AAcell']

for i in cells:
	for sec in netParams.cellParams[i].secs:
 		netParams.cellParams[i].secs[sec].threshold = -10.0

#############################################
####		NETWORK CONNECTIONS	#####
#############################################

weights={'PYRcell2PYRcell': 0.001, 'PYRcell2AAcell':0.0005, 'PYRcell2Bcell':0.0005, 'PYRcell2BScell':0.0005,'PYRcell2OLMcell': 0.00005, \
'AAcell2PYRcell': 0.04,\
'Bcell2PYRcell': 0.02, 'Bcell2Bcell': 0.001, 'Bcell2BScell': 0.02,\
'BScell2PYRcell': 0.002, 'BScell2PYR_GABABcell': 0.0004, 'BScell2Bcell': 0.01, \
'OLMcell2PYRcell': 0.04, 'OLMcell2PYR_GABABcell': 0.0004,'OLMcell2Bcell': 0.01, }

delays={'PYRcell2PYRcell': 1., 'PYRcell2AAcell':1., 'PYRcell2Bcell':1., 'PYRcell2BScell':1.,'PYRcell2OLMcell': 1., \
'AAcell2PYRcell': 1., \
'Bcell2PYRcell': 1., 'Bcell2Bcell': 1., 'Bcell2BScell': 1., \
'BScell2PYRcell': 1., 'BScell2PYR_GABABcell': 1., 'BScell2Bcell': 1., \
'OLMcell2PYRcell': 1., 'OLMcell2PYR_GABABcell': 1.,'OLMcell2Bcell': 1. }

# Cue (CA3) excitation
CHWGT = 0.0015	#// cue weight
CLWGT = 0.0005	#// unlearnt weight (usually 0)
CNWGT = 0.0005	#// excitatory weights (NMDA)
CDEL = 1.	#// cue delay

#EC excitation
ECWGT = 0.0	# EC weight to PCs
#ECWGT = 0.001	# EC weight to PCs
ECDEL = 1.	# EC delay
EIWGT = 0.00015	# excitatory weights to INs
EIDEL = 1.	# delay (msecs)

# Septal inhibition
SEPWGT = 0.02	# SEP weight to BCs and AACs
SEPWGTL = 0.0002	# SEP weight to BSCs and OLMs
SEPDEL = 1.	# SEP delay


#############################################
#### DESCRIPTION OF SYNAPTIC MECHANISMS	#####
#############################################

###STDP configuration
STDPDFAC = 0.	# depression factor
STDPPFAC = 0.	# potentiation factor
#STDPDFAC = 0.2	# depression factor
#STDPPFAC = 1.0	# potentiation factor
AMPASUPP = 0.4	# fraction of AMPA during storage
STDPTHRESH = -55.	# voltage threshold for STDP
STDPSTART = STARTDEL+(THETA/2.)	# STDP starts at same time as EC input
STDPINT = THETA/2.	# STDP interburst (recall) interval
STDPLEN = THETA/2.	# STDP burst (storage) length

netParams.synMechParams['STDP']={'mod':'STDPE2', 'wmax': CHWGT, 'wmin':CLWGT,'d': STDPDFAC, 'p' : STDPPFAC, 'gscale': AMPASUPP, 'thresh': STDPTHRESH, \
'gbdel': STDPSTART, 'gbint': STDPINT, 'gblen': STDPLEN}
netParams.synMechParams['GABAA']={'mod':'MyExp2Syn', 'tau1':1.0, 'tau2':8.0, 'e':-75.0}
netParams.synMechParams['GABAB']={'mod':'MyExp2Syn', 'tau1':35.0, 'tau2':100.0, 'e':-75.0}
netParams.synMechParams['AMPA']={'mod':'MyExp2Syn', 'tau1':0.5, 'tau2':3.0, 'e':0.0}
netParams.synMechParams['NMDA']={'mod':'NMDA', 'tcon': 2.3, 'tcoff': 100.0, 'enmda': 0.0, 'gNMDAmax': 1.0, 'tauD': 800.0, 'tauF': 800.0, 'util': 0.3}

netParams.synMechParams['OLM_GABAA']={'mod':'Exp2Syn', 'tau1':1.0, 'tau2':8.0, 'e':-75.0}
netParams.synMechParams['OLM_GABAB']={'mod':'Exp2Syn', 'tau1':35.0, 'tau2':100.0, 'e':-75.0}
netParams.synMechParams['OLM_AMPA']={'mod':'Exp2Syn', 'tau1':0.5, 'tau2':3.0, 'e':0.0}


#netParams.synMechParams
####MyExp2Syn_0 == GABA-A  ==? Exp2Syn_1 == {tau2: 8.0, tau1: 1.0, e: -75.0}
####MyExp2Syn_1 == AMPA ==? Exp2Syn_2 == {tau2: 3.0, tau1: 0.5, e: 0.0}
####MyExp2Syn_2 == GABA-B ==? Exp2Syn_0 == {tau2: 100.0, tau1: 35.0, e: -75.0}
####NMDA_3 == NMDA
###THE EXP2SYN MECHS ARE USED FOR OLM CONNECTIONS ONLY

#######################
##presyn = PYR CHECKED
#######################

postsynList=['PYR','AA','B','BS','OLM']
postsynDict={'PYR':['radTprox'], 'AA': ['oriT1','oriT2'], 'B':['oriT1','oriT2'], 'BS':['oriT1','oriT2'], 'OLM':['dend1','dend2']}

for i in range(len(postsynList)):
	k='PYRcell2'+postsynList[i]+'cell'
	netParams.connParams['PYR->'+postsynList[i]] = {
		'preConds': {'pop': 'PYR'},
		'postConds': {'pop': postsynList[i]},
		'sec': postsynDict[postsynList[i]],
		'synsPerConn':len(postsynDict[postsynList[i]]),
		'synMech': 'AMPA',
		'weight': weights[k],
		'delay': delays[k]
		#'threshold': -10.0
		}
	if postsynList[i]=='PYR':
		netParams.connParams['PYR->PYR']['convergence'] = 1. # PC_PC = 1  // # of connections received by each PC from other PCs (excit)
	if postsynList[i]=='OLM':
		netParams.connParams['PYR->OLM']['synMech'] = 'OLM_AMPA'
#FOR THE CONNECTIONS TO OLM CELLS THEY USE A DIFFERENT SYNAPSE MODEL


#######################
##presyn == AA CHECKED
#######################

netParams.connParams['AA->PYR'] = {
        'preConds': {'pop': 'AA'},
        'postConds': {'pop': 'PYR'},
        'sec': 'axon',
		'loc': 0.1,
        'synMech': 'GABAA',
        'weight': weights['AAcell2PYRcell'],
        'delay': delays['AAcell2PYRcell']
		#'threshold': -10.0
		}

#######################
##presyn == B CHECKED
#######################

postsynList=['PYR','B','BS']		##B->AA not connected

for i in range(len(postsynList)):
	k='Bcell2'+postsynList[i]+'cell'
	netParams.connParams['B->'+postsynList[i]] = {
			'preConds': {'pop': 'B'},
			'postConds': {'pop': postsynList[i]},
			'sec': 'soma',
			'synMech': 'GABAA',   #GABA-A
			'weight': weights[k],
			'delay': delays[k]
		#	'threshold': -10.0
			}
	if postsynList[i]=='BS': netParams.connParams['B->BS']['loc'] = 0.6

##WITH THIS LINE IT DOESNT CREATE THE B->B CONNECTION
##	elif postsynList[i]=='B': netParams.connParams['B->B']['convergence'] = 1. # BC_BC = 1  // # of connections received by each BC from other BCs (inhib)


#######################
##presyn == BS  CHECKED
#######################

##BS->AA & BS->BS not connected

netParams.connParams['BS->B'] = {
	'preConds': {'pop': 'BS'},
	'postConds': {'pop': 'B'},
	'sec': 'soma',
	'synMech': 'GABAA',
	'loc':0.6,
	'weight': weights['BScell2Bcell'],
	'delay': delays['BScell2Bcell']
	#'threshold': -10.0
	}


netParams.connParams['BS->PYR'] = {
		'preConds': {'pop': 'BS'},
		'postConds': {'pop': 'PYR'},
		'sec': 'radTmed',
		'synsPerConn':7,
		'loc':[[0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2],[0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]],
		'synMech': ['GABAA','GABAB'],
		'weight': [weights['BScell2PYRcell'], weights['BScell2PYR_GABABcell']],
		'delay': [delays['BScell2PYRcell'],delays['BScell2PYR_GABABcell']]
#		'threshold': -10.0
		}


#######################
##presyn == OLM  CHECKED
#######################

netParams.connParams['OLM->PYR'] = {
		'preConds': {'pop': 'OLM'},
		'postConds': {'pop': 'PYR'},
		'sec': ['lm_thick1','lm_thick2'],
		'synMech': ['GABAA','GABAB'],  #GABA-A,GABA-B
		'weight': [weights['OLMcell2PYRcell'], weights['OLMcell2PYR_GABABcell']],
		'delay': [delays['OLMcell2PYRcell'],delays['OLMcell2PYR_GABABcell']],
		'synsPerConn':21
		#'threshold': -10.0
		}


#############################################
####		STIMULATION - INPUTS		#####
#############################################


#####################################
#####EC input to active pyramidal cells
#####################################

FPATT = "Weights/pattsN100S20P5.dat"	#already stored patterns: each column is a pattern. Each line is a CA1 pyramidal cell
PATTS = np.transpose(np.loadtxt(fname=FPATT, dtype='int16')) #each column is a pattern - 100 lines (one per pyramidal cell)

lista_EC2PYR=[] #to check which pyr cells are active in the pattern

##each EC cell will stimulate every active pyr cell in the pattern
for i in range(nEC):
	for j in range(nPYR):
		if PATTS[PATTi][j]:
			lista_EC2PYR.append([i,j])

netParams.connParams['EC->PYR'] = {
		'preConds': {'pop': 'EC'},
		'postConds': {'pop': 'PYR'},
		'connList':lista_EC2PYR,
		'sec': ['lm_thick1','lm_thick2'],
		'synMech': 'AMPA',
		'loc':0.5,
		'weight': ECWGT,
		'delay': ECDEL,
		'synsPerConn':2
		#'threshold': 10.0
		}


##############################
### EC to inhibitory neurons --
##############################

netParams.connParams['EC->IN'] = {
		'preConds': {'pop': 'EC'},
		'postConds': {'pop': ['B','AA']},
		'sec': ['lmM1','lmM2'],
		'synMech': 'AMPA',
		'weight': EIWGT,
		'delay': EIDEL,
		'synsPerConn':2
		#'threshold': -10.0
		}

######################
####CA3 EXCITATION
#####################

FCONN = "Weights/wgtsN100S20P5.dat"		#weights matrix generated with matlab file
#WGTCONN = np.transpose(np.loadtxt(fname=FCONN, dtype='int16')) #each column has the weights for one pyramidal cell
WGTCONN = (np.loadtxt(fname=FCONN, dtype='int16')) #each column has the weights for one pyramidal cell

#############################
####CA3 -> INHIBITORY CELLS
############################

lista_CA3active=[]
###connect CA3 input to all pyramidal cells but with different weights according to the WGTCONN[i][j] value
lista_CA3highW=[]
lista_CA3lowW=[]

for i in range(nCA3):
	if PATTS[PATTi][i]:    ##ONLY CONNECTIONS FROM ACTIVE CA3 CELLS IN THE PATTERN
		lista_CA3active.append(i)

for i in lista_CA3active:  ##ONLY CONNECTIONS FROM ACTIVE CA3 CELLS IN THE PATTERN
	for j in range(nPYR):
			if WGTCONN[i][j]:
				lista_CA3highW.append([i,j])
			else: lista_CA3lowW.append([i,j])

postsynList=['AA','B','BS']
postsynDict={'AA': ['radM1','radM2','radT1', 'radT2'], 'B':['radM1','radM2','radT1', 'radT2'], 'BS':['radM1','radM2','radT1', 'radT2']}

cellnums={'B':nB, 'AA': nAA, 'BS': nBS, 'OLM': nOLM}
list=[]
connections={}

for j in postsynList:
	num=0
	list=[]
	connections[j]= list
	for i in range(cellnums[j]):
		for k in lista_CA3active: list.append([k,i])


for i in range(len(postsynList)):
	k='CA3cell2'+postsynList[i]+'cell'
	netParams.connParams['CA3->'+postsynList[i]] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': postsynList[i]},
		'connList':connections[postsynList[i]],
		'sec': postsynDict[postsynList[i]],
		'synsPerConn':len(postsynDict[postsynList[i]]),
		'synMech': 'AMPA',
		'weight': EIWGT,
		'delay': EIDEL,
		'loc':0.5
		#'threshold': -10.0
		}

netParams.connParams['CA3_highW->PYR'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'PYR'},
		'connList':lista_CA3highW,
		'sec': 'radTmed',
#		'synMech': 'AMPA',
		'synMech': 'STDP',
		'loc':0.5,
		'weight': CHWGT,
		'delay': CDEL
		#'threshold': 10.0
		}

netParams.connParams['CA3_lowW->PYR'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'PYR'},
		'connList':lista_CA3lowW,
		'sec': 'radTmed',
		'synMech': 'STDP',
		'loc':0.5,
		'weight': CLWGT,
		'delay': CDEL
		#'threshold': 10.0
		}

netParams.connParams['CA3_NMDA->PYR'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'PYR'},
		'sec': 'radTmed',
		'connList':lista_CA3highW+lista_CA3lowW,
		'synMech': 'NMDA',
		'loc':0.5,
		'weight': CNWGT,
		'delay': CDEL
		#'threshold': 10.0
		}


#######################
## Septal inhibition
#######################

postsynList=['AA','B','BS','OLM']
postsynDict={'AA': ['oriT1','oriT2'], 'B':['oriT1','oriT2'], 'BS':['oriT1','oriT2'], 'OLM':['soma']}
w_SEP={'AA': SEPWGT, 'B':SEPWGT, 'BS':SEPWGTL, 'OLM':SEPWGTL}

## CHECKED
for i in range(len(postsynList)):
	netParams.connParams['SEP->'+postsynList[i]] = {
		'preConds': {'pop': 'SEP'},
		'postConds': {'pop': postsynList[i]},
		'sec': postsynDict[postsynList[i]],
		'loc':0.6,
		'synMech': ['GABAA'], #,'MyExp2Syn_2'],  #GABA-A, GABA-B
		'synsPerConn':len(postsynDict[postsynList[i]]),
		'weight': w_SEP[postsynList[i]],
		'delay': SEPDEL
		#'threshold': -10.0
		}
	if postsynList[i]=='OLM':
		netParams.connParams['SEP->OLM']['loc'] = 0.5
		netParams.connParams['SEP->OLM']['synMech'] = ['OLM_GABAA']
	###	FOR THE CONNECTIONS TO OLM CELLS THEY USE A DIFFERENT SYNAPSE MODEL. I DON'T KNOW WHAT IS THE DIFFERENCE


#############################################
####		SIMULATION PARAMETERS		#####
#############################################

#SIMDUR = STARTDEL + (THETA*8)	// simulation duration (msecs)


simConfig.dt = 0.05                 # Internal integration timestep to use
simConfig.verbose = 0
simConfig.duration = 1.0e3
simConfig.recordStim = True
simConfig.recordStep = 0.1             # Step size in ms to save data (e.g. V traces, LFP, etc)

simConfig.hParams['celsius'] = 34.

simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}, 'V_lmT':{'sec':'lm_thick1','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.analysis['plotTraces'] = {'include': [('PYR',[0,1]),('AA',0),('B',[0,1]),('OLM',0),('BS',0)], 'oneFigPer':'trace', 'overlay':1}
simConfig.analysis['plotRaster'] = True   # Plot a raster
#simConfig.analysis['plot2Dnet'] = True

simConfig.saveDataInclude=['simData']
#simConfig.saveJson=True
#simConfig.saveMat=True

# simConfig.recordLFP = [[netParams.sizeX/2, netParams.sizeY*1/4, netParams.sizeZ/2],
# 						[netParams.sizeX/2, netParams.sizeY*2/4, netParams.sizeZ/2],
# 						[netParams.sizeX/2, netParams.sizeY*3/4, netParams.sizeZ/2]]
#
# simConfig.recordLFP = [[x,y,z] for x in range(900, netParams.sizeX, 900) for y in range(40, netParams.sizeY, 40) for z in range(40, netParams.sizeZ, 40)]


sim.createSimulateAnalyze(netParams, simConfig)


sim.analysis.plotConn(graphType='matrix', saveFig=1)
sim.analysis.plotConn(graphType='bar', saveFig=1)
sim.analysis.plotSpikeStats(stats = ['rate', 'isicv', 'sync', 'pairsync'], saveFig=1)
# sim.analysis.plotLFP(NFFT=256*10, noverlap=48*10, nperseg=64*10, saveFig=True)
sim.analysis.granger(cells1=['EC'], cells2=['PYR'], label1='EC', label2='PYR')


#sim.saveData()
#sim.create()
#sim.analysis.plot2Dnet(include = ['AA', ('EC',[0,1,2]),('PYR',[0,1,2]), ('CA3',[0,1,2])])
#sim.analysis.plotConn()
#sim.analysis.plotShape(includePost= ['PYR','AA','B','BS','OLM'], showFig=True, includeAxon=True, showSyns=True)
#sim.analysis.plotRaster(include = ['SEP','EC','CA3'])

#sim.allSimData.V_soma.cell_1
#sim.net.pops.AA.cellGids

#plotConn(include = ['allCells'], feature='strength', groupBy= 'pop', figSize=(9,9), showFig=True)
