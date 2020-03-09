# Epidemic

Use graph visualization to study the spread of Epidemics.  

## Burndown

- [ ] Graph
	- [x] Node
	- [x] Edge
		- [x] Weights -- Represent probability of infection given that one vertex is infected and one vertex isn't over some time period e.g. a day
	- [x] To pyvis
	- [ ] Combine -- Given multiple graphs with the same nodes representing different types of vectors (say, % infection at home with family vs. % infection at work => p = 1 - (1 - p_0)\*(1 - p_1)
- [ ] CLI
	- [x] Basic display of N nodes
- [ ] Time evolution
	- [ ] Initial conditions
	- [ ] Length of infection
	- [ ] Ability to evolve graph

## Usage

From root directory,

`python3 ./src/visualize_graph.py [Number of nodes]`