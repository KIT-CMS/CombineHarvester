import ROOT as r

categories = {
    r"\texttt{ggH}" : "htt_{CH}_1_Run{YEAR}_prefit",
    r"\texttt{qqH}" : "htt_{CH}_2_Run{YEAR}_prefit",
    r"\texttt{wj}" : "htt_{CH}_11_Run{YEAR}_prefit",
    r"\texttt{ztt}" : "htt_{CH}_12_Run{YEAR}_prefit",
    r"\texttt{tt}" : "htt_{CH}_13_Run{YEAR}_prefit",
    r"\texttt{qcd}" : "htt_{CH}_{QCDBIN}_Run{YEAR}_prefit",
    r"\texttt{zll}" : "htt_{CH}_15_Run{YEAR}_prefit",
    r"\texttt{misc}" : "htt_{CH}_16_Run{YEAR}_prefit",
    r"\texttt{st}" : "htt_{CH}_18_Run{YEAR}_prefit",
    r"\texttt{db}" : "htt_{CH}_19_Run{YEAR}_prefit",
}

processes_lists  = {
    "mt": ["data_obs", "ggH", "qqH", "ttH125", "VH125", "EMB", "ZL", "VVL", "TTL", "jetFakes"],
    "et": ["data_obs", "ggH", "qqH", "ttH125", "VH125", "EMB", "ZL", "VVL", "TTL", "jetFakes"],
    "tt": ["data_obs", "ggH", "qqH", "ttH125", "VH125", "EMB", "ZL", "VVL", "TTL", "jetFakes"],
    "em": ["data_obs", "ggH", "qqH", "ttH125", "VH125", "EMB", "ZL", "VV", "ST", "TT", "W", "QCD", "HWW"],
}

category_lists = {
    "mt" : ["ggH", "qqH", "ztt", "zll", "misc", "tt", "qcd", "wj"],
    "et" : ["ggH", "qqH", "ztt", "zll", "misc", "tt", "qcd", "wj"],
    "tt" : ["ggH", "qqH", "ztt", "misc", "qcd"],
    "em" : ["ggH", "qqH", "ztt", "db", "st", "tt", "misc", "qcd"],
}

channel = "tt"
year = "2017"
f = r.TFile("cmb_datacard_shapes_prefit.root","read")
for year in ["2016","2017"]:
    print year
    for channel in ["mt", "et", "tt","em"]:
        print "\t",channel
        table = ""
        for cname in category_lists[channel]:
            c = (r"\texttt{%s}"%cname, categories[r"\texttt{%s}"%cname])
            cat_name = c[1].replace("{CH}",channel).replace("{YEAR}",year)
            if "{QCDBIN}" in cat_name:
                cat_name = cat_name.replace("{QCDBIN}","17") if channel == "tt" else  cat_name.replace("{QCDBIN}","14")
            cat_line_list = [c[0]]
            folder = f.Get(cat_name)
            if folder:
                complete_integral = sum([folder.Get(p).GetBinContent(1) for p in processes_lists[channel] if p != "VH125" and p != "HWW" and p != "data_obs" and folder.Get(p)])
                complete_integral += folder.Get("ZH125").GetBinContent(1) + folder.Get("WH125").GetBinContent(1)
                if channel == "em":
                    complete_integral += folder.Get("ggHWW125").GetBinContent(1) + folder.Get("qqHWW125").GetBinContent(1)
                for p in processes_lists[channel]:
                    if p not in ["VH125", "HWW"]:
                        h = folder.Get(p)
                        if h:
                            number = h.GetBinContent(1) if p == "data_obs" else h.GetBinContent(1)*100.0/complete_integral
                        else:
                            number = 0.0
                    elif p == "VH125":
                        h1 = folder.Get("ZH125")
                        h2 = folder.Get("WH125")
                        number = (h1.GetBinContent(1)+ h2.GetBinContent(1))*100.0/complete_integral
                    elif p == "HWW":
                        h1 = folder.Get("ggHWW125")
                        h2 = folder.Get("qqHWW125")
                        number = (h1.GetBinContent(1)+ h2.GetBinContent(1))*100.0/complete_integral
                    p_cat_filled_string = "%d"%number if p == "data_obs" else "%.2f"%number
                    if channel in ["mt","et","tt"] and p in ["jetFakes", "VVL", "TTL"]:
                        p_cat_filled_string = r"\multicolumn{2}{c}{" + p_cat_filled_string + "}"
                    cat_line_list.append(p_cat_filled_string)
                    if p == "ttH125":
                        if folder.Get(p):
                            print "\t\t",cname,folder.Get(p).GetBinContent(1)
                        else:
                             print "\t\t",cname,0.0
            cat_line = "    & " + " & ".join(cat_line_list) + r" \\" + "\n"
            table += cat_line

print table
