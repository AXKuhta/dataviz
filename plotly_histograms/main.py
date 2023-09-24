from plotly.graph_objects import Figure, Scatter
import torch
import os

# Add some random numbers together to hopefully obtain a normal distribution
def random_normal_dist(sz, depth=16):
	return torch.rand(depth, sz).sum(0) / depth

# Plotly's Histogram lacks styling options and looks bad by default
# Do not use it, instead bin using torch and use Scatter
data = random_normal_dist(512)
v, k = torch.histogram(data, bins=32)

hist = Scatter(x=k, y=v, name="p(x)")
hist.line.shape = "hvh" # Step lines
fig = Figure(hist)

fig.write_html("hist.html")
os.system("open hist.html")
