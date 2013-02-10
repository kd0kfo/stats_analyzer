if __name__ == "__main__":
    from sys import argv
    import visitors
    if len(argv) == 1:
        exit(0)
    visits = visitors.parse_file(argv[1])
    
    for i in visits:
        print("%s" % visits[i])
