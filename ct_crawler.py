#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 24 12:50:01 2018

@author: mitchellbailey
"""

import urllib2
import urllib
import argparse

parser = argparse.ArgumentParser(description="Retrieve py dictionary of clinical trials at clinicaltrials.gov for list of disorders")
parser.add_argument('conditions', type=str, help='semi-colon-separated list of conditions')

args = parser.parse_args()

conds = args.conditions.split(";")

res = {}

for item in conds:
    cond = urllib.urlencode({'cond': item})
    temp_url = "https://clinicaltrials.gov/ct2/results?%s"%cond
    f = urllib2.urlopen(temp_url)
    html= f.read()
    
    
    
    html_split = html.split("<table id=\"theDataTable\"")[1]
#    html_table = html_split.split("<tbody style=\"\">")[1]
    temp_rows = html_split.split("<tr")
    rows = []
    for item2 in temp_rows:
        test = item2.split("<td")
        if len(test) > 1:
            rows += [test]
        
    
    #0 :   class="odd" role="row">                           
    #1 :   class=" dt-body-right" tabindex="0"><a id="rowId1"></a>1</td>                             
    #2 :  ><div style="text-align:center"><input type="checkbox" class="SavedStudyCB" name="NCT02963350" onchange="updateCart(&#39;NCT02963350&#39;);"></div></td>                           
    #3 :  ><span style="color:red;">Approved for marketing</span></td>                               
    #4 :  ><a title="Show study NCT02963350: A Multicenter, Multi-national Open-label Program to Provide BMN 190 to Patients Diagnosed With CLN2 Disease" href="https://clinicaltrials.gov/ct2/show/NCT02963350?cond=cln2+disease&amp;rank=1">A Multicenter, Multi-national Open-label Program to Provide BMN 190 to Patients Diagnosed With <span class="hit_inf">CLN2 Disease</span></a></td>                              
    #5 :  ><ul><li><span class="hit_inf">CLN2 Disease</span></li></ul></td>                          
    #6 :  ><ul><li>Drug: BMN190, recombinant human tripeptidyl peptidase-1 (rhTPP1)</li></ul></td>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    #7 :  ><ul><li>Orange, California, United States</li><li>Columbus, Ohio, United States</li><li>Hamburg, Germany</li><li>(and 2 more...)</li></ul></td>  
    
    status = []
    title = []
    number = []
    url = []
    for item3 in rows:
        if len(item3[0].replace(" ","").replace("\n", "").replace("\t","")) != 0:
            status += [item3[3].split(">")[2].replace("</span","")]
            temp = item3[4].split("title=\"")[1]
            number += [temp.split(":")[0].replace("Show study","")]
            title += [temp.split(": ")[1].split("\"")[0]]
            url += ["https://clinicaltrials.gov" + temp.split("href=\"")[1].split("\">")[0]]
        else:
            pass
    i = 0
    res[item] = {}
    while i < len(number):
        res[item][i] = {'trial_number': number[i], 'status': status[i], 'title': title[i], 'url': url[i]}
        i += 1
        
for key, item in res.items():
    print key, item