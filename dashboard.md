<head>
<meta charset="UTF-8">
<link rel="stylesheet" type="text/css" href="stmarkdown.css">
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
</script>
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_CHTML">
</script>
</head>

# Stata/Python intergration

Stata provides two ways for Python and Stata to interact, and we refer to these mechanisms collectively as PyStata.

## Use Python within Stata  - Stata 16

Python can be invoked from a running Stata session so that Python's extensive language features can be leveraged from within Stata.

```
<<dd_do>>
python:
print("Hello!")
end
<</dd_do>>
``` 

[Chuck's blog series](https://blog.stata.com/2020/08/18/stata-python-integration-part-1-setting-up-stata-to-use-python/)


## Use Stata from Python  - Stata 17

Stata can be invoked from a standalone Python environment via the pystata Python package. It includes three IPython (interactive Python) magic commands and a suite of API functions for interacting with Stata.

* [Configure stata](https://www.stata.com/python/pystata/install.html#method-1-installing-via-pip)

* [Use Stata in Jupyter](https://www.stata.com/new-in-stata/jupyter-notebooks/)

* [Stata Python API](https://www.stata.com/python/api17/)

## Use Stata with Python/dash to generate dashboard

[An example](./src/dashboard.py)

## Use Stata to generate maps

* spmap (grmap)

```
use ./data/covid19_adj, replace
grmap, activate
drop if province_state == "Alaska" | province_state == "Hawaii"
spset, modify shpfile(usacounties_shp)
grmap confirmed_adj, clnumber(7)
```

<<dd_do: quietly>>
use ./data/covid19_adj, replace
grmap, activate
drop if province_state == "Alaska" | province_state == "Hawaii"
spset, modify shpfile(usacounties_shp)
grmap confirmed_adj, clnumber(7)
<</dd_do>>

<<dd_graph: saving(map_ex0.svg) replace>>


[src](./src/covid19_ts.do)

* maptile

```
sysuse census
rename (state state2) (statename state)
gen babyperc=poplt5/pop*100
maptile babyperc, geo(state)
```


<<dd_do: quietly>>
sysuse census, clear
rename (state state2) (statename state)
gen babyperc=poplt5/pop*100
maptile babyperc, geo(state)
<</dd_do>>

<<dd_graph: saving(map_ex1.svg) replace>>

* Use Python

<<dd_do:quietly>>
cd ./src
* do covid19_py
cd ..
<</dd_do>>

<img src="./images/fig1.svg">

[src](../src/covid19_py.do)

# 3d gif
```
stata.run('sysuse sandstone, clear')
D = stata.nparray_from_data("northing easting depth")

ax = plt.axes(projection='3d')
plt.xticks(np.arange(60000, 90001, step=10000))
plt.yticks(np.arange(30000, 50001, step=5000))
ax.plot_trisurf(D[:,0], D[:,1], D[:,2], cmap=plt.cm.Spectral, edgecolor='none')

for i in range(0, 360, 10):
	ax.view_init(elev=10., azim=i)
	plt.savefig("../gif/sandstone"+str(i)+".png")
	
with io.get_writer('../gif/sandstone.gif', mode='I', duration=0.5) as writer:
	for i in range(0, 360, 10):
		image = io.imread("../gif/sandstone"+str(i)+".png")
		writer.append_data(image)
writer.close()
```

<img src="./gif/sandstone.gif">
