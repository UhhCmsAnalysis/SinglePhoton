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
```

Now we should be ready to make plots
