import pickle
import ipdb
from pygraphviz import *
import random

# graph data:
f = open(r'graph-from-incident.pickle', 'rb')
gdata = pickle.load(f)
f.close()

# print dictionary object loaded from file
# print(gdata)
# datastructure:
#   {
#     (type, sys_id) -> [(type, sys_id), (type_sys_id)]
#     (type, sys_id) -> [(type, sys_id), (type_sys_id), (type, sys_id)]
#   }
#
# so,let's color the specific type of vertices.

# some taken from http://www.graphviz.org/doc/info/colors.html
colors_o_bunch = ["aliceblue", "antiquewhite4", "aquamarine4", "azure4", "bisque3", "blue1", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk4", "cyan3", "darkgoldenrod3", "darkolivegreen1", "darkorange1", "darkorchid1", "darkseagreen", "darkslateblue", "darkslategray4", "deeppink1", "deepskyblue1", "dimgrey", "dodgerblue4", "firebrick4", "gold", "goldenrod", "gray", "gray11", "gray16", "gray20", "gray25", "gray3", "gray34", "gray39", "gray43", "gray48", "gray52", "gray57", "gray61", "gray66", "gray70", "gray75", "gray8", "gray84", "gray89", "gray93", "gray98", "green3", "grey1", "grey13", "grey18", "grey22", "grey27", "grey31", "grey36", "grey40", "grey45", "grey5", "grey54", "grey59", "grey63", "grey68", "grey72", "grey77", "grey81", "grey86", "grey90", "grey95", "honeydew", "hotpink", "indianred", "indigo", "ivory3", "khaki3", "lavenderblush2", "lemonchiffon1", "lightblue1", "lightcyan", "lightgoldenrod", "lightgoldenrodyellow", "lightpink2", "lightsalmon2", "lightskyblue1", "lightslategray", "lightsteelblue3", "lightyellow3", "magenta1", "maroon1", "mediumblue", "mediumorchid4", "mediumpurple4", "mediumvioletred", "mistyrose2", "navajowhite1", "navyblue", "olivedrab2", "orange2", "orangered2", "orchid2", "palegreen1", "paleturquoise1", "palevioletred1", "peachpuff", "peru", "pink4", "plum4", "purple3", "red3", "rosybrown3", "royalblue3", "salmon2", "seagreen1", "seashell1", "sienna1", "skyblue1", "slateblue1", "slategray1", "snow", "springgreen", "steelblue", "tan", "thistle", "tomato", "transparent", "turquoise4", "violetred3", "wheat3", "yellow1", "aliceblue", "beige", "blueviolet", "chocolate", "cyan", "darkgreen", "darkorange", "darkslateblue", "deeppink", "firebrick", "ghostwhite", "green", "indigo", "lawngreen", "lightgoldenrodylighw", "lightsalmon", "lightsteelblue", "magenta", "mediumpmediu", "mediumvioletred", "navajowhite", "orange", "orangurorange", "pink", "rosybrown", "seagrseagrlateblue", "steelblue", "turquoise", "yellow"]

node_types = set([n[0] for n in gdata.keys()])
colors = random.sample(colors_o_bunch, len(node_types))
# {'sys_user_group', 'cmdb_ci_service', 'u_ops_programs', 'incident', 'cmn_cost_center', 'ldap_server_config', 'sys_user', 'cmdb_ci'}
type_color = dict(zip(node_types, colors))

G=AGraph(directed=True, data=gdata)
# ipdb.set_trace()
for l in G.nodes():
    l.attr['style'] = 'filled'
    for t in type_color.keys():
        if t in str(l):
            l.attr['fillcolor'] = type_color[t]

G.draw('from_incident.png', format='png',prog='dot')

