
class Visitor():
    def __init__(self,initial_dict):
        self.data = initial_dict

    def __str__(self):
        retval = ""
        for i in self.data:
            if self.data[i]:
                retval += "%s: %s\n" % (i.capitalize(),self.data[i])
        return retval

def add_visitor(map, visitor):
    if not "ip" in visitor.data:
        raise Exception("Broken IP block. Missing IP address. Keys %s" % visitor.data.keys())
    map[visitor.data["ip"]] = visitor
        
def parse_file(_file):
    file = None
    if isinstance(_file,str):
        file = open(_file,"r")
    else:
        file = _file
        
    retval = {}
    curr_visitor = None
    for line in file:
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
    file = None
    if isinstance(_file1,str):
        file = open(_file1,"r")
    else:
        file = _file1
        
    retval = {}
    for line in file:
        line = line.strip()
        if not line:
            continue
        tokens = line.split("\t")
        ip = tokens[0].strip()
        if not ip in canonical:
            continue
        retval[ip] = canonical[ip]
    
    return retval
            
def find_unknown(_file1, canonical):
    file = None
    if isinstance(_file1,str):
        file = open(_file1,"r")
    else:
        file = _file1
        
    retval = {}
    for line in file:
        line = line.strip()
        if not line:
            continue
        tokens = line.split("\t")
        ip = tokens[0].strip()
        if not ip in canonical:
            retval[ip] = line
    
    return retval
