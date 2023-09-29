from cumulative import add_smooth_cdf, add_step_cdf
from plotly.graph_objects import Figure, Scatter
import torch
import os

# Add some random numbers together to hopefully obtain a normal distribution
def random_normal_dist(sz, depth=16):
	return torch.rand(depth, sz).mean(0)

# Plotly's Histogram lacks styling options and looks bad by default
# Do not use it, instead bin using torch and use Scatter
data = random_normal_dist(1024)
v, k = torch.histogram(data, bins=32)

hist = Scatter(x=k, y=v/v.max(), name="p(x)")
hist.line.shape = "hvh" # Step lines

fig = Figure(hist)

# Some extra functions
# add_smooth_cdf(fig, data)
# add_step_cdf(fig, k, v)

fig.write_html("hist.html")
os.system("open hist.html")
