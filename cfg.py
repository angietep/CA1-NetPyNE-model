from netpyne import specs

#############################################
####		SIMULATION PARAMETERS		#####
#############################################

#SIMDUR = STARTDEL + (THETA*8)	// simulation duration (msecs)
simConfig = specs.SimConfig()

simConfig.dt = 0.05                 # Internal integration timestep to use
simConfig.verbose = 0
simConfig.duration = 1.0e3
simConfig.recordStim = True
simConfig.recordStep = 0.1             # Step size in ms to save data (e.g. V traces, LFP, etc)

simConfig.hParams['celsius'] = 34.

simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}} #, 'V_lmT':{'sec':'lm_thick1','loc':0.5,'var':'v'}}  # Dict with traces to record
simConfig.analysis['plotTraces'] = {'include': [('Pyramidal',[0,1]),('AA',0),('Basket',[0,1]),('OLM',0),('BS',0)], 'oneFigPer':'trace', 'overlay':1}
simConfig.analysis['plotRaster'] = True   # Plot a raster
#simConfig.analysis['plot2Dnet'] = True

simConfig.saveDataInclude=['simData']
#simConfig.saveJson=True
#simConfig.saveMat=True

# simConfig.recordLFP = [[netParams.sizeX/2, netParams.sizeY*1/4, netParams.sizeZ/2], 
# 						[netParams.sizeX/2, netParams.sizeY*2/4, netParams.sizeZ/2],
# 						[netParams.sizeX/2, netParams.sizeY*3/4, netParams.sizeZ/2]]

# simConfig.recordLFP = [[x,y,z] for x in range(900, netParams.sizeX, 900) for y in range(40, netParams.sizeY, 40) for z in range(40, netParams.sizeZ, 40)]
