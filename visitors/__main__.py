if __name__ == "__main__":
    from sys import argv
    import visitors
    from getopt import getopt

    def print_all(visitor_dict):
        for i in visitor_dict:
            print("%s" % visitor_dict[i])

    find_intersect = False
    relative_complement = False
    canonical_list = None
    do_lookup = False
    find_unknown = False
    short_opts = "c:ilru"
    long_opts = ["canonical=","intersect","relcomp","lookup","unknown"]
            
    (opts,args) = getopt(argv[1:],short_opts,long_opts)
    if not args:
        print("No file name given.")
        exit(0)

    for (opt,optarg) in opts:
        while opt[0] == "-":
            opt = opt[1:]
        if opt in ["c","canonical"]:
            canonical_list = visitors.parse_file(optarg)
        elif opt in ["i","intersect"]:
            find_intersect = True
        elif opt in ["l","lookup"]:
            do_lookup = True
        elif opt in ["r","relcomp"]:
            relative_complement = True
        elif opt in ["u","unknown"]:
            find_unknown = True
        else:
            print("Unknown Option: %s" % opt)
            exit(1)

    if find_intersect:
        if len(args) < 2:
            print("Intersect requires two files. Received: %d" % len(args))
            exit(1)
        print_all(visitors.intersect(args[0],args[1]))
        exit(0)
    if relative_complement:
        if len(args) < 2:
            print("Relative complement requires two files. Received: %d" % len(args))
            exit(1)
        print_all(visitors.rel_complement(args[0],args[1]))
        exit(0)
    if find_unknown:
        unknowns = visitors.find_unknown(args[0],canonical_list)
        print("Have %d unknown IPs" % len(unknowns))
        print_all(unknowns)
        exit(0)
    if do_lookup:
        visits = visitors.lookup(args[0],canonical_list)
        print("Have %d records" % len(visits))
        print_all(visits)
        exit(0)
        
    print_all(visitors.parse_file(args[0]))
