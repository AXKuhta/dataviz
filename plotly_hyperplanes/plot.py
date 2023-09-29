from plotly.graph_objects import Figure, Scatter
from sklearn.tree import DecisionTreeClassifier
# from sklearn import tree as _tree
# import graphviz
import numpy as np
import os

#
# decisiontree
#

data = np.loadtxt("source.dat")

# Перекосить данные таким образом, чтобы сделать данные проще для решающего дерева
data[:, 0] += data[:, 1]*0.2

x = data[:, :-1]
y = data[:, -1:]

tree = DecisionTreeClassifier()
tree.fit(x, y)
print(tree.score(x, y))

#
# dataviz
#

type_a = data[data[:, 2] == 0]
type_b = data[data[:, 2] == 1]

plot_a = Scatter(x=type_a[:, 0], y=type_a[:, 1], mode="markers")
plot_b = Scatter(x=type_b[:, 0], y=type_b[:, 1], mode="markers")
fig = Figure([plot_a, plot_b])

for feature, threshold in zip(tree.tree_.feature, tree.tree_.threshold):
	if feature == 0: # x axis
		fig.add_vline(x=threshold)
	elif feature == 1: # y axis
		fig.add_hline(y=threshold)

fig.write_html("hyperplanes.html")
os.system("open hyperplanes.html")

#dot_data = _tree.export_graphviz(tree, out_file=None)
#graph = graphviz.Source(dot_data)
#graph.render("a")
