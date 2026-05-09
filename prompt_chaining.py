# prompt_chaining_workflow

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGroq(
    model="enter your model name here", ,
    temperature= 1.5
)
r = llm.invoke("when is pakistan independed")
print(r)

from typing import TypedDict
class pc_state(TypedDict):
    title : str
    gen_outline : str
    gen_blog : str
     

# create your first fuction for the node which will generate outline from the topic
def gen_outline_func(state : pc_state) -> pc_state :
   # extract the topic from the state
    title = state['title']
    
    # now generate outline from the topic
    prompt1 = f' generate an detailed outline for a blog on the topic {title}'
    
    # now we will give this  prompt1 to llm 
    gen_outline = llm.invoke(prompt1).content
    
    # and now import that gen_outline to the state (update state)
    state['gen_outline'] = gen_outline
    return state

# create your secod function for the blog 
def gen_blog_func(state : pc_state) -> pc_state :
    # now extact the title and gen_outline from the state 
    title = state['title']
    gen_outline = state['gen_outline']
    
    prompt2 = f'write a detail blog on the title {title} using the following outline \n {gen_outline}'
    
    #now give that prompt2 to llm
    gen_blog = llm.invoke(prompt2).content
    
    # now update the state again
    state['gen_blog'] = gen_blog
    return state

# now define graph and give your state u define
from langgraph.graph import StateGraph
graph = StateGraph(pc_state)

# now add your node ( function)
graph.add_node('outline_node' , gen_outline_func)
graph.add_node('blog_node' , gen_blog_func)

# now connect the edges between nodes
from langgraph.graph import START , END

graph.add_edge( START, 'outline_node')
graph.add_edge( 'outline_node' , 'blog_node')
graph.add_edge( 'blog_node' , END)

# now compile graph
workflow = graph.compile()

ip = { 'title' : "Rise of Artificial Intelligence in pakistan"}
f_result = workflow.invoke(ip)
print(f_result)

print(f_result['gen_outline'])

print(f_result['gen_blog'])