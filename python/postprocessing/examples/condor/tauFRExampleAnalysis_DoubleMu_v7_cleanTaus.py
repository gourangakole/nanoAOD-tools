#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

import os,sys
from argparse import ArgumentParser

parser = ArgumentParser()

# https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
# Add more options if you like
parser.add_argument("-f", "--file", dest="inputfile",
                    help="input FILE", metavar="FILE")
parser.add_argument("-o", "--output", dest="outputfile", default="output.root",
                    help="outut FILE", metavar="FILE")
parser.add_argument("-copy", "--doCopyToEos", dest="doCopy", default=False,
                    help="make it to true if you want to really copy to eos")
parser.add_argument("-version", "--version", dest="version", default="v1",
                    help="change if needed")
parser.add_argument("-presel", "--sel", dest="presel", default="@Tau_pt.size() >= 1 && Tau_pt[0] > 20 && fabs(Tau_eta[0]) < 1.5 && Tau_decayMode == 0",
                    help="what is the preselection")
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
#print("copyToEos: ",args.doCopy)
#print("version: ", args.version)
print("Preselection: ",args.presel)
print("tauDecayMode: ",args.tauDecayMode)
print("isTauIn: ",args.isTauIn)
print("tightJetdisc: ", args.tightJetdisc)
print("looseJetdisc: ", args.looseJetdisc)
print("muondisc: ", args.muondisc)
print("eledisc: ", args.eledisc)
    
inputFname = args.inputfile
#fullpaths = open(inputFname).read().splitlines()
#print "Total number of files: ", len(fullpaths)


class ExampleAnalysis(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	Module.beginJob(self,histFile,histDirName)

        self.h_counter=ROOT.TH1F('counter',   'counter',   10, 0, 10)
	self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
        self.h_numpt=ROOT.TH1F('numpt',   'numpt',   20, 0, 200)
        self.h_denpt=ROOT.TH1F('denpt',   'denpt',   20, 0, 200)
        self.h_numpt_minDR=ROOT.TH1F('numpt_minDR',   'numpt_minDR',   20, 0, 200)
        self.h_denpt_minDR=ROOT.TH1F('denpt_minDR',   'denpt_minDR',   20, 0, 200)
        self.h_num_jetpt=ROOT.TH1F('num_jetpt',   'num_jetpt',   20, 0, 200)
        self.h_den_jetpt=ROOT.TH1F('den_jetpt',   'den_jetpt',   20, 0, 200)

        self.h_numeta=ROOT.TH1F('numeta',   'numeta',   50, -5.0, 5.0)
        self.h_deneta=ROOT.TH1F('deneta',   'deneta',   50, -5.0, 5.0)
        self.h_dimuonmass=ROOT.TH1F('dimuonmass',   'dimuonmass',   40, 50, 130)
        self.h_testpt=ROOT.TH1F('testpt',   'testpt',   20, 0, 200)
        self.h_test_jetpt=ROOT.TH1F('test_jetpt',   'test_jetpt',   20, 0, 200)
        self.h_testeta=ROOT.TH1F('testeta',   'testeta',   50, -5.0, 5.0)
        self.h_testdm=ROOT.TH1F('testdm',   'testdm',   20, 0, 20)
        self.h_deltaR_Mu_tau=ROOT.TH1F('deltaR_Mu_tau',   'deltaR_Mu_tau',   100, 0, 10)
        self.h_deltaR_Mu_Tighttau=ROOT.TH1F('deltaR_Mu_Tighttau',   'deltaR_Mu_Tighttau',   100, 0, 10)
        self.h_deltaR_Mu_Loosetau=ROOT.TH1F('deltaR_Mu_Loosetau',   'deltaR_Mu_Loosetau',   100, 0, 10)
        self.h_muonPt=ROOT.TH1F('muonPt',   'muonPt',   20, 0, 200)
        self.h_muonEta=ROOT.TH1F('muonEta',   'muonEta',   50, -5.0, 5.0)
        self.h_muonPt_mindeltaR=ROOT.TH1F('muonPt_mindeltaR',   'muonPt_mindeltaR',   20, 0, 200)
        self.h_muonEta_mindeltaR=ROOT.TH1F('muonEta_mindeltaR',   'muonEta_mindeltaR',   50, -5.0, 5.0)

        self.h_deltaR_E_tau=ROOT.TH1F('deltaR_E_tau',   'deltaR_E_tau',   100, 0, 10)
        self.h_deltaR_E_Tighttau=ROOT.TH1F('deltaR_E_Tighttau',   'deltaR_E_Tighttau',   100, 0, 10)
        self.h_deltaR_E_Loosetau=ROOT.TH1F('deltaR_E_Loosetau',   'deltaR_E_Loosetau',   100, 0, 10)
        self.h_electronPt=ROOT.TH1F('electronPt',   'electronPt',   20, 0, 200)
        self.h_electronEta=ROOT.TH1F('electronEta',   'electronEta',   50, -5.0, 5.0)
        self.h_electronPt_mindeltaR=ROOT.TH1F('electronPt_mindeltaR',   'electronPt_mindeltaR',   20, 0, 200)
        self.h_electronEta_mindeltaR=ROOT.TH1F('electronEta_mindeltaR',   'electronEta_mindeltaR',   50, -5.0, 5.0)

        self.addObject(self.h_counter)
        self.addObject(self.h_vpt )
        self.addObject(self.h_numpt)
        self.addObject(self.h_denpt)
        self.addObject(self.h_numpt_minDR)
        self.addObject(self.h_denpt_minDR)
        self.addObject(self.h_num_jetpt)
        self.addObject(self.h_den_jetpt)

        self.addObject(self.h_numeta)
        self.addObject(self.h_deneta)
        self.addObject(self.h_testpt)
        self.addObject(self.h_test_jetpt)
        self.addObject(self.h_testeta)
        self.addObject(self.h_testdm)
        self.addObject(self.h_dimuonmass)

        self.addObject(self.h_deltaR_Mu_tau)
        self.addObject(self.h_deltaR_Mu_Tighttau)
        self.addObject(self.h_deltaR_Mu_Loosetau)
        self.addObject(self.h_muonPt)
        self.addObject(self.h_muonEta)
        self.addObject(self.h_muonPt_mindeltaR)
        self.addObject(self.h_muonEta_mindeltaR)

        self.addObject(self.h_deltaR_E_tau)
        self.addObject(self.h_deltaR_E_Tighttau)
        self.addObject(self.h_deltaR_E_Loosetau)
        self.addObject(self.h_electronPt)
        self.addObject(self.h_electronEta)
        self.addObject(self.h_electronPt_mindeltaR)
        self.addObject(self.h_electronEta_mindeltaR)

    def analyze(self, event):
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        taus = Collection(event, "Tau")
        eventSum = ROOT.TLorentzVector()
        numtauP4 = ROOT.TLorentzVector()
        dentauP4 = ROOT.TLorentzVector()
        tauP4 = ROOT.TLorentzVector()
        diMuon = ROOT.TLorentzVector()

        # do tau cleaning from muons and electrons
        muon_selection = []
        electron_selection = []
        jet_selection = []
        for idx, muon in enumerate(muons):
            #if (muon satisfies criteria for selection): #fill criteria
            muon_selection.append((idx, muon))
        for idx, electron in enumerate(electrons):
            #if (electron satisfies criteria for selection):
            electron_selection.append((idx, electron))
        for idx, jet in enumerate(jets):
            #if (jet satisfies criteria for selection):
            jet_selection.append((idx, jet))

        lepton_selection = muon_selection + electron_selection # carefull now (Jet_jetIdx is not a branch)
        tausToClean = set([lep[1].jetIdx for lep in lepton_selection]) #lep[1] "1" stands to access 'ele' or 'muon' object
        tau_selection = []
        for idx, tau in enumerate(taus):
            if idx not in tausToClean:
                tau_selection.append((idx, tau))

        # now "tau_selection" is cleaned from lepton(electron+muons)
        icount = 0
        self.h_counter.Fill(icount)
 
        #select events with 2 muons 
        selMuons = []
        for lep in muons :     #loop on muons
            #print "muon loop"
            if lep.pt<20: continue
            #self.h_muonPt.Fill(lep.pt) #imporatnt GKOLE move at the muon loop later
            #self.h_muonEta.Fill(lep.eta)
            #if abs(lep.eta)>2.4: continue
            #if abs(lep.dz)>0.2: continue
            #if abs(lep.dxy)>0.045: continue
            #if not lep.mediumId: continue
            selMuons.append(lep)
        if len(selMuons) < 2: return False 
        icount += 1
        self.h_counter.Fill(icount)
        #print "len(selMuons): ", len(selMuons)

	#select events with 1 tau
        #itau = 0
        checkTight = False
        checkLoose = False
        tauDM = 100
        #tau  = max(tau_selection,key=lambda p: p[1].pt) #fix me
        newtaus = [tau[1] for tau in tau_selection]
        #print "newtaus before: ", newtaus
        if len(newtaus) < 1: return False
        icount += 1
        self.h_counter.Fill(icount)
        tau  = max(newtaus,key=lambda p: p.pt) # take the highest pt tau
        if tau.pt < 20: return False
        icount += 1
        self.h_counter.Fill(icount)

        if (args.isTauIn == "EB"):
            if abs(tau.eta) > 1.5 : return False
        else:
            if abs(tau.eta) < 1.5 : return False
    
        icount += 1
        self.h_counter.Fill(icount)

        if tau.decayMode != int(args.tauDecayMode): return False
        icount += 1
        self.h_counter.Fill(icount)

        checkTight = bool(tau.idDeepTau2017v2p1VSjet >= int(args.tightJetdisc)) and bool(tau.idDeepTau2017v2p1VSmu >= int(args.muondisc)) and bool(tau.idDeepTau2017v2p1VSe >= int(args.eledisc))
        checkLoose = bool(tau.idDeepTau2017v2p1VSjet >= int(args.looseJetdisc))  and bool(tau.idDeepTau2017v2p1VSmu >= int(args.muondisc)) and bool(tau.idDeepTau2017v2p1VSe >= int(args.eledisc))
        if checkTight: #16: Medium
            numtauP4 += tau.p4()
        if checkLoose: #4: VLoose
            dentauP4 += tau.p4()
        tauP4 += tau.p4()
        tauDM = tau.decayMode

        # per jet quantities, find the reco jet that matches best, aka tau seed (if any)
        best_match_idx = tau.jetIdx
        # print "best_match_idx: ", best_match_idx
        if best_match_idx >= 0:
            #for j in jets :
            #print "jets[best_match_idx].pt", jets[best_match_idx].pt
            #print "tau.pt: ", tau.pt
            self.h_test_jetpt.Fill(jets[best_match_idx].pt)
            if checkTight==True:
                self.h_num_jetpt.Fill(jets[best_match_idx].pt)
            if checkLoose==True:
                self.h_den_jetpt.Fill(jets[best_match_idx].pt)

        deltaR_min = 999.0
        closestMuon = []
        for mu in selMuons:
            self.h_muonPt.Fill(mu.pt) 
            self.h_muonEta.Fill(mu.eta)
            deltaR_mu_tau  = mu.DeltaR(tau)
            if (deltaR_mu_tau < deltaR_min):
                deltaR_min = deltaR_mu_tau
                closestMuon.append(mu)
            
        # DeltaR (looseTau and muon)        
        deltaR_min_looseTau = 999.0
        if checkLoose: 
            icount += 1
            self.h_counter.Fill(icount)
            deltaR_min_looseTau = deltaR_min
        # DeltaR (tighTau and muon)        
        deltaR_min_tightTau = 999.0
        if checkTight: 
            icount += 1
            self.h_counter.Fill(icount)
            deltaR_min_tightTau = deltaR_min
        #print "deltaR_min", deltaR_min
        #if len(selMuons) < 2: return False
        #if (selMuons[0].charge*selMuons[1].charge) > 0: return False
        #diMuon = selMuons[0].p4() + selMuons[1].p4()
        #if diMuon.M() < 70 or diMuon.M() > 110: return False
        #for mu in selMuons:
        #    print "mu.charge:  ", mu.charge
        #diMuon
        # add Z mass <70-110>
        #eventSum += lep.p4()
        closestElectron = []
        deltaR_min_e_tau = 999.0
        for lep in electrons : #loop on electrons
            eventSum += lep.p4()
            self.h_electronPt.Fill(lep.pt)
            self.h_electronEta.Fill(lep.eta)
            deltaR_e_tau  = lep.DeltaR(tau)
            if (deltaR_e_tau < deltaR_min_e_tau):
                deltaR_min_e_tau = deltaR_e_tau
                closestElectron.append(lep)
                    
        for j in jets :       #loop on jets
            eventSum += j.p4()
        self.h_vpt.Fill(eventSum.Pt()) #fill histogram
        if checkTight==True:
            self.h_numpt.Fill(numtauP4.Pt()) 
        if checkLoose==True:
            self.h_denpt.Fill(dentauP4.Pt()) 
        if checkTight==True and deltaR_min_tightTau > 0.4 and deltaR_min > 0.4:
            self.h_numpt_minDR.Fill(numtauP4.Pt()) 
        if checkLoose==True and deltaR_min_tightTau > 0.4 and deltaR_min > 0.4:
            self.h_denpt_minDR.Fill(dentauP4.Pt()) 
        if checkTight:
            self.h_numeta.Fill(numtauP4.Eta()) 
        if checkLoose:
            self.h_deneta.Fill(dentauP4.Eta()) 
        self.h_testpt.Fill(tauP4.Pt())
        self.h_testeta.Fill(tauP4.Eta())
        self.h_testdm.Fill(tauDM)
        #self.h_dimuonmass.Fill(diMuon.M())
        self.h_deltaR_Mu_tau.Fill(deltaR_min)
        self.h_deltaR_Mu_Tighttau.Fill(deltaR_min_tightTau)
        self.h_deltaR_Mu_Loosetau.Fill(deltaR_min_looseTau)
        #self.h_muonPt_mindeltaR.Fill(closestMuon[-1].pt)
        #self.h_muonEta_mindeltaR.Fill(closestMuon[-1].eta)
        #electron
        self.h_deltaR_E_tau.Fill(deltaR_min)
        if checkTight:
            self.h_deltaR_E_Tighttau.Fill(deltaR_min_e_tau)
        if checkLoose:
            self.h_deltaR_E_Loosetau.Fill(deltaR_min_e_tau)
        #self.h_electronPt_mindeltaR.Fill(closestElectron[-1].pt)
        #self.h_electronEta_mindeltaR.Fill(closestElectron[-1].eta)
        
        #print "event loop=============="
        return True


#preselection="@Muon_pt.size() >= 2 && @Tau_pt.size() >= 1 && Tau_pt[0] > 20 && fabs(Tau_eta[0]) < 1.5 && Tau_decayMode == 0"
#preselection="@Tau_pt.size() >= 1 && Tau_pt[0] > 20 && fabs(Tau_eta[0]) < 1.5 && Tau_decayMode == 0"
preselection=args.presel
#files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
#z = open(inputFname)
files=[inputFname]
#files = [line.strip().split() for line in z if not line.startswith('#')] #not working
#files = [line.strip() for line in z if not line.startswith('#')]
print "files", files
#files=[
#    "root://cms-xrd-global.cern.ch//store/data/Run2016C/DoubleMuon/NANOAOD/02Apr2020-v1/40000/1B5DA83E-CD1B-1D49-9C73-29F3CD221647.root",
#    "root://cms-xrd-global.cern.ch//store/data/Run2016C/DoubleMuon/NANOAOD/02Apr2020-v1/40000/A6B36E73-3D4C-324A-A62C-CD4425ABE886.root",
#]
#p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ExampleAnalysis()],noOut=True,histFileName="histOut_2016C_DoubleMuon_v4_11Sep.root",histDirName="plots")
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[ExampleAnalysis()],noOut=True,histFileName=args.outputfile,histDirName="plots")
p.run()
