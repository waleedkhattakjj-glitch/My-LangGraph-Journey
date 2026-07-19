from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

from langchain_core.messages.utils import trim_messages ,count_tokens_approximately
tokens = 500
def llm_call(state : chat_state):
    messages =trim_messages(
        state['messages'],
        strategy='last',
        token_counter=count_tokens_approximately,
        max_tokens=tokens
    )
    result = model.invoke(messages)
    return {'messages' : [result]}

from langgraph.graph import StateGraph
graph = StateGraph(chat_state)

graph.add_node('chat_node' , llm_call)

from langgraph.graph import START,END
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()
workflow = graph.compile(checkpointer= memory)
workflow

from langchain_core.messages import HumanMessage
config1 = {'configurable' : {'thread_id' : '1'}}
result = workflow.invoke({'messages' :[HumanMessage(content='hi my name is waleed ')]},config= config1)
print(result['messages'][-1].content)