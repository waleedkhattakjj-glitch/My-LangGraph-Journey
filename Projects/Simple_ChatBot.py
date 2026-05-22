from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
model = ChatGroq(model= 'openai/gpt-oss-120b')

from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langgraph.graph.message import add_messages
class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages ]

def chat_func(state : chat_state):
    messages = state['messages']
    result = model.invoke(messages)

    return {'messages' : [result]}

from langgraph.graph import StateGraph
graph = StateGraph(chat_state)

graph.add_node('chat_node' , chat_func)

from langgraph.graph import START , END
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
workflow = graph.compile( checkpointer= checkpointer)

config1 = {'configurable' : {'thread_id' : '1'}}
while True:
    user = input("type here : ")
    print('user :' , user)
    if user != 'exit':
        result = workflow.invoke({'messages': [HumanMessage(content=user)]} , config= config1 )
        print('AI :' , result['messages'][-1].content)
    else :
        break