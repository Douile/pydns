def read_text_file(file):
    f = open(file,'rb')
    b = f.read()
    f.close()
    return str(b,'utf-8')

def parse_hosts(file):
    definitions = {}

    text = read_text_file(file)
    rules = text.split('\n')
    for rule in rules:
        parts = rule.strip().split(' ')
        if len(parts) == 2:
            add_definition(definitions, parts[0], 'A', parts[1])
            # definitions[parts[0]] = ('A',parts[1])
        elif len(parts) > 2:
            add_definition(definitions, parts[0], parts[1], ' '.join(parts[2:]))
            # definitions[parts[0]] = (parts[1],' '.join(parts[2:]))
    return definitions

def add_definition(defs, host, rtype, rvalue):
    if host in defs:
        defs[host].append((rtype,rvalue))
    else:
        defs[host] = [(rtype,rvalue)]
