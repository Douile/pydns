import struct
from .utils import bitunpack

def unpack_headers(data):
    id, h, qdcount, ancount, nscount, arcount = struct.unpack('>HHHHHH',data[:12])
    qr, opcode, aa, tc, rd, ra, z, rcode = bitunpack(h,'14111134')
    return (id, qr, opcode, aa, tc, rd, ra, z, rcode, qdcount, ancount, nscount, arcount)

def unpack_question(data):
    names = []
    name_i = 0
    while 1:
        name_len = data[name_i]
        name_i += 1
        if name_len == 0:
            break
        name = data[name_i:name_i+name_len]
        names.append(name)
        name_i += name_len
    qtype, qclass = struct.unpack('>HH',data[name_i:name_i+4])
    # qtype = data[name_i:2+name_i]
    # qclass = data[2+name_i:4+name_i]
    r = 4+name_i
    return (names,qtype,qclass),r

def unpack_record(data):
    names = []
    name_i = 0
    while 1:
        name_len = data[name_i]
        name_i += 1
        if name_len == 0:
            break
        name = data[name_i:name_i+name_len]
        names.append(name)
        name_i += name_len
    type, cclass, ttl, rdlength = struct.unpack('>HHIH',data[1+name_i:11+name_i])
    # type = data[1+name_len:3+name_len]
    # cclass = data[3+name_len:4+name_len]
    # ttl = data[4+name_len:9+name_len]
    # rdlength = data[9+name_len:11+name_len]
    rdata = data[11+name_i:11+name_i+rdlength]
    r = 11+name_i+rdlength
    return (names, type, cclass, ttl, rdata), r

def unpack(data):
    # compression handling needed
    headers = unpack_headers(data)
    rdata = data[12:]
    questions = []
    for i in range(0,headers[9]): # unpack questions
        question, r = unpack_question(rdata)
        rdata = rdata[r:]
        questions.append(question)
    answers = []
    for i in range(0,headers[10]): # unpack answers
        record, r = unpack_record(rdata)
        answers.append(record)
        rdata = rdata[r:]
    authority_records = []
    for i in range(0,headers[11]): # unpack authority records
        record, r = unpack_record(rdata)
        authority_records.append(record)
        rdata = rdata[r:]
    additional_records = []
    for i in range(0,headers[12]): # unpack additional
        record, r = unpack_record(rdata)
        additional_records.append(record)
        rdata = rdata[r:]
    if len(rdata) > 0:
        print('Unused data: ',rdata)
    return headers, questions, answers, authority_records, additional_records
