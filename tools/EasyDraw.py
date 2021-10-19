from ROOT import *
from utils import *
gStyle.SetOptStat(0)

f = TFile('/nfs/dust/cms/user/beinsam/pMSSM13TeV/Scan2/Recipes/NtupleMaker/CMSSW_10_2_21/src/TreeMaker/Production/test/NtupleStash/pMSSM_MCMC_86_7257-SUS-RunIIAutumn18FSPremix-00157.root')

tree = f.Get('TreeMaker2/PreSelection')
tree.Show(0)

c = mkcanvas('c1')
tree.Draw('MHT')

c1.Update()

hist = tree.GetHistogram().Clone('hist')
histoStyler(hist, kBlack)
hist.GetXaxis().SetTitle('MHT [GeV]')
hist.GetYaxis().SetTitle('Events/bin')
hist.SetTitle('')
hist.Draw('hist')

pause()
