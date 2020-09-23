import itertools
import os, sys

#Last used
#python createCondorJdl.py -f ../NanoAOD_DoubleMuon_2016C_whole.txt -o DoubleMuon_2016C -tauDecayMode=0 -isTauIn EB -tightJetdisc=16 -looseJetdisc=4 -muondisc=8 -eledisc=32
########

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="inputfile",
                    help="input FILE", metavar="FILE")
parser.add_argument("-o", "--output", dest="outputfile", default="output.root",
                    help="outut FILE", metavar="FILE")
parser.add_argument("-tauDecayMode", "--tauDecayMode", dest="tauDecayMode", default=0,
                    help="tauDecayMode value in Int", metavar="N")
parser.add_argument("-isTauIn", "--isTauIn", dest="isTauIn", default="EB",
                    help="make where is your tau located EB or EE")
parser.add_argument("-tightJetdisc", "--tightJetdisc", dest="tightJetdisc", default=16,
                    help="tightJetdisc disc value in Int", metavar="N")
parser.add_argument("-looseJetdisc", "--looseJetdisc", dest="looseJetdisc", default=4,
                    help="looseJetdisc disc value in Int", metavar="N")
parser.add_argument("-muondisc", "--muondisc", dest="muondisc", default=8,
                    help="muondisc disc value in Int", metavar="N")
parser.add_argument("-eledisc", "--eledisc", dest="eledisc", default=8,
                    help="eledisc disc value in Int", metavar="N")
args = parser.parse_args()

print("InputFile:  ",args.inputfile)
print("OutputFile: ",args.outputfile)
print("tauDecayMode: ",args.tauDecayMode)
print("isTauIn: ",args.isTauIn)
print("tightJetdisc: ", args.tightJetdisc)
print("looseJetdisc: ", args.looseJetdisc)
print("muondisc: ", args.muondisc)
print("eledisc: ", args.eledisc)

# output Jdl file define
jdlOutput = "submit"+args.outputfile+"_"+str(args.tauDecayMode)+"_"+args.isTauIn+"_"+str(args.tightJetdisc)+"_"+str(args.looseJetdisc)+"_"+str(args.muondisc)+"_"+str(args.eledisc)+".jdl"
print("Output Jdl file: ", jdlOutput)

#Read a file and make a list
inputFname = args.inputfile
z = open(inputFname)
inputFiles = [line.strip() for line in z if not line.startswith('#')]
#print "inputFiles: ", inputFiles
outputFiles = [args.outputfile+"_"+str(args.tauDecayMode)+"_"+args.isTauIn+"_"+str(args.tightJetdisc)+"_"+str(args.looseJetdisc)+"_"+str(args.muondisc)+"_"+str(args.eledisc)+"_"+str(i)+".root" for i in range(len(inputFiles))]
#print "outputFiles", outputFiles

Year       =["2016", "2017", "2018"]
SampleList    =["TTGamma", "TTbar", "TGJets", "WJets", "ZJets", "WGamma", "ZGamma", "Diboson", "SingleTop", "TTV","GJets"]
SampleListEle = SampleList + ["QCDEle", "DataEle"]
SampleListMu  = SampleList + ["QCDMu", "DataMu"]
Systematics   =["PU","MuEff","PhoEff","BTagSF_b","BTagSF_l","EleEff","Q2","Pdf","isr","fsr"]
SystLevel     = ["up", "down"]
ControlRegion = ["tight"]
#ControlRegion=["tight", "looseCRge2e0", "looseCRge2ge0", "looseCRe3ge2", "looseCRge4e0", "looseCRe3e0", "looseCRe2e1", "looseCRe2e0", "looseCRe2e2", "looseCRe3e1" ]

common_command = \
'Universe   = vanilla\n\
should_transfer_files = YES\n\
when_to_transfer_output = ON_EXIT\n\
use_x509userproxy = true\n\
Output = log/log$(cluster)_$(process).stdout\n\
Error  = log/log$(cluster)_$(process).stderr\n\
Log    = log/log$(cluster)_$(process).condor\n\n'

#----------------------------------------
#Create jdl file for base
#----------------------------------------
if not os.path.exists("jdl"):
    os.makedirs("jdl")
fileBase = open('jdl/'+jdlOutput,'w')
fileBase.write('Executable =  remoteRunBase.sh \n')
fileBase.write(common_command)
#for year, sample, cr in itertools.product(Year, SampleListEle, ControlRegion):
#    run_commandEle =  \
#                      'arguments  = %s Ele %s %s \n\
#queue 1\n\n' %(year, sample, cr)
#    fileBase.write(run_commandEle)
for (ifile, iout) in zip(inputFiles, outputFiles):
    run_commandMu =  \
                     'arguments  = %s %s %d %s %d %d %d %d \n\
queue 1\n\n' %(ifile, iout, int(args.tauDecayMode), args.isTauIn, int(args.tightJetdisc), int(args.looseJetdisc), int(args.muondisc), int(args.eledisc))
    fileBase.write(run_commandMu)
fileBase.close()
