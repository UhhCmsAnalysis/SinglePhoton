void myimage()
{
//=========Macro generated from canvas: c1/c1
//=========  (Thu Oct 14 18:24:03 2021) by ROOT version 6.14/09
   TCanvas *c1 = new TCanvas("c1", "c1",67,57,700,500);
   c1->Range(-17.6,-4.2,113.0667,23.8);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetLeftMargin(0.15);
   c1->SetBottomMargin(0.15);
   c1->SetFrameBorderMode(0);
   c1->SetFrameBorderMode(0);
   
   TH1F *hist2__1 = new TH1F("hist2__1","Another Histogram",100,2,100);
   hist2__1->SetBinContent(12,1);
   hist2__1->SetBinContent(19,6);
   hist2__1->SetBinContent(44,10);
   hist2__1->SetBinError(12,1);
   hist2__1->SetBinError(19,6);
   hist2__1->SetBinError(44,10);
   hist2__1->SetEntries(3);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.835,0.98,0.995,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   TText *ptstats_LaTex = ptstats->AddText("hist2");
   ptstats_LaTex->SetTextSize(0.0368);
   ptstats_LaTex = ptstats->AddText("Entries = 3      ");
   ptstats_LaTex = ptstats->AddText("Mean  =  34.29");
   ptstats_LaTex = ptstats->AddText("Std Dev   =  12.89");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   hist2__1->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(hist2__1);
   hist2__1->SetLineColor(4);
   hist2__1->Draw("");
   
   TPaveText *pt = new TPaveText(0.01,0.9395378,0.3136676,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(1);
   pt->SetFillColor(0);
   TText *pt_LaTex = pt->AddText("Another Histogram");
   pt->Draw();
   
   TH1F *hist1__2 = new TH1F("hist1__2","My First Histogram",100,5,50);
   hist1__2->SetBinContent(16,2);
   hist1__2->SetBinContent(65,3);
   hist1__2->SetBinContent(81,1);
   hist1__2->SetBinError(16,2);
   hist1__2->SetBinError(65,3);
   hist1__2->SetBinError(81,1);
   hist1__2->SetEntries(3);
   
   ptstats = new TPaveStats(0.78,0.835,0.98,0.995,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats_LaTex = ptstats->AddText("hist1");
   ptstats_LaTex->SetTextSize(0.03679999);
   ptstats_LaTex = ptstats->AddText("Entries = 3      ");
   ptstats_LaTex = ptstats->AddText("Mean  =  27.83");
   ptstats_LaTex = ptstats->AddText("Std Dev   =  11.47");
   ptstats->SetOptStat(1);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   hist1__2->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(hist1__2);
   hist1__2->SetLineColor(8);
   hist1__2->GetXaxis()->SetTitle("`f[#circ]");
   hist1__2->GetXaxis()->SetLabelSize(0.05);
   hist1__2->GetXaxis()->SetTitleSize(0.05);
   hist1__2->GetYaxis()->SetTitle("Entries / bin");
   hist1__2->GetYaxis()->SetLabelSize(0.05);
   hist1__2->GetYaxis()->SetTitleSize(0.05);
   hist1__2->Draw("same");
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
