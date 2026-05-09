# simple_workflow.py

# sequential workflow
# how to make a graph in langGraph
# it have 7 steps 
# we are going to make a ibm calculator

# 1) Define states with the help of the class and it will inherit TypedDict
from typing import TypedDict
class bmi_state(TypedDict):
    height_in_CM : float
    weight_in_Kg : float
    bmi : float
    

# 2) define function ( processing of the bmi calculator) and in function instate = ( provide the state u define)
def bmi_cal (state : bmi_state) -> bmi_state : # it means that in input we got a state object (that we define in the state) and in output we got stae object
    # now extract the height and weight value from state
    # and it should be store in new variable
    height = state['height_in_CM']
    weight = state['weight_in_Kg']
    # now we need to calculate the bmi value and store it in new variable
    bmi = weight / (height/100)**2
    # now we need to update the state with the new value of bmi
    state['bmi'] = bmi
    # now we need to return the state
    return state

# 3) now define Graph
from langgraph.graph import StateGraph
graph = StateGraph(bmi_state) # it means that we are going to use the state that we define in the graph

# 4) now add Nodes(functions) to your Graph
graph.add_node('bmi_calculator' , bmi_cal) # first define your node name and then add the function that you define in step 2

# 5) now we need to define the edges ( Connection between nodes)
# edges have 2 dumies nodes that tells where to START and where to END
from langgraph.graph import START, END
graph.add_edge(START , 'bmi_calculator')
graph.add_edge('bmi_calculator' , END)

# 6) now compile the graph
workflow = graph.compile()

# 7) now execute the graph
final_workflow = workflow.invoke({ 'weight_in_Kg' : 70 , 'height_in_CM' : 170 })
print(final_workflow) 

from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())