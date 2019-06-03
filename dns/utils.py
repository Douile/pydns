def bitpack(struct_s,*args):
    output = 0
    t = -1
    for c in struct_s:
        t += int(c)
    pos = 0
    for b in range(0,len(struct_s)):
        length = int(struct_s[b])
        i = t-pos
        x = args[b] << i
        output = output ^ x
        pos += length
    return output

def bitunpack(byte,struct_s):
    a = 0
    output = []
    negator = 0
    pos = 0
    for c in struct_s:
        a += int(c)
    for b in range(0,len(struct_s)):
        length = int(struct_s[b])
        i = a-pos
        x = byte ^ negator
        y = x>>i
        output.append(y)
        negator = negator ^ (y<<i)
        pos += length
    return tuple(output)

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

def transform_bindings(bindings):
    transformed = {}
    for name in bindings:
        host_bindings = bindings[name]
        for i in range(0,len(host_bindings)):
            binding = host_bindings[i]
            if binding[0] == 'A':
                ip = ipv4_to_int(binding[1])
                if ip is not None:
                    host_bindings[i] = (binding[0],ip)
        transformed[name] = host_bindings
    return transformed
