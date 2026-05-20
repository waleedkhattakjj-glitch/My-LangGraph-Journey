# Persistence
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq ( model = 'openai/gpt-oss-120b')

from typing import TypedDict
class joke_state(TypedDict):
    topic : str
    joke : str
    explanation : str

def joke_func(state : joke_state):
    topic = state['topic']
    prompt1 = f" make a joke on the topic {topic}"
    result = model.invoke(prompt1).content
    return {'joke' : result}

def explanation_func( state : joke_state):
    joke = state['joke']
    prompt2 = f" give a 50 charactors explanation of this joke {joke}"
    result = model.invoke(prompt2).content
    return {'explanation' : result}

from langgraph.graph import StateGraph
graph = StateGraph(joke_state)

graph.add_node('joke_node' , joke_func )
graph.add_node('explanation_node' , explanation_func )

from langgraph.graph import START , END
graph.add_edge( START , 'joke_node' )
graph.add_edge( 'joke_node' , 'explanation_node' )
graph.add_edge( 'explanation_node' , END)

from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer= checkpointer)

config1 = {'configurable' : {'thread_id' : '1'}}
result = workflow.invoke({'topic' : 'pizza'} , config= config1)
print(result)

print(result['topic'])
print('/n/n')

print(result['joke'])
print('/n/n')

print(result['explanation'])
print('/n/n')

workflow.get_state(config1)

list(workflow.get_state_history(config1))