from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model ='gemini-3.1-flash-lite')

from langchain_core.tools import tool
@tool
def calculatur( num1 : float , num2 : float , operation : str) -> list  :
    "basic calculator of add , sub, mul and dev"
    if operation == 'add':
        return num1 + num2
    
    elif operation == 'mul':
        return num1 * num2
    
    elif operation == 'sub':
        return num1 - num2
    
    else :
        return num1 / num2
    
from langchain_community.tools import DuckDuckGoSearchResults
search_tool = DuckDuckGoSearchResults()

tools = [search_tool , calculatur]
llm_with_tools = model.bind_tools(tools)

from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]

# create your graph nodes (functions)
def chat_func(state: chat_state):
    'llm node that may answer or request a tool call'
    messages = state['messages']
    result = llm_with_tools.invoke(messages)
    return {'messages' : result}

# now craete a Tool node
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools)

# define graph
from langgraph.graph import StateGraph
graph = StateGraph(chat_state)

# add nodes
graph.add_node('chat_node',chat_func)
graph.add_node('tools' , tool_node)

# connect the nodes 
from langgraph.prebuilt import tools_condition
from langgraph.graph import START,END
graph.add_edge(START , 'chat_node')
graph.add_conditional_edges('chat_node' ,tools_condition )
graph.add_edge('tools' , 'chat_node')
graph.add_edge('chat_node' , END)

workflow = graph.compile()
workflow

from langchain_core.messages import HumanMessage, AIMessage
user_input = ' what is today latest news about AI Engineer Role and what  is 25 * 6'
result = workflow.invoke({'messages' : HumanMessage(content=user_input)})
print(result)

print(result['messages'][-1].content)