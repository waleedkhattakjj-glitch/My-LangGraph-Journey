from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model = 'gemini-3.1-flash-lite')

from langchain_community.document_loaders import PyPDFLoader
path = "data for chatbot.pdf.pdf"
loader = PyPDFLoader(path)
doc = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter
chunk = RecursiveCharacterTextSplitter(
    chunk_size = 500 ,
    chunk_overlap = 100
)
chunks = chunk.split_documents(doc)

from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model='bge-m3:567m')

from langchain_community.vectorstores import Chroma
vector_database = Chroma(
    embedding_function=embedding_model,
    persist_directory='chroma_embed_db',
    collection_name='sample'
)
vector_database.add_documents(chunks)

retriever = vector_database.as_retriever(
    search_type="similarity",
    search_kwargs={'k': 5}
)

from langchain.tools import tool
@tool
def rag_tool(query : str ) -> str :
    "this tool is for to search the data from private data(pdf document)"
    result = retriever.invoke(query)
    context = [doc.page_content for doc in result]
    
    return {'context' : context , 'user_query' : query}

tools = [rag_tool]
llm_with_tools = model.bind_tools(tools)

from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
class chatbot_state(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    

def chatbot_func(state : chatbot_state) :
    yoyo = state['messages']
    result = llm_with_tools.invoke(yoyo)
    return {'messages' : [result] }

# tool node
from langgraph.prebuilt import ToolNode
tool_node = ToolNode(tools)

from langgraph.graph import StateGraph
graph = StateGraph(chatbot_state)

graph.add_node('chatbot_node' , chatbot_func)
graph.add_node('tools' , tool_node)

from langgraph.graph import START , END
from langgraph.prebuilt import tools_condition
graph.add_edge(START , 'chatbot_node')
graph.add_conditional_edges('chatbot_node' , tools_condition)
graph.add_edge('tools' , 'chatbot_node')

workflow = graph.compile()
workflow

from langchain_core.messages import HumanMessage
result = workflow.invoke({"messages" : [HumanMessage(content=("from the given pdf tell me who is the instructor of digital markiting "))]})

print(result['messages'][-1].content)