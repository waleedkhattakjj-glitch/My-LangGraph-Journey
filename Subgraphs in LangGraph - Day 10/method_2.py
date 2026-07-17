from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
child_model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')
parent_model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

from typing import TypedDict
class ParentState(TypedDict):
    text : str
    eng_text : str
    urdu_text : str

def child_urdu_translation_func(state : ParentState):
    english = state['eng_text']
    p=f"""Convert the Foloowing text into Urdu 
    Dont Add Extra Content \n\n
    TEXT: {english}"""
    result = child_model.invoke(p)
    return {'urdu_text' : result}

from langgraph.graph import StateGraph,START,END
subgraph = StateGraph(ParentState)

subgraph.add_node('urdu_conversion_node' , child_urdu_translation_func)

subgraph.add_edge(START , 'urdu_conversion_node')
subgraph.add_edge('urdu_conversion_node' , END)

childgraph = subgraph.compile()
childgraph

# Parent Graph
def Parent_english_generation(state : ParentState):
    text = state['text']
    p=f""" You Are A Helpfull Assistance
    Answer The Questions \n\n
    {text}"""
    result = parent_model.invoke(p).content
    return {'eng_text': result}

from langgraph.graph import StateGraph,START,END
graph = StateGraph(ParentState)

graph.add_node('english_generation_node' , Parent_english_generation)
graph.add_node('urdu_generation_node' , childgraph)

graph.add_edge(START , 'english_generation_node')
graph.add_edge('english_generation_node' , 'urdu_generation_node')
graph.add_edge('urdu_generation_node' , END)

workflow = graph.compile()

workflow

r = workflow.invoke({'text':'what is ml explain in 50 words'})
print(r['urdu_text'])