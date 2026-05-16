from typing import TypedDict
class check_state(TypedDict):
    num : int
    positive : int
    negative : int
    zero : int
    result : str


def positive_func( state : check_state ):
    result = f"the  {state['num']} is positive number"
    return { 'result' : result }


def negative_func( state : check_state ):
    result = f"the  {state['num']} is negative number"
    return { 'result' : result }


def zero_func( state : check_state ):
    result = f"the  {state['num']} is zero number"
    return { 'result' : result }


from typing import Literal

# Change the return type hint and the return values to strings
def condition_func(state : check_state) -> Literal['positive_node', 'negative_node', 'zero_node']:
    if state['num'] > 0:
        return 'positive_node'  # Matches the name in graph.add_node
    elif state['num'] < 0:
        return 'negative_node'
    else:
        return 'zero_node'


from langgraph.graph import StateGraph
graph = StateGraph (check_state)


graph.add_node('positive_node' , positive_func)
graph.add_node('negative_node' , negative_func)
graph.add_node('zero_node' , zero_func)


from langgraph.graph import START , END

graph.add_conditional_edges(START , condition_func)
graph.add_edge('positive_node' , END)
graph.add_edge('negative_node' , END)
graph.add_edge('zero_node' , END)


workflow = graph.compile()
workflow


a = {'num':0}
r = workflow.invoke(a)
print(r)