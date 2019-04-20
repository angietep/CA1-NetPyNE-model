from netpyne import sim
from cfg import simConfig
from netParams import netParams

sim.createSimulateAnalyze(netParams, simConfig)


# additional plots
#sim.analysis.plotTraces([('Pyramidal',1),('Basket',0)], saveFig=1, oneFigPer='trace', overlay=0)
# sim.analysis.plotConn(graphType='matrix', saveFig=1)
# sim.analysis.plotConn(graphType='bar', saveFig=1)
# sim.analysis.plotSpikeStats(stats = ['rate', 'isicv', 'sync', 'pairsync'], saveFig=1)
# sim.analysis.plotLFP(NFFT=256*10, noverlap=48*10, nperseg=64*10, saveFig=True)
# sim.analysis.granger(cells1=['EC'], cells2=['Pyramidal'], label1='EC', label2='Pyramidal')

# create and plot
#sim.saveData()
#sim.create()
#sim.analysis.plot2Dnet(include = ['AA', ('EC',[0,1,2]),('Pyramidal',[0,1,2]), ('CA3',[0,1,2])])
#sim.analysis.plotConn(include = ['allCells'], feature='strength', groupBy= 'pop', figSize=(9,9), showFig=True)
#sim.analysis.plotShape(includePost= ['Pyramidal','AA','Basket','BS','OLM'], showFig=True, includeAxon=True, showSyns=True)
#sim.analysis.plotRaster(include = ['CA3', lista_CA3active])
