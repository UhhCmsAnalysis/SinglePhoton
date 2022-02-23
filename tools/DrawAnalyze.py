import os, sys
from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

'''
rm output/mediumchunks/*
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-Autumn18.GJets_DR-0p4_HT-600ToInf_Tune*.root"
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-Autumn18.ZGTo2NuG_Tune*.root"
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-pMSSM_MCMC_86_7257*.root"


rm output/bigchunks/*
hadd -f output/bigchunks/Autumn18.GJets.root output/mediumchunks/*Autumn18.GJets_DR-0p4_HT*.root
hadd -f output/bigchunks/Autumn18.ZGTo2NuG.root output/mediumchunks/*Autumn18.ZGTo2NuG_Tune*.root
hadd -f output/bigchunks/2018Observed.root output/bigchunks/*.root
rm output/signals/*
cp output/mediumchunks/weightedHists*pMSSM_MCMC*.root output/signals/

'''

try: fileskey = sys.argv[1]
except: fileskey = '/eos/uscms//store/user/sbein/RebalanceAndSmear/Run2ProductionV17/*Summer16v3.QCD*.root'


print 'fileskey', fileskey
if 'Run20' in fileskey: isdata = True
else: isdata = False




pixelseedstring = "&& (Pho1_hasPixelSeed==0)"
showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==1)"
universalconstraint = ' abs(HardMetMinusMet)<100 && mva_Photons1Et>20 && mva_Ngoodjets>1' + showershapestring
universalconstraint
universalconstraint += pixelseedstring


fins = glob(fileskey)
if not isdata:
    ccounter = TChain('tcounter')
    for fname in fins: ccounter.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
    nev_total = ccounter.GetEntries()
    print 'nevents in total =', nev_total
    
chain = TChain('TreeMaker2/PreSelection')
print 'fileskey', fileskey
for fname in fins: chain.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
chain.Show(0)
print 'nevents in skim =', chain.GetEntries()


isprivatesignal = bool('pMSSM' in fins[0])
if isprivatesignal:
    xsecdict = {'pMSSM_MCMC_106_19786': 1.26100000e-01, 'pMSSM_MCMC_399_10275': 3.98200000e-02, 'pMSSM_MCMC_473_54451': 9.87200000e-01, 'pMSSM_MCMC_86_7257': 2.99100000e-03, 'pMSSM_MCMC_70_90438':7.52100000e-01}
    thekey = 'pMSSM'+fname.split('pMSSM')[-1].split('-SUS')[0]
    xsec = xsecdict[thekey]
    evtweight = str(xsec)+'/'+str(nev_total)
    print 'the key', thekey, 'got weight', xsec
elif isdata: evtweight = '1'
else: evtweight = 'CrossSection/'+str(nev_total)



promptname = 'Photons_nonPrompt'
#promptname = 'Photons_genMatched'
WP = 'Medium/2'
WP = 'Loose'



plotBundle = {}


#2d plots
plotBundle['OnePho_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_HardMet'] = ['min(HardMETPt,999)>>hadchadc(20,0,1000)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_NJets'] = ['min(mva_Ngoodjets,9)>>hadc(11,-1,10)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_Pho1Pt'] = ['min(analysisPhotons[0].Pt(),499.9)>>hadc(100,0,500)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_Eta1Pt'] = ['min(analysisPhotons[0].Eta(),499.9)>>hadc(25,-5,5)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_HT'] = ['mva_ST_jets>>hadc(10,100,2300)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_ST'] = ['mva_ST>>hadc(10,100,2300)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_nPhotons'] = ['NPhotons>>hadc(3,1,4)','HardMETPt>200 && NPhotons>=1',False]


infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')
newfilename = 'output/mediumchunks/weightedHists_'+infilekey+'.root'
if 'T5' in infilekey or 'T6' in infilekey: newfilename = newfilename.replace('mediumchunks','signals')

    
fnew = TFile(newfilename, 'recreate')
print 'will make file', fnew.GetName()
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, blinding = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ' && IsRandS==0)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', obsweight
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    if not ('Vs' in key): hobs.GetYaxis().SetRangeUser(0.01,10000*hobs.GetMaximum())

    c1.cd()

    drawarg = drawarg
    randsconstraint = constraint
    methweight = evtweight+'/NSmearsPerEvent*('+ randsconstraint + ' && '+universalconstraint+ ' && IsRandS==1 && rebalancedHardMet<120)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', methweight
    chain.Draw(drawarg, methweight, 'e')
    hrands = chain.GetHistogram().Clone(key+'_rands') 
    if blinding and 'Run20' in fileskey: hobs = hrands.Clone(key+'_obs')
    if not ('Vs' in drawarg): hrands.GetYaxis().SetRangeUser(0.01,10000*hrands.GetMaximum())
    if 'ZGG' in fileskey: histoStyler(hrands, kViolet+1)
    else: histoStyler(hrands, kAzure-8)
    hrands.SetFillColor(hrands.GetLineColor())
    hrands.SetFillStyle(1001)

    leg = mklegend(x1=.45, y1=.57, x2=.95, y2=.74, color=kWhite)
    if 'ZGG' in fileskey: hobs.SetTitle('Summer16 ZGG')
    else: hobs.SetTitle('observed')
    hobs.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.SetTitle('rebalance and smeared')        
    hrands.Write('h'+hrands.GetName())
    hobs.Write('h'+hobs.GetName())






print 'just created', fnew.GetName()
fnew.Close()

