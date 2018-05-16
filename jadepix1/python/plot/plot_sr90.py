#!/usr/bin/env python

'''
plot Sr90 clusters compare hist
'''

__author__ = "YANG TAO <yangtao@ihep.ac.cn>"
__copyright__ = "Copyright (c) yangtao"
__created__ = "[2018-04-10 Apr 12:00]"


import sys,os
import ROOT
ROOT.gStyle.SetOptFit(111111)
ROOT.gStyle.SetStatX(0.9)
ROOT.gStyle.SetStatY(0.9)
ROOT.gStyle.SetStatW(0.18)
ROOT.gStyle.SetStatH(0.22)
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# console.setFormatter(logging.Formatter(' %(asctime)s - %(levelname)s- %(message)s'))
# logging.getLogger('').addHandler(console)

def landau_fit(hist,min,max):

    landau_fit = ROOT.TF1('landau_fit','landau',min,max)
    hist.Fit(landau_fit,'R0+')

    p = []
    for ip in xrange(3):
        p.append(landau_fit.GetParameter(ip))

    draw_landau = ROOT.TF1('draw_landau','landau',500,60000)
    draw_landau.SetParameters(p[0],p[1],p[2])
    #hist.Fit(draw_landau,'R+')

    return draw_landau

def main(cluster55_fname,min,max,title):
    try:

        cluster55_file = ROOT.TFile(cluster55_fname)
        cluster55_cluster_tree = cluster55_file.Get('Cluster_Tree')
        cluster55_cluster_entries = cluster55_cluster_tree.GetEntries()

    except:
        logging.error('input file is invalid!')
        sys.exit()

    cluster_canvas = ROOT.TCanvas('cluster_canvas','cluster_siganl',200,10,1600,1200)
    #cluster_legend = ROOT.TLegend(0.75,0.7,0.85,0.85)


    cluster55_cluster_hist = ROOT.TH1F('CHIP %s {}^{90}sr cluster signal'%title,'CHIP %s {}^{90}Sr  Cluster Signal'%title,256,0,65536)
    cluster55_cluster_hist.GetXaxis().SetTitle('ADC')
    cluster55_cluster_hist.GetXaxis().CenterTitle()
    cluster55_cluster_hist.GetYaxis().SetTitle('Normalized Counts')
    cluster55_cluster_hist.GetYaxis().CenterTitle()
    cluster55_cluster_hist.SetLineColor(4)
    cluster55_cluster_hist.SetLineWidth(2)

    for cluster55_cluster_entry in xrange(cluster55_cluster_entries):
        cluster55_cluster_tree.GetEntry(cluster55_cluster_entry)
        tmp = cluster55_cluster_tree.TotalClusterSignal
        cluster55_cluster_hist.Fill(tmp) 
    mpv = cluster55_cluster_hist.GetMaximumBin()*256
    cluster55_cluster_hist.Scale(1/cluster55_cluster_hist.Integral())

    print('*******MPV :',mpv,'********')

    #fit = landau_fit(cluster55_cluster_hist,min,max)

    if not os.path.exists('../fig/'):
        os.makedirs('../fig/')


    cluster_canvas.cd()
    cluster55_cluster_hist.Draw('hist')
    #fit.Draw('same')
    cluster_canvas.Update()
    cluster_canvas.SaveAs('../fig/Sr90_cluster_chip_%s.gif'%title)


if __name__ == '__main__':
    
    main('../output/CHIPA1_Cluster55_Sr90_thr500.root',2000,10000,'A1')
    main('../output/CHIPA2_Cluster55_Sr90_thr500.root',2000,10000,'A2')
    main('../output/CHIPA3_Cluster55_Sr90_thr500.root',1000,10000,'A3')

    main('../output/CHIPA4_Cluster55_Sr90_thr500.root',2000,10000,'A4')
    main('../output/CHIPA5_Cluster55_Sr90_thr500.root',1000,10000,'A5')
    main('../output/CHIPA6_Cluster55_Sr90_thr500.root',1000,10000,'A6')




