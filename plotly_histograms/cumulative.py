import torch

# Smooth Cumulative Distribution Function
# Attempts to fit a normal distribution
# Samples 100 points
def add_smooth_cdf(fig, data):
	distribution = torch.distributions.Normal(data.mean(), data.std())
	x = torch.linspace(data.min(), data.max(), 100)
	y = distribution.cdf(x)

	fig.add_scatter(x=x, y=y, name="F(x)")

# Step cumulative distribution
# Sums the values
# Uses bin points
def add_step_cdf(fig, k, v):
	z = torch.cumsum(v, 0)
	z /= z[-1].item()

	trace = fig.add_scatter(x=k, y=z, name="F(x)", line={"shape": "hvh"})
