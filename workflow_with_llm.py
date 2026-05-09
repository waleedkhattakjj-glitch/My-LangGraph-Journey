# Workflow with llm 
# how langChain and langGraph work together
# pip install langChain

# LLM (model)
# pip install langchain-groq
# pip install python-dotenv
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
model = ChatGroq(
    model="enter your model here",
    temperature=1.5,
)

p = "what is the capital of pakistan"
r = model.invoke(p)
print(r.content)

# (1) now first make states with the help of class and class should be inherit TypedDict
from typing import TypedDict
class llm_state(TypedDict):
    question : str
    answer : str
     

# (2) now define function

def llm_work( state : llm_state ) -> llm_state:
    # now here first we extract question from state
    question =state['question']
    
    # now arite prompt for llm
    prompt = f" Answer the followi ng Question \n :{question}"
    
    # now invoke the model
    answer = model.invoke(prompt).content
    
    # now update the state 
    state['answer'] = answer
    return state

# (3) now make a Graph
from langgraph.graph import StateGraph
graph = StateGraph(llm_state)

# (4) now make nodes in graph and add function to node

graph.add_node("llm_node", llm_work)

# (5) now add edges between nodes
from langgraph.graph import START , END
graph.add_edge(START, "llm_node")
graph.add_edge('llm_node' , END)

# (6) now compile graph
workflow = graph.compile()

f_answer = workflow.invoke({'question' : "AI in pakistan"})
print(f_answer)

from IPython.display import Image
Image(workflow.get_graph().draw_mermaid_png())
