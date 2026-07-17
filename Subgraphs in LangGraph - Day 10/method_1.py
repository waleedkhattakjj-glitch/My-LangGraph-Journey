from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

from typing import TypedDict
class SubState(TypedDict):
       eng_text : str
       urdu_text : str

def urdu_translation(state : SubState):
    
    p=f"""Translate the following text into urdu
    Do not add extra content and Keep it clear
    TEXT = {state['eng_text']}"""
    result = model.invoke(p).content
    return {'urdu_text' : result}

from langgraph.graph import StateGraph
subgraph = StateGraph(SubState)

subgraph.add_node('translation_node' , urdu_translation)

from langgraph.graph import START,END
subgraph.add_edge(START,'translation_node')
subgraph.add_edge('translation_node',END)

childgraph = subgraph.compile()

childgraph

result = childgraph.invoke({'eng_text' : '**Agentic AI** refers to AI systems that are designed to go beyond simply generating content or answering questions. Instead, they act as **autonomous agents** that can perceive their environment, reason through complex tasks, and take independent actions to achieve a specific goal.'})
print(result['urdu_text'])

# PARENT GRAPH
from typing import TypedDict
class ParentState(TypedDict):
    question : str
    genrate_text : str
    urdu_generation :str

def question_func(state : ParentState):
    question = state['question']
    p=f""" You are a helpfull assistance.
    Answer Clearly \n\n
    Question : {question}"""
    result = model.invoke(p).content
    return {'genrate_text': result}
    

def urdu_generation(state : ParentState):
    english_text = state['genrate_text']
    result = childgraph.invoke({'eng_text' : english_text})
    return {'urdu_generation': result['urdu_text']}

from langgraph.graph import StateGraph
graph = StateGraph(ParentState)

graph.add_node('question_node' , question_func)
graph.add_node('generation_node' , urdu_generation)

from langgraph.graph import START,END
graph.add_edge(START,'question_node')
graph.add_edge('question_node', 'generation_node')
graph.add_edge('generation_node',END)

workflow = graph.compile()

workflow

r = workflow.invoke({'question': 'what is agentic AI'})

print(r['urdu_generation'])