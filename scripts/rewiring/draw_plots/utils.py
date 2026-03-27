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
    "cheeger_constant" : "Cheeger Constant"
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
    "border_breadth" : "Border Breadth"
}