
class Visitor():
    def __init__(self,initial_dict):
        self.data = initial_dict

    def __str__(self):
        retval = ""
        for i in self.data:
            if self.data[i]:
                retval += "%s: %s\n" % (i.capitalize(),self.data[i])
        return retval

def add_visitor(vistor_map, visitor):
    if not "ip" in visitor.data:
        raise Exception("Broken IP block. Missing IP address. Keys %s" % visitor.data.keys())
    vistor_map[visitor.data["ip"]] = visitor
        
def parse_file(_file):
    infile = None
    if isinstance(_file,str):
        infile = open(_file,"r")
    else:
        infile = _file
        
    retval = {}
    curr_visitor = None
    for line in infile:
        line = line.strip()
        if not line:
            if curr_visitor:
                add_visitor(retval,curr_visitor)
                curr_visitor = Visitor({})
            continue
        if not ":" in line:
            raise Exception("Broken IP block. Missing ':' on line: %s" % line)
        tokens = line.split(":")
        key = tokens[0].strip().lower()
        val = ":".join(tokens[1:])
        val = val.strip()
        if not curr_visitor:
            curr_visitor = Visitor({})
        curr_visitor.data[key] = val
        
    if curr_visitor and curr_visitor.data:
        add_visitor(retval,curr_visitor)
    curr_visitor = None

    return retval

UNKNOWN = "UNK"
def json2visitor(json):
    data = {}
    data['ip'] = json['ip']
    data['country'] = json['country_code']
    data['city'] = json['city']
    data['orgid'] = UNKNOWN
    data['stateprov'] = json['region_code']
    data['postalcode'] = json['zipcode']
    data['country'] = json['country_code']
    data['latitude'] = json['latitude']
    data['longitude'] = json['longitude']
    return Visitor(data)

def parse_jsonfile(_file):
    import json
    visitor_map = {}
    infile = None
    if isinstance(_file,str):
        infile = open(_file,"r")
    else:
        infile = _file

    json_array = json.loads(infile.read())
    for data in json_array:
        add_visitor(visitor_map,json2visitor(data))
    return visitor_map
        
def intersect(file1, file2):
    set1 = parse_file(file1)
    set2 = parse_file(file2)
    
    retval = {}
    for i in set1:
        if i in set2:
            retval[i] = set1[i]
    
    return retval

def rel_complement(file1,file2):
    set1 = parse_file(file1)
    set2 = parse_file(file2)
    
    retval = {}
    for i in set1:
        if not i in set2:
            retval[i] = set1[i]
    
    return retval

def lookup(_file1, canonical):
    infile = None
    if isinstance(_file1,str):
        infile = open(_file1,"r")
    else:
        infile = _file1
        
    retval = {}
    for line in infile:
        line = line.strip()
        if not line:
            continue
        tokens = line.split("\t")
        ip = tokens[0].strip()
        if not ip in canonical:
            continue
        last_date = None
        latest_hits = None
        if len(tokens) >= 5:
            last_date = tokens[4]
        if len(tokens) >= 3:
            latest_hits = tokens[2]
        retval[ip] = canonical[ip]
        if last_date:
            retval[ip].data["Last Date"] = last_date
        if last_date:
            retval[ip].data["Latest Hits"] = latest_hits


    
    return retval
            
def find_unknown(_file1, canonical):
    infile = None
    if isinstance(_file1,str):
        infile = open(_file1,"r")
    else:
        infile = _file1
        
    retval = {}
    for line in infile:
        line = line.strip()
        if not line:
            continue
        tokens = line.split("\t")
        ip = tokens[0].strip()
        if not ip in canonical:
            retval[ip] = line
    
    return retval
