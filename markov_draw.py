#!/usr/bin/env python

# Produces a graph of a markov chain given the names of the the states 
# and a transition matrix.


import yapgvb

edge_min = .002

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

def draw_chain(states, transition_matrix):
    g = yapgvb.Digraph('Markov Chain')

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
            if p>edge_min:
                edge=g.add_edge(state_list[i],state_list[j])
                edge.label=str(round(p*100,1))+'%'
                edge.labelfloat=False

    g.layout(yapgvb.engines.dot)
    g.render('MarkovChain.jpg')

if __name__ == '__main__':
    
    states = load_states()
    transition_matrix = load_data()

    print states
    print transition_matrix

    draw_chain(states, transition_matrix)
