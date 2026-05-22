from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
model = ChatGroq(model='openai/gpt-oss-120b')

from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class chatbot_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

def chat_func(state : chatbot_state) -> chatbot_state :
    messages = state['messages']
    result = model.invoke(messages)
    return {'messages' : result}

from langgraph.graph import StateGraph
graph = StateGraph(chatbot_state)

graph.add_node('chatbot_node' , chat_func)

from langgraph.graph import START , END
graph.add_edge(START , 'chatbot_node')
graph.add_edge('chatbot_node' , END)

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
connection = sqlite3.connect(database='chatbot.db' , check_same_thread= False)
checkpointer = SqliteSaver(conn= connection)
workflow = graph.compile(checkpointer= checkpointer)
workflow

from langchain_core.messages import HumanMessage, AIMessage
config1 = {'configurable' : {'thread_id' : '1'}}
while True:
    user_input = input('type here : ')
    print('User: ',user_input)
    if user_input != 'exit' :
        result = workflow.invoke({'messages' : HumanMessage(content=user_input)}, config= config1)
        print('AI: ', result['messages'][-1].content)
    else :
        break