OPCODE_DEFS = {
    0: 'QUERY',
    1: 'IQUERY',
    2: 'STATUS'
}
I_OPCODE_DEFS = {v: k for k, v in OPCODE_DEFS.items()}
TYPE_DEFS = {
    1: 'A',
    2: 'NS',
    3: 'MD',
    4: 'MF',
    5: 'CNAME',
    6: 'SOA',
    7: 'MB',
    8: 'MG',
    9: 'MR',
    10: 'NULL',
    11: 'WKS',
    12: 'PTR',
    13: 'HINFO',
    14: 'MINFO',
    15: 'MX',
    16: 'TXT',
    252: 'AXFR',
    253: 'MAILB',
    254: 'MAILA',
    255: '*'
}
I_TYPE_DEFS = {v: k for k, v in TYPE_DEFS.items()}
CLASS_DEFS = {
    1: 'IN',
    2: 'CS',
    3: 'CH',
    4: 'HS'
}
I_CLASS_DEFS = {v: k for k, v in CLASS_DEFS.items()}
