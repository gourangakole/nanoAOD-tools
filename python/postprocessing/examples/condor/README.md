# NanoAOD to histogram directly

# Local run 
```
login to lxplus7
python tauFRExampleAnalysis_DoubleMu_v7_cleanTaus.py -h 
```

# for Condor submission

* create a text file with NanoAOD files using dasgclient

```
NanoAOD_DoubleMuon_2016C_whole.txt
```

* create jdl file
```
python createCondorJdl.py -f ../NanoAOD_DoubleMuon_2016C_whole.txt -o DoubleMuon_2016C -tauDecayMode=0 -isTauIn EB -tightJetdisc=16 -looseJetdisc=4 -muondisc=8 -eledisc=32
```

* submit to condor
```
./submitCondor.sh
```