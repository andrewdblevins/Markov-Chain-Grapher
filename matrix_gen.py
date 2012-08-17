###################################################################################################
#
#            matrix_gen.py
#    By Andrew Blevins and Sara Smoot
#
#    usage: 
#    >>>python matrix_gen.py <sorted_list_of_facts_in_tsv_format>
#
#    installation:
#    the following package must be installed to render images:
#    >>>sudo apt-get install python-yapgvb 
#
#    
#
#################################################################################################
import csv
import sys

from collections import defaultdict
from collections import namedtuple


from datetime import datetime
from datetime import date

import markov_draw


csv.register_dialect('tsv',delimiter='\t', quoting=csv.QUOTE_NONE)

states = []


TIMED_OUT = 1800



customer_states = defaultdict(list)
Fact = namedtuple('Fact', 'table_id cid fact_id date_time attr1 attr2 attr3 attr4 attr5 attr6 attr7 attr8 attr9 attr10 attr11 attr12 attr13 attr14 attr15 attr16 attr17 attr18 attr19 attr20')
State = namedtuple('State','cid time name')

transition_matrix = defaultdict(lambda : defaultdict(int))


def read_fact(line):
    fact = Fact._make(line)
    return fact

def sort_fact_to_state(fact):

    state = fact.fact_id

    if fact.fact_id == '101651' and fact.attr1 == 'panel':
        state =  (fact.cid,fact.date_time,'View Label') 

    if fact.fact_id == '101651' and fact.attr1 != 'panel':
        state =  (fact.cid,fact.date_time,'View Photostream')

    if fact.fact_id == '101653':
        state =  (fact.cid,fact.date_time,'View Photo')

    if fact.fact_id == '101652':
        state =  (fact.cid,fact.date_time,'View Product')

    if fact.fact_id == '101654':
        state =  (fact.cid,fact.date_time,'Try on Product')

    if fact.fact_id == '101662':
        return None

    if fact.fact_id == '23':
        state =  (fact.cid,fact.date_time,'Buy')
       
    state = (state[0],datetime.strptime(state[1], "%Y-%m-%d %H:%M:%S"),state[2])
    return State._make(state)

def add_state(state):
    global customer_states
    try:
        customer_states[state.cid].append((state.time,state.name))
    except Exception, e:
        print 'Unhandled State:  '
        pass

def tally_transition(state1,state2,dt):
    if state1 not in states:
        states.append(state1)
    if state2 not in states:
        states.append(state2)
#    print (state1,state2,dt)
    if dt > 1:
        transition_matrix[state1][state2]+=1

def prepare_to_draw(states,transition_matrix):
    tm = []
    for i in states:
        row = []
        rowsum = 0
        for j in states:
            rowsum += transition_matrix[i][j]
        for j in states:
            print float(transition_matrix[i][j]/float(rowsum)),
            row.append(float(transition_matrix[i][j]/float(rowsum)))
        tm.append(row)
        print
    return states, tm

if __name__ == '__main__':
    filename = sys.argv[1]

    prev_state = State._make((0,0,None))
    for line in csv.reader(open(filename,'rb'),'tsv'):
        fact = read_fact(line)
        
        state = sort_fact_to_state(fact)
        if not state:
            continue
        add_state(state) 
        if prev_state.cid == state.cid and prev_state.name != None:
            if (TIMED_OUT < (state.time-prev_state.time).seconds):
                tally_transition(prev_state.name,'Exit',0)
                tally_transition('Exit',state.name,(state.time-prev_state.time).seconds)
            else:
                tally_transition(prev_state.name,state.name,(state.time-prev_state.time).seconds)
        else:
            if prev_state.name != None:
                tally_transition(prev_state.name,'Exit',0)
        prev_state = state

    s,tm = prepare_to_draw(states,transition_matrix)
    markov_draw.draw_chain(s,tm)
#   pp = pprint.PrettyPrinter(indent = 2, width=80) 
#   pp.pprint(dict(customer_states))
    
