from plotly.graph_objects import Scatter, Figure
from graph_functions import split_nodes_edges
import shapely.prepared
import shapely
import math
import json
import os

def distance(site_1, site_2):
	loc_1 = site_1["location"]
	loc_2 = site_2["location"]
	r = 6371

	phi_1 = math.radians(loc_1["lat"])
	phi_2 = math.radians(loc_2["lat"])

	d_phi = math.radians(loc_2["lat"] - loc_1["lat"])
	d_lambda = math.radians(loc_2["lon"] - loc_1["lon"])

	a = math.sin(d_phi/2)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(d_lambda/2) ** 2
	c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

	return r * c

def build_graph(sites, max_distance=math.inf):
	edges = []
	nodes = []
	nodes_d = {}

	total = len(sites)
	i = 1

	print("")

	while sites:
		print(f"\r{i}/{total}", end="")
		src = sites.pop(0)
		i = i + 1

		for dst in sites:
			d = distance(src, dst)

			if d > max_distance:
				continue

			edges.append( (src["code"], dst["code"], d) )

		nodes_d[src["code"]] = src

	print("")

	return nodes_d, nodes, edges


with open("continents.json") as f:
	continents = json.load(f)
	north_america = continents["features"][1]["geometry"]["coordinates"]

	subcontinents = []

	for subcontinent in north_america:
		bound_lons = []
		bound_lats = []

		for points in subcontinent:
			for c in points:
				lon, lan = c

				bound_lons.append(lon)
				bound_lats.append(lan)

		# Ленивый способ, ну и ладно
		if shapely.Polygon(points).area < 2580.0:
			continue
		else:
			north_america_poly = shapely.Polygon(points)

		subcontinents.append( (bound_lons, bound_lats) )

with open("base.json") as f:
	sites = json.load(f)
	print(len(sites))
	print(sites[0])

	lons = []
	lats = []

	us_sites = []
	us_lons = []
	us_lats = []

	# Prepared позволяет быстрее выполнять много операций contains()
	north_america_poly_prep = shapely.prepared.prep(north_america_poly)

	for site in sites:
		lon = site["location"]["lon"]
		lat = site["location"]["lat"]

		point = shapely.Point([lon, lat])

		if north_america_poly_prep.contains(point):
			us_sites.append(site)
			us_lons.append(lon)
			us_lats.append(lat)
		else:
			lons.append(lon)
			lats.append(lat)

# 800 км является "минимальным" максимальным расстоянием, при котором этот граф не развалится на несколько подграфов ещё до кластеризации
nodes_d, nodes, edges = build_graph(us_sites, 800)
split = split_nodes_edges(nodes, edges, 40)

clusters = []

for island in split:
	cluster_points_x = []
	cluster_points_y = []

	for edge in island.edges:
		x1 = nodes_d[edge[0]]["location"]["lon"]
		x2 = nodes_d[edge[1]]["location"]["lon"]

		y1 = nodes_d[edge[0]]["location"]["lat"]
		y2 = nodes_d[edge[1]]["location"]["lat"]

		cluster_points_x.append(x1)
		cluster_points_x.append(x2)
		cluster_points_x.append(None)
		cluster_points_y.append(y1)
		cluster_points_y.append(y2)
		cluster_points_y.append(None)

	clusters.append( Scatter(x=cluster_points_x, y=cluster_points_y, mode="lines") )

us_stations = Scatter(x=us_lons, y=us_lats, mode="markers", name="US Stations")
stations = Scatter(x=lons, y=lats, mode="markers", name="Stations")
subconts = [
	Scatter(x=sub[0], y=sub[1], mode="lines", name="Continent") for sub in subcontinents
]

fig = Figure(subconts + [stations, us_stations] + clusters)

fig.write_html("map.html")
os.system("firefox map.html")

