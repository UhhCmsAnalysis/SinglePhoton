from ROOT import *
from utils import *
import os,sys
from glob import glob
gROOT.SetBatch(1)

datamc = 'data'
datamc = 'mc'



finalstate = 'pho'


try: year = sys.argv[1]
except:
    year = '2017'
    year = '2016'
    year = '2018'    

mcstring = {}
mcstring['2016'] = 'Summer16v3'
#mcstring['2017'] = 'Fall17'
mcstring['2017'] = 'Summer16v3'
mcstring['Run2'] = 'Summer16v3'
mcstring['2018'] = 'Autumn18'

    
prediction_sources = {}
histOfFile = {}
#prediction_sources['FakeMet']         = 'output/bigchunks/'+mcstring[year]+'.GJets.root'


#prediction_sources['t#bar{t}+jets'] = 'output/bigchunks/'+mcstring[year]+'.TTJets.root'
#prediction_sources['W+jets'] = 'output/bigchunks/'+mcstring[year]+'.WJetsToLNu.root'
prediction_sources['#gamma+jets'] = 'output/bigchunks/'+mcstring[year]+'.GJets.root'
prediction_sources['Z#gamma+jets'] = 'output/bigchunks/'+mcstring[year]+'.ZGTo2NuG.root'
    
        

colors = [2,4, kTeal-5, kYellow+2, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]

#fkeys = [['W+jets',kYellow+1],['GJets',kOrange+1], ['t#bar{t}+jets',kTeal-5], ['ZG+jets', kViolet+2]]#,['WJets',kYellow+1]
fkeys = [['#gamma+jets',kOrange+1], ['Z#gamma+jets', kViolet+2]]



#signals = glob('output/signals/weighted*.root')
signals = ['output/signals/weightedHists_posterior-pMSSM_MCMC_86_7257.root']
    
sigcolors = [kRed+1, kMagenta, kTeal-5]

if year=='2016':
    lumi = 35.9 # 2016 
    datasource = 'output/bigchunks/Run2016_DoubleEG.root'
if year=='2017':
    datasource = 'output/bigchunks/Run2017_Photon.root'
    datasource = 'output/bigchunks/Run2017_DoubleEG.root'
    lumi = 41.52
if year=='2018':
    datasource = 'output/bigchunks/2018Observed.root'
    lumi = 54.52
if year=='Run2':
    datasource = 'output/bigchunks/Run2_DoubleEG.root'
    lumi = 131.94
if year=='2018A':
	lumi = 13.95
if year=='2018D':
	lumi = 31.74
if year=='2018C':
	lumi = 6.89

    
fdata = TFile(datasource)
fdata.ls()
keys = fdata.GetListOfKeys()
keys = sorted(keys,key=lambda thing: thing.GetName())

redoBinning = {}

linscale = False

gStyle.SetOptStat(0)
gROOT.ForceStyle()

newfile = TFile('plots_'+year+'_'+finalstate+'.root','recreate')

fkeys.reverse()

for key in keys:
    name = key.GetName()
    if 'Vs' in name: continue
    if not name[0]=='h': continue
    if not 'obs' in name: continue
    hObserved = fdata.Get(name).Clone()
    if datamc=='mc': hObserved.Scale(1000*lumi)
    print 'here we are', name

    hObserved.SetTitle('Data ('+year+')')
    histoStyler(hObserved, 1)
    hpreds = []
    
    for fkey, color in fkeys:
        fname_pred = prediction_sources[fkey]
        print 'fkey', fkey

        fname_pred = prediction_sources[fkey]
        fpred = TFile(fname_pred)
        thename = name
        
        print 'trying to get', thename, 'from', fpred.GetName()
        hpred = fpred.Get(thename)
        hpred.SetTitle(fkey)#namewizard(fname_pred.split('/')[-1].replace('.root',''))            
        
        hpred.Scale(1000*lumi)
        hpred.SetDirectory(0)
        
        histoStyler(hpred, color)     
        hpred.SetFillColor(hpred.GetLineColor())
        hpreds.append(hpred)   
        hpreds[-1].SetDirectory(0)        
        fpred.Close()
    kinvar = name.split('_')[1]
    print 'found kinvar', kinvar, 'from', name
    cGold = TCanvas('cEnchilada','cEnchilada', 800, 800)
    if kinvar in redoBinning.keys():
        print 'redoing the binning', kinvar
        if len(redoBinning[kinvar])>3: ##this should be reinstated
            nbins = len(redoBinning[kinvar])-1
            newxs = array('d',redoBinning[kinvar])
        else:
            newbinning = []
            stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
            for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
            nbins = len(newbinning)-1
            newxs = array('d',newbinning)

            
        hObserved = hObserved.Rebin(nbins,'',newxs)
        for ih in range(len(hpreds)):  hpreds[ih] = hpreds[ih].Rebin(nbins,'',newxs)
                    

    if not linscale: hObserved.GetYaxis().SetRangeUser(max(0.0005,min(0.001, 0.01*hObserved.GetMinimum())),max(700000, 10*hObserved.GetMaximum()))

    newfile.cd()
        
    oldalign = tl.GetTextAlign()    
    tl.SetTextAlign(oldalign)
    leg = mklegend(x1=.62, y1=.5, x2=.9, y2=.8, color=kWhite)
    newfile.cd() 
    hratio, hmethodsyst = FabDrawSystyRatio(cGold,leg,hObserved,hpreds,datamc=datamc,lumi=str(lumi), title = '',LinearScale=linscale,fractionthing='observed/method')

    pad1, pad2 = hmethodsyst[-2], hmethodsyst[-1]
    
    for ih in range(len(hpreds)): 
        if linscale:            
            hpreds[ih].GetYaxis().SetRangeUser(0.0,2.0*hpreds[ih].GetMaximum())
        else:
            hpreds[ih].GetYaxis().SetRangeUser(0.02,20000000)

    pad1.cd()
    sighists = []
    leg2 = mklegend(x1=.16, y1=.58, x2=.5, y2=.82, color=kWhite)
    for isig, fsigname in enumerate(signals):
        print 'looking for', name, 'in', fsigname
        fsig = TFile(fsigname)
        hist = fsig.Get(name)
        hist.Scale(1000*lumi)
        if kinvar in redoBinning.keys(): hist = hist.Rebin(nbins,'',newxs)
        hist.SetDirectory(0)        
        histoStyler(hist, sigcolors[isig])
        #histoStyler(hist, kBlue+isig)
        hist.SetLineWidth(3)
        fsig.Close()
        sighists.append(hist)
        sighists[-1].Draw('hist same')
        leg2.AddEntry(hist, fsigname.split('/')[-1].split('weightedHists_posterior-')[-1].split('-SUS')[0].split('SMS-')[-1].split('_RA2')[0].replace('.root',''))
    leg2.Draw('same')
    hratio.GetYaxis().SetRangeUser(0.0,2.0)
    print 'setting', kinvar, 'title to', kinvar.replace('mva_','(for MVA) ')
    hratio.GetXaxis().SetTitle(kinvar.replace('mva_','(for MVA) '))
    cname = 'c_'+name[1:]
    newfile.cd()
    cGold.Write(cname)
    #print 'trying:','pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf'
    cGold.Print('figures/'+datasource.split('/')[-1].replace('.root','')+cname[1:]+'.png')


print 'just created', newfile.GetName()
'''
scp pdfs/Validation/ beinsam@naf-cms11.desy.de:/afs/desy.de/user/b/beinsam/www/Diphoton/Validation/23March2021/TwoElectrons/
'''






exit(0)




















