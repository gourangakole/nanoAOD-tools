
#//////////////////////////////////////////////////
#                                                 #
# Copy Ntuple root files from T2_IN_TIFR to T3.   #
# Merge them into a single root file at T3.       #
# Send the merged file back to T2_IN_TIFR.        #
# Store the full path of merged file for Analysis #
#                                                 #
#//////////////////////////////////////////////////

import os
import sys
import datetime

#USERS INPUTS
isData = True
isMC = False

mc = [
    "TTJets",
    "HplusM120",
    "ST_tW",
    "ST_t_",
    "ST_s",
    "WJetsToLNu",
    "W1JetsToLNu",
    "W2JetsToLNu",
    "W3JetsToLNu",
    "W4JetsToLNu",
    "DYJetsToLL",
    "DY1JetsToLL",
    "DY2JetsToLL",
    "DY3JetsToLL",
    "DY4JetsToLL",
    "WW",
    "WZ",
    "ZZ",
    "QCD_Pt-15to20_Mu",
    "QCD_Pt-20to30_Mu",
    "QCD_Pt-30to50_Mu",
    "QCD_Pt-50to80_Mu",
    "QCD_Pt-80to120_Mu",
    "QCD_Pt-120to170_Mu",
    "QCD_Pt-170to300_Mu",
    "QCD_Pt-300to470_Mu",
    "HplusM80",
    "HplusM90",
    "HplusM100",
    "HplusM140",
    "HplusM150",
    "HplusM155",
    "HplusM160"]

data = [
    "DoubleMuon_2016C_0_EB_16_4_8_32",
    "DoubleMuon_2016C_0_EE_16_4_8_32",
    "DoubleMuon_2016C_1_EB_16_4_8_32",
    "DoubleMuon_2016C_0_EB_16_4_8_0",
    "DoubleMuon_2016C_0_EB_16_4_0_32",
#    "DoubleMuon_2016E_16_4_8_32",
#    "DoubleMuon_2016E_16_4_8_0",
#    "DoubleMuon_2016E_16_4_0_32",
#    "DoubleMuon_2016G_16_4_8_32",
#    "DoubleMuon_2016G_16_4_8_0",
#    "DoubleMuon_2016G_16_4_0_32",
    "DoubleMuon_2016H_0_EB_16_4_8_32",
    "DoubleMuon_2016H_0_EE_16_4_8_32",
    "DoubleMuon_2016H_1_EB_16_4_8_32",
    "DoubleMuon_2016H_0_EB_16_4_8_0",
    "DoubleMuon_2016H_0_EB_16_4_0_32",
#    "DoubleMuon_2016H_16_4_8_0",
#    "DoubleMuon_2016H_16_4_0_32"
        ]

#-------------------------------
def execme(command):
    print ""
    print "\033[01;32m"+ "Excecuting: "+ "\033[00m",  command
    print ""
    os.system(command)

#DoubleMuon_2016G_16_4_8_0*.root
if isData:
    for samp in range(len(data)):
        execme("hadd -k "+str(data[samp])+"_Merged.root "+str(data[samp])+"_*")
        

if isMC:
    for samp in range(len(mc)):
        execme("hadd -k "+str(mc[samp])+"_Merged.root "+str(mc[samp])+"*")

#execme("hadd -k all_muData.root MuRun*_Merged.root")
#execme("hadd -k all_ST.root ST*_Merged.root")
#execme("hadd -k all_TTJets.root TTJets_Merged.root")
#execme("hadd -k all_Hplus.root Hplus*_Merged.root")
#execme("hadd -k all_QCD.root QCD*_Merged.root")
#execme("hadd -k all_VV.root WW_Merged.root WZ_Merged.root ZZ_Merged.root")
#execme("hadd -k all_WJets.root W1*_Merged.root W2*_Merged.root W3*_Merged.root W4*_Merged.root WJ*_Merged.root")
#execme("hadd -k all_DY.root DY1*_Merged.root DY2*_Merged.root DY3*_Merged.root DY4*_Merged.root DYJ*_Merged.root")

execme("mkdir merged_histos")
execme("cp *_Merged.root merged_histos")
#execme("cp all* merged_histos")
execme("tar -czvf merged_histos.tar.gz merged_histos")


