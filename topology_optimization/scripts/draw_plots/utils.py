import matplotlib as mpl
from cycler import cycler

def apply_styling():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial"],
        "mathtext.fontset": "cm",
        "mathtext.rm": "sans",
        "mathtext.default": "regular",
        "font.size": 14,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,

        "axes.prop_cycle": cycler(color=[
        "#3F77D2",
        "#D23C37",
        "#4EB130", 
        "#FFB330",
        "#774CB5",
    ]),
})

METRIC_NAMES = {
    "avg_degree" : r"Average Degree, $\langle k \rangle$",
    "algebraic_connectivity" : "Algebraic Connectivity",
    "|V|" : "Number of Nodes",
    "|E|" : "Number of Edges",
    "assortativity": "Assortativity Coefficient",
    "transitivity": "Transitivity $C\delta$",
    "degree_std" : "Degree Standard Deviation",
    "degree_entropy" : "Degree Entropy",
    "spectral gap": "Spectral Gap",
    "cheeger_constant" : "Cheeger Constant",
    "total_paths_avg" : "Average Total Paths",
    "inter_isd_paths_avg" : "Average Inter ISD Paths",
    "intra_isd_paths_avg" : "Average Intra ISD Paths",
    "border_breadth_avg" : "Average Border Breadth"
}

METRIC_LABELS = {
    "avg_degree" : r"Average Degree, $\langle k \rangle$",
    "algebraic_connectivity" : "$a(G)$",
    "|V|" : "$|N|$",
    "|E|" : "$|E|$",
    "assortativity": "Assortativity Coefficient",
    "transitivity": "Transitivity $C\delta$",
    "degree_std" : "Degree Standard Deviation",
    "degree_entropy" : "Degree Entropy",
    "spectral gap": "Spectral Gap",
    "cheeger_constant" : "Cheeger Constant",
    "border_breadth" : "Border Breadth",
    "total_paths_avg" : "Nr Paths (avg)",
    "inter_isd_paths_avg" : "Nr Paths (avg)",
    "intra_isd_paths_avg" : "Nr Paths (avg)",
    "border_breadth_avg" : "Border Breadth (avg)"
}

TOPO_NAMES = {
    "topo0" : "Initial Testbed Topology",
    "topo1" : "SCIERA Topology",
    "topo2" : "Synthetic Topology 1",
    "topo3" : "Synthetic Topology 2",
    "topo4" : "Synthetic Topology 3",
    "topo5" : "Synthetic Topology 4",
    "topo6" : "Synthetic Topology 5",
    "topo7" : "Synthetic Topology 6",
    "topo8" : "Synthetic Topology 7",
    "topo9" : "Synthetic Topology 8",
    "topo10" : "Synthetic Topology 9",
    "topo11" : "Synthetic Topology 10",
}