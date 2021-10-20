# SinglePhoton

##
Here are some quick commands to get set up and rolling. To do once,
when it's your first time setting up CMSSW:
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src/
cmsenv
```

The last two commands should be run each time you log in. Then, if you need to check out the package the first time:
```
git clone https://github.com/UhhCmsAnalysis/SinglePhoton
cd SinglePhoton
mkdir output
mkdir output/smallchunks
mkdir output/mediumchunks
mkdir output/bigchunks
mkdir output/signals/
mkdir figures/
```

Now we should be ready to make plots. For a very straightforward
skeleton for drawing  a single plot on a canvas, you can test

```
python tools/EasyDraw.py
```

This script draws a histogram directly from a ROOT tree, then grabs
and styles the histogram on a canvas. The last function is
```pause```, and the idea is it halts the program where it is while
you can interact with canvases, or save them as pdfs, etc.

Now perhaps we can try creating a properly-weighted stack of
background events and comparing them to the signal model. First, let's
draw a suite of histograms, one set per distinct process, and
assuming there are only two backgrounds for the moment (there are
really more):


```
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-Autumn18.GJets_DR-0p4_HT-600ToInf_Tune*.root"
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-Autumn18.ZGTo2NuG_Tune*.root"
python tools/DrawAnalyze.py "/nfs/dust/cms/user/beinsam/CommonSamples/SinglePhoRandS_skimsv8/posterior-pMSSM_MCMC_86_7257*.root"
```

One file per command above has been created and cached away in
```output/mediumchunks/```. Now we can transfer the mediumchunks to
the bigchunks folder using ```hadd```, which does an object-by-object 
merging of root files. Also we can simply copy the signal file(s) into
the signals folder:

```
rm output/bigchunks/*
hadd -f output/bigchunks/Autumn18.GJets.root output/mediumchunks/*Autumn18.GJets_DR-0p4_HT*.root
hadd -f output/bigchunks/Autumn18.ZGTo2NuG.root output/mediumchunks/*Autumn18.ZGTo2NuG_Tune*.root
hadd -f output/bigchunks/2018Observed.root output/bigchunks/*.root
rm output/signals/*
cp output/mediumchunks/weightedHists*pMSSM_MCMC*.root output/signals/
```

Now things are ready to stack together and observe. You can do:
```
python tools/MakePlots.py
```

to produce a new root file containing a canvas per observable defined
in ```DrawAnalyze.py```. ```scp``` the file to your laptop or opening
it directly with root is a nice way to go and look at the canvases
with a TBrowser. 
