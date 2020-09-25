#!/bin/bash
mkdir -p log
condor_submit  jdl/submitDoubleMuon_2016C_0_EB_16_4_8_32.jdl
condor_submit  jdl/submitDoubleMuon_2016C_0_EB_16_4_8_0.jdl
condor_submit  jdl/submitDoubleMuon_2016C_0_EB_16_4_0_32.jdl
#condor_submit  jdl/submitDoubleMuon_2016C_0_EE_16_4_8_32.jdl
#condor_submit  jdl/submitDoubleMuon_2016C_1_EB_16_4_8_32.jdl
condor_submit  jdl/submitDoubleMuon_2016H_0_EB_16_4_8_32.jdl
condor_submit  jdl/submitDoubleMuon_2016H_0_EB_16_4_8_0.jdl
condor_submit  jdl/submitDoubleMuon_2016H_0_EB_16_4_0_32.jdl
#condor_submit  jdl/submitDoubleMuon_2016H_0_EE_16_4_8_32.jdl 
#condor_submit  jdl/submitDoubleMuon_2016H_1_EB_16_4_8_32.jdl 
