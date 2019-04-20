from netpyne import sim, specs
from neuron import gui
import matplotlib.pyplot as plt
import numpy as np

netParams = specs.NetParams()


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
nPyramidal=100
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
netParams.popParams['Pyramidal'] = {'cellType': 'Pyramidalcell', 
	'numCells': nPyramidal, 
	'cellModel': 'Pyramidal_model', 
	'xRange':[2100, 2100], 
	'yRange':[0, 100], 
	'zRange':[0, 100]}#100cells
netParams.popParams['OLM'] = {'cellType': 
	'OLMcell', 'numCells': nOLM, 
	'cellModel': 'OLM_model', 
	'xRange':[2700, 2700], 
	'yRange':[0, 100], 
	'zRange':[0, 100]}
netParams.popParams['BS'] = {'cellType': 
	'BScell', 'numCells': nBS, 
	'cellModel': 'BS_model',
	 'xRange':[1600, 1600],
	  'yRange':[0, 100],
	   'zRange':[0, 100]}
netParams.popParams['Basket'] = {'cellType':
 	'Basketcell', 'numCells': nB, 
 	'cellModel': 'B_model', 
 	'xRange':[900, 900],
 	 'yRange':[0, 100],
 	  'zRange':[0, 100]}
netParams.popParams['AA'] = {'cellType': 
	'AAcell', 'numCells': nAA, 
	'cellModel': 'AA_model',
	 'xRange':[0, 0], 
	 'yRange':[0, 100], 
	 'zRange':[0, 100]}

#'cellModel': 'RegnStim' ##they use this other model (not NetStim) in their EC and CA3 cells.
netParams.popParams['EC']={'cellModel': 
'RegnStim', 'numCells': nEC, 'number': 1000, 'interval': GAMMA,'start': STARTDEL, 'noise': 0.2,\
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
netParams.importCellParams(label='Pyramidalcell', conds={'cellType': 'Pyramidalcell', 'cellModel': 'Pyramidal_model'}, \
fileName='pyramidal_cell_14Vb.hoc', cellName='PyramidalCell', importSynMechs=False)

netParams.importCellParams(label='OLMcell', conds={'cellType': 'OLMcell', 'cellModel': 'OLM_model'}, \
fileName='olm_cell2.hoc', cellName='OLMCell', importSynMechs=False)
#netParams.cellParams['OLMcell'].globals.Rm=20000.

netParams.importCellParams(label='BScell', conds={'cellType': 'BScell', 'cellModel': 'BS_model'}, \
fileName='bistratified_cell13S.hoc', cellName='BistratifiedCell', importSynMechs=False)

netParams.importCellParams(label='Basketcell', conds={'cellType': 'Basketcell', 'cellModel': 'B_model'}, \
fileName='basket_cell17S.hoc', cellName='BasketCell', importSynMechs=False)

netParams.importCellParams(label='AAcell', conds={'cellType': 'AAcell', 'cellModel': 'AA_model'}, \
fileName='axoaxonic_cell17S.hoc', cellName='AACell', importSynMechs=False)

##Setting thresholds

cells=['Pyramidalcell','OLMcell','BScell','Basketcell','AAcell']

for i in cells:
	for sec in netParams.cellParams[i].secs:
 		netParams.cellParams[i].secs[sec].threshold = -10.0

#############################################
####		NETWORK CONNECTIONS	#####
#############################################

weights={'Pyramidalcell2Pyramidalcell': 0.001, 'Pyramidalcell2AAcell':0.0005, 'Pyramidalcell2Basketcell':0.0005, 'Pyramidalcell2BScell':0.0005,'Pyramidalcell2OLMcell': 0.00005, \
'AAcell2Pyramidalcell': 0.04,\
'Basketcell2Pyramidalcell': 0.02, 'Basketcell2Basketcell': 0.001, 'Basketcell2BScell': 0.02,\
'BScell2Pyramidalcell': 0.002, 'BScell2Pyramidal_GABABasketcell': 0.0004, 'BScell2Basketcell': 0.01, \
'OLMcell2Pyramidalcell': 0.04, 'OLMcell2Pyramidal_GABABasketcell': 0.0004,'OLMcell2Basketcell': 0.01, }

delays={'Pyramidalcell2Pyramidalcell': 1., 'Pyramidalcell2AAcell':1., 'Pyramidalcell2Basketcell':1., 'Pyramidalcell2BScell':1.,'Pyramidalcell2OLMcell': 1., \
'AAcell2Pyramidalcell': 1., \
'Basketcell2Pyramidalcell': 1., 'Basketcell2Basketcell': 1., 'Basketcell2BScell': 1., \
'BScell2Pyramidalcell': 1., 'BScell2Pyramidal_GABABasketcell': 1., 'BScell2Basketcell': 1., \
'OLMcell2Pyramidalcell': 1., 'OLMcell2Pyramidal_GABABasketcell': 1.,'OLMcell2Basketcell': 1. }

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
##presyn = Pyramidal CHECKED
#######################

postsynList=['Pyramidal','AA','Basket','BS','OLM']
postsynDict={'Pyramidal':['radTprox'], 'AA': ['oriT1','oriT2'], 'Basket':['oriT1','oriT2'], 'BS':['oriT1','oriT2'], 'OLM':['dend1','dend2']}

for i in range(len(postsynList)):
	k='Pyramidalcell2'+postsynList[i]+'cell'
	netParams.connParams['Pyramidal->'+postsynList[i]] = {
		'preConds': {'pop': 'Pyramidal'},
		'postConds': {'pop': postsynList[i]},
		'sec': postsynDict[postsynList[i]],
		'synsPerConn':len(postsynDict[postsynList[i]]),
		'synMech': 'AMPA',
		'weight': weights[k],
		'delay': delays[k]
		#'threshold': -10.0
		}
	if postsynList[i]=='Pyramidal':
		netParams.connParams['Pyramidal->Pyramidal']['convergence'] = 1. # PC_PC = 1  // # of connections received by each PC from other PCs (excit)
	if postsynList[i]=='OLM':
		netParams.connParams['Pyramidal->OLM']['synMech'] = 'OLM_AMPA'
#FOR THE CONNECTIONS TO OLM CELLS THEY USE A DIFFERENT SYNAPSE MODEL


#######################
##presyn == AA CHECKED
#######################

netParams.connParams['AA->Pyramidal'] = {
        'preConds': {'pop': 'AA'},
        'postConds': {'pop': 'Pyramidal'},
        'sec': 'axon',
		'loc': 0.1,
        'synMech': 'GABAA',
        'weight': weights['AAcell2Pyramidalcell'],
        'delay': delays['AAcell2Pyramidalcell']
		#'threshold': -10.0
		}

#######################
##presyn == B CHECKED
#######################

postsynList=['Pyramidal','Basket','BS']		##B->AA not connected

for i in range(len(postsynList)):
	k='Basketcell2'+postsynList[i]+'cell'
	netParams.connParams['B->'+postsynList[i]] = {
			'preConds': {'pop': 'Basket'},
			'postConds': {'pop': postsynList[i]},
			'sec': 'soma',
			'synMech': 'GABAA',   #GABA-A
			'weight': weights[k],
			'delay': delays[k]
		#	'threshold': -10.0
			}
	if postsynList[i]=='BS': netParams.connParams['B->BS']['loc'] = 0.6

##WITH THIS LINE IT DOESNT CREATE THE B->B CONNECTION
##	elif postsynList[i]=='Basket': netParams.connParams['B->B']['convergence'] = 1. # BC_BC = 1  // # of connections received by each BC from other BCs (inhib)


#######################
##presyn == BS  CHECKED
#######################

##BS->AA & BS->BS not connected

netParams.connParams['BS->B'] = {
	'preConds': {'pop': 'BS'},
	'postConds': {'pop': 'Basket'},
	'sec': 'soma',
	'synMech': 'GABAA',
	'loc':0.6,
	'weight': weights['BScell2Basketcell'],
	'delay': delays['BScell2Basketcell']
	#'threshold': -10.0
	}


netParams.connParams['BS->Pyramidal'] = {
		'preConds': {'pop': 'BS'},
		'postConds': {'pop': 'Pyramidal'},
		'sec': 'radTmed',
		'synsPerConn':7,
		'loc':[[0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2],[0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]],
		'synMech': ['GABAA','GABAB'],
		'weight': [weights['BScell2Pyramidalcell'], weights['BScell2Pyramidal_GABABasketcell']],
		'delay': [delays['BScell2Pyramidalcell'],delays['BScell2Pyramidal_GABABasketcell']]
#		'threshold': -10.0
		}


#######################
##presyn == OLM  CHECKED
#######################

netParams.connParams['OLM->Pyramidal'] = {
		'preConds': {'pop': 'OLM'},
		'postConds': {'pop': 'Pyramidal'},
		'sec': ['lm_thick1','lm_thick2'],
		'synMech': ['GABAA','GABAB'],  #GABA-A,GABA-B
		'weight': [weights['OLMcell2Pyramidalcell'], weights['OLMcell2Pyramidal_GABABasketcell']],
		'delay': [delays['OLMcell2Pyramidalcell'],delays['OLMcell2Pyramidal_GABABasketcell']],
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

lista_EC2Pyramidal=[] #to check which pyr cells are active in the pattern

##each EC cell will stimulate every active pyr cell in the pattern
for i in range(nEC):
	for j in range(nPyramidal):
		if PATTS[PATTi][j]:
			lista_EC2Pyramidal.append([i,j])

netParams.connParams['EC->Pyramidal'] = {
		'preConds': {'pop': 'EC'},
		'postConds': {'pop': 'Pyramidal'},
		'connList':lista_EC2Pyramidal,
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
		'postConds': {'pop': ['Basket','AA']},
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
	for j in range(nPyramidal):
			if WGTCONN[i][j]:
				lista_CA3highW.append([i,j])
			else: lista_CA3lowW.append([i,j])

postsynList=['AA','Basket','BS']
postsynDict={'AA': ['radM1','radM2','radT1', 'radT2'], 'Basket':['radM1','radM2','radT1', 'radT2'], 'BS':['radM1','radM2','radT1', 'radT2']}

cellnums={'Basket':nB, 'AA': nAA, 'BS': nBS, 'OLM': nOLM}
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

netParams.connParams['CA3_highW->Pyramidal'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'Pyramidal'},
		'connList':lista_CA3highW,
		'sec': 'radTmed',
#		'synMech': 'AMPA',
		'synMech': 'STDP',
		'loc':0.5,
		'weight': CHWGT,
		'delay': CDEL
		#'threshold': 10.0
		}

netParams.connParams['CA3_lowW->Pyramidal'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'Pyramidal'},
		'connList':lista_CA3lowW,
		'sec': 'radTmed',
		'synMech': 'STDP',
		'loc':0.5,
		'weight': CLWGT,
		'delay': CDEL
		#'threshold': 10.0
		}

netParams.connParams['CA3_NMDA->Pyramidal'] = {
		'preConds': {'pop': 'CA3'},
		'postConds': {'pop': 'Pyramidal'},
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

postsynList=['AA','Basket','BS','OLM']
postsynDict={'AA': ['oriT1','oriT2'], 'Basket':['oriT1','oriT2'], 'BS':['oriT1','oriT2'], 'OLM':['soma']}
w_SEP={'AA': SEPWGT, 'Basket':SEPWGT, 'BS':SEPWGTL, 'OLM':SEPWGTL}

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
		netParams.connParams['SEP->OLM']['synMech'] = ['OLM_GABAA'] # connections to OLM use a differen synapse mode - check what are differences


