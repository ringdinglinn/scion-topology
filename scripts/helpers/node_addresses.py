def isd_as_to_address(isd_n, as_n):
    return f"{15 + int(isd_n)}-ffaa:{isd_n}:{as_n}"

def node_to_address(node):
    return isd_as_to_address(node['isd_n'], node['as_n'])

def node_to_name(node):
    return f"scion{node['isd_n']}-{node['as_n']}"

def name_to_isd_as(node_name):
    parts = node_name.split('-')
    isd_n = parts[0].replace('scion', '')
    as_n = parts[1]
    return isd_n, as_n

def name_to_address(node):
    return isd_as_to_address(*name_to_isd_as(node))

def isd_as_to_label(isd_n, as_n):
    return str(isd_n) + "-" + str(as_n)

def label_to_idx(G, label):
    return next(n for n in G.nodes if G.nodes[n].get("label") == label)

