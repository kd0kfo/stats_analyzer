#!/usr/bin/env python
#
# IP Lookup script.
# Expects a tab delimited list of: IP, PAGES, HITS, BANDWIDTH, LAST VISIT
# The first column (IP) is required. Others are optional.
#
# This script uses a local settings module that the user must provide that
# contains an address to be used to look up IPs. This script is meant for 
# simplifying the look up process and should NOT provide unnecessary and 
# onerous traffic to any website that is nice enough to provide stats. DO NOT
# USE THIS IN THAT MANNER! It is expected that the user use this script
# MANUALLY rather than in an automated way. License to use this script is
# denied to anyone violating terms of another website that may provide
# IP statistics. Otherwise this script is free to be used under the terms
# of the GNU General Public License  version 3 which may be found at 
# http://www.gnu.org/licenses/gpl.html
#

import local_settings
import httplib
from sys import stdout,argv

conn = httplib.HTTPConnection(local_settings.URL)
in_filename = argv[1]
def parse_awk(in_filename):
    retval = []
    for line in open(in_filename,"r"):
        clean_line = line.strip()
        if not clean_line:
            continue
        tokens = clean_line.split("\t")
        if not tokens:
            continue

        ip = tokens[0]
        date = None
        if len(tokens) >= 5:
            date = tokens[4]
        hits = 0
        if len(tokens) >= 2:
            hits = tokens[1]
        retval.append({"ip": ip, "date": date, "hits": hits})
    return retval

def parse_json(in_filename):
    import json
    retval = []
    for line in open(in_filename, "r"):
        line = line.strip()
        retval.append(json.loads(line))
    return retval

if "json" in in_filename:
    hits = parse_json(in_filename)
else:
    hits = parse_awk(in_filename)

for hit in hits:
    ip = hit['ip']
    date = None
    hits = 0
    if 'date' in hit:
        date = hit['date']
    if 'hits' in hit:
        hits = int(hits)
    if not 'region_name' in hit:
        continue
    if hit['region_name'] != 'Virginia':
        continue

    conn.request("GET",local_settings.URL_DIRECTORY + ip)
    resp = conn.getresponse()
    content = resp.read()

    import re
    print("IP: " + ip)
    for key in local_settings.SEARCH_KEYS:
        search_str = "%s</td><td>([^<]*)</td>"%key
        #print(search_str)
        m = re.search(search_str,content)
        if m:
            for g in m.groups():
                print("%s: %s" % (key,g))
    if date and date != "-":
        print("Date: " + date)
    if hits:
        print("Hits: " + hits)
    else:
        print("Hits: 1")
    print("")
    stdout.flush()
conn.close()
