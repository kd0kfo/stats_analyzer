if __name__ == "__main__":
    from sys import argv
    import visitors
    from getopt import getopt

    def print_all(visitor_dict):
        for i in visitor_dict:
            print("%s" % visitor_dict[i])

    find_intersect = False
    canonical_list = None
    do_lookup = False
    short_opts = "c:il"
    long_opts = ["canonical=","intersect","lookup"]
            
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
        else:
            print("Unknown Option: %s" % opt)
            exit(1)

    if find_intersect:
        if len(args) < 2:
            print("Intersect requires two files. Received: %d" % len(args))
            exit(1)
        print_all(visitors.intersect(args[0],args[1]))
        exit(0)
    if do_lookup:
        visits = visitors.lookup(args[0],canonical_list)
        print("Have %d records" % len(visits))
        print_all(visits)
        exit(0)
        
    print_all(visitors.parse_file(args[0]))
