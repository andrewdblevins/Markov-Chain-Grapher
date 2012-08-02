#!/usr/bin/env python

# Produces a graph of a markov chain given the names of the the states 
# and a transition matrix.


import yapgvb

def load_states():
    f = open('states.tsv')
    lines = f.readlines()
    states = [x for x in lines]
    return states

def load_data():
    f = open('data.tsv')
    lines = f.readlines()
    transition_matrix = [[float(y) for y in x.split('\t')] for x in lines]
    return transition_matrix 
    
if __name__ == '__main__':
    g = yapgvb.Digraph('Markov_Chain')
    
    states = load_states()
    transition_matrix = load_data()
    m = len(transition_matrix)
    state_list = []

    for state in states:
        state_node =  g.add_node(state,
        label = state,
        shape = yapgvb.shapes.doublecircle,
        color = yapgvb.colors.blue,
        fontsize = 12)

        state_list.append(state_node)

    for i in range(m):
        for j in range(m):
            p = transition_matrix[i][j]
            if p!=0.0:
                edge=g.add_edge(state_list[i],state_list[j])
                edge.label=str(p*100)+'%'
                edge.labelfloat=False

    g.layout(yapgvb.engines.dot)
    g.render('MarkovChain.jpg')
