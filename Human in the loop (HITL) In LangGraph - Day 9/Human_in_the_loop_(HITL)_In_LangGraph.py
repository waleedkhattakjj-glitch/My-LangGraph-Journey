from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model= 'gemini-3.1-flash-lite')

from typing import Annotated , TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class chat_state(TypedDict):
    topic : str
    messages : Annotated[list[BaseMessage] ,add_messages]
    checker : str

from langchain_core.output_parsers import StrOutputParser
parser = StrOutputParser()
def topic_func(state : chat_state):
    topic = state['topic']
    prompt=f"""<ROLE>you are a senior social media manager with 10+ years experiance</ROLE>
    <GOAL>your work is to make a post on {topic} and post it on social media</GOAL>
    <INSTRUCTIONS>
    <INSTRUCTION> the post should be 60 words </INSTRUCTION>
    <INSTRUCTION> the post should be new and not generated before to any other user </INSTRUCTION>
    </INSTRUCTIONs>"""
    plain = model | parser
    result = plain.invoke(prompt)
    return {'checker': result}

from langgraph.types import interrupt , Command
def human_func(state : chat_state) :
    checker = state['checker']
    decision = interrupt(f'Approve this {checker} ? (yes\\no)')
    if decision.lower() == 'yes':
        return {'checker': 'The post is submitted successfully on LinkedIn'} 
    else:
        return {'checker': 'The post is Canceled'}

from langgraph.graph import StateGraph

graph = StateGraph(chat_state)

graph.add_node('chat_node' , topic_func)
graph.add_node('human_node', human_func)

from langgraph.graph import START , END
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node', 'human_node')
graph.add_edge('human_node',END)

from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()
workflow = graph.compile(checkpointer=memory)
workflow

from langchain_core.messages import HumanMessage

while True:
    user_input = input('enter the topic')
    print('USER:', user_input)
    if user_input == 'exit':
        break
    config1 = {'configurable':{'thread_id':'1'}}
    result = workflow.invoke({'topic':user_input},config= config1)
    interrupts = result.get('__interrupt__',[])
    
    if interrupts:
        prompt_to_human = interrupts[0].value
        print('HITL:',prompt_to_human)
        desicion = input('your desicion = ')
        
        result = workflow.invoke(Command(resume=desicion),config= config1)
    print('AI:',result['checker'])

print(result)