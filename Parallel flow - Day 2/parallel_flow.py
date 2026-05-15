# parallel_flow

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# define state
class cricketstate(TypedDict):
    runs: int
    balls: int
    fours: int
    sixes: int
    stricke_rate: float
    boundary_percentage: float
    balls_per_boundary: float
    summary: str


# strike rate function
def strick_rate_func(state: cricketstate) -> dict:
    runs = state['runs']
    balls = state['balls']
    stricke_rate = (runs / balls) * 100
    return {'stricke_rate': stricke_rate}


# boundary_percentage function
def boundary_percentage_func(state: cricketstate) -> dict:
    runs = state['runs']
    fours = state['fours']
    sixes = state['sixes']
    boundry_runs = (fours * 4) + (sixes * 6)
    boundary_percentage = (boundry_runs / runs) * 100
    return {'boundary_percentage': boundary_percentage}


# balls_per_boundary function
def balls_per_boundary_func(state: cricketstate) -> dict:
    balls = state['balls']
    fours = state['fours']
    sixes = state['sixes']
    total_boundry = fours + sixes
    balls_per_boundary = balls / total_boundry
    return {'balls_per_boundary': balls_per_boundary}


# summary function
def summary_func(state: cricketstate) -> dict:
    stricke_rate = state['stricke_rate']
    boundary_percentage = state['boundary_percentage']
    balls_per_boundary = state['balls_per_boundary']
    summary = f"Strick Rate : {stricke_rate} , Boundary Percentage : {boundary_percentage} , Balls per Boundary : {balls_per_boundary}"
    return {'summary': summary}


# define graph
graph = StateGraph(cricketstate)

graph.add_node('boundary_percentage_node', boundary_percentage_func)
graph.add_node('balls_per_boundary_node', balls_per_boundary_func)
graph.add_node('strick_rate_node', strick_rate_func)
graph.add_node('summary_node', summary_func)

graph.add_edge(START, 'boundary_percentage_node')
graph.add_edge(START, 'balls_per_boundary_node')
graph.add_edge(START, 'strick_rate_node')
graph.add_edge('boundary_percentage_node', 'summary_node')
graph.add_edge('balls_per_boundary_node', 'summary_node')
graph.add_edge('strick_rate_node', 'summary_node')
graph.add_edge('summary_node', END)

workflow = graph.compile()

final_ans = workflow.invoke({'runs': 120, 'balls': 80, 'fours': 10, 'sixes': 5})
print(final_ans)