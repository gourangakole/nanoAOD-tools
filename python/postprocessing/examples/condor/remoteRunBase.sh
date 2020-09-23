#!/bin/bash

inputFile=$1
coutputFile=$2
tauDecayMode=$3
isTauIn=$4
tightJetdisc=$5
looseJetdisc=$6
muondisc=$7
eledisc=$8
printf "Start Running Analyzer at ";/bin/date
printf "Worker node hostname ";/bin/hostname
echo "---------------------------------------------"

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    #cd /home/gkole/t3store3/NanoAOD/CMSSW_10_6_12/src/PhysicsTools/NanoAODTools/python/postprocessing/examples/condor/
    cd /home/gkole/t3store3/NanoAOD/CMSSW_10_4_0/src/PhysicsTools/NanoAODTools/python/postprocessing/examples/condor/
    eval `scramv1 runtime -sh`
fi

python tauFRExampleAnalysis_DoubleMu_v7_cleanTaus.py -f $inputFile -o $coutputFile -presel="@Muon_pt.size() >= 2" -tauDecayMode=$tauDecayMode -isTauIn $isTauIn -tightJetdisc=$tightJetdisc -looseJetdisc=$looseJetdisc -muondisc=$muondisc -eledisc=$eledisc
#python makeHistograms13TeV.py -y $year -c $channel -s $sample --$controlRegion --plot presel_Njet
printf "Done Analyzer at ";/bin/date
