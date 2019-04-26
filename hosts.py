def read_text_file(file):
    f = open(file,'rb')
    b = f.read()
    f.close()
    return str(b,'utf-8')

def ipv4_to_int(ip):
    r = None
    p = ip.split('.')
    if len(p) == 4:
        r = 0
        for i in range(0,4):
            try:
                x = int(p[i])
            except:
                return None
            r |= x << (8*(3-i))
    return r

def parse_hosts(file):
    definitions = {}

    text = read_text_file(file)
    rules = text.split('\n')
    for rule in rules:
        parts = rule.strip().split(' ')
        if len(parts) == 2:
            ip = ipv4_to_int(parts[1])
            if ip is not None:
                definitions[parts[0]] = ip
    return definitions
