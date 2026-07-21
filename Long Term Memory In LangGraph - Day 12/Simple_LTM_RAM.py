from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

from langgraph.store.memory import InMemoryStore
store = InMemoryStore()

user_data = ("user","u1","details")

store.put(user_data,"profile_1",{'data':'name : waleed'})
store.put(user_data,"profile_1",{'data':'proffession : AI Engineer'})
store.put(user_data,"profile_1",{'data':'Bulding projects in generative and agentic AI'})
store.put(user_data,"profile_1",{'data':'likes to playing games'})
store.put(user_data,"profile_1",{'data':'prefers concis answers'})

system_prompt = """You are a helpful assistant with memory capabilities. If user-specific memory is available, use it to personalize your responses based on what you know about the user.

Your goal is to provide relevant, friendly, and tailored assistance that reflects the user's preferences, context, and past interactions.

If the user's name or relevant personal context is available, always personalize your responses by:

Always Address the user by name (e.g., "Sure, Waleed…") when appropriate
Referencing known projects, tools, or preferences (e.g., "your generative and agentic AI based project")
Adjusting the tone to feel friendly, natural, and directly aimed at the user
Avoid generic phrasing when personalization is possible. For example, instead of "In TypeScript apps…" say "Since your project is built with TypeScript..."

Use personalization especially in:

Greetings and transitions
Help or guidance tailored to tools and frameworks the user uses
Follow-up messages that continue from past context
Always ensure that personalization is based only on known user details and not assume.

In the end suggest 3 relevant further questions based on the current response
the user memory (which may be empty) is provided as: {user_detail}"""

from langgraph.graph.message import add_messages
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage

class chat_state(TypedDict):
    messages : Annotated[list[BaseMessage] ,add_messages]

from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

def chat_func(state : chat_state , config : RunnableConfig , store : BaseStore ):
    user_id = config['configurable']['user_id']
    
    user_data = ("user","u1","details")
    items = store.search(user_data)
    
    if items :
        user_detail ="\n".join(f'-{it.value.get('data','')} 'for it in items)
        
    else:
        user_detail = ""
        
    from langchain_core.messages import SystemMessage
    final_system_prompt = system_prompt.format(
        user_detail = user_detail
    )
    
    system_message = SystemMessage(content=final_system_prompt)
    messages = state['messages']
    all_messages = [system_message] + messages  # NOT [messages]
    
    # Invoke the model
    result = model.invoke(all_messages)
    return {'messages' : [result]}

from langgraph.graph import StateGraph
graph = StateGraph(chat_state)

graph.add_node('chat_node' , chat_func)

from langgraph.graph import START , END 

graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

workflow = graph.compile(store=store)
workflow

config = {'configurable': {'user_id':'u1'}}
from langchain_core.messages import HumanMessage
result = workflow.invoke({'messages' : [HumanMessage(content='explan genai in simple term')]},config=config)
print(result['messages'][-1])

from dotenv import load_dotenv
load_dotenv()

import uuid
from typing import List
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore

# 1) LTM store
store = InMemoryStore()

from langchain_google_genai import ChatGoogleGenerativeAI
memory_llm = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite', temperature=0)

class MemoryItem(BaseModel):
    text: str = Field(description="Atomic user memory as a short sentence")
    is_new: bool = Field(description="True if this memory is NEW and should be stored. False if duplicate/already known.")

class MemoryDecision(BaseModel):
    should_write: bool = Field(description="Whether to store any memories")
    memories: List[MemoryItem] = Field(default_factory=list, description="Atomic user memories to store")

memory_extractor = memory_llm.with_structured_output(MemoryDecision)

MEMORY_PROMPT = """You are responsible for updating and maintaining accurate user memory.

CURRENT USER DETAILS (existing memories):
{user_details_content}

TASK:
- Review the user's latest message.
- Extract user-specific info worth storing long-term (identity, stable preferences, ongoing projects/goals).
- For each extracted item, set is_new=true ONLY if it adds NEW information compared to CURRENT USER DETAILS.
- If it is basically the same meaning as something already present, set is_new=false.
- Keep each memory as a short atomic sentence.
- No speculation; only facts stated by the user.
- If there is nothing memory-worthy, return an empty list.
"""

def chat_creates_memory_node(state: MessagesState, config: RunnableConfig, store: BaseStore):

    user_id = config["configurable"]["user_id"]

    namespace = ("user", user_id, "details")

    # A) Load existing memories
    existing_items = store.search(namespace)
    existing_texts = [it.value.get("data", "") for it in existing_items if it.value.get("data")]
    user_details_content = "\n".join(f"- {t}" for t in existing_texts) if existing_texts else "(empty)"

    # B) Latest user message
    last_text = state["messages"][-1]

    # C) LLM extracts memories + marks new vs duplicate
    decision: MemoryDecision = memory_extractor.invoke(
        [
            SystemMessage(content=MEMORY_PROMPT.format(user_details_content=user_details_content)),
            {"role": "user", "content": f"USER MESSAGE:\n{last_text}"},
        ]
    )

    # D) Store ONLY new memories
    if decision.should_write:
        for mem in decision.memories:
            if mem.is_new:
                store.put(namespace, str(uuid.uuid4()), {"data": mem.text})

    return {"messages": [{"role": "assistant", "content": "Noted."}]}

builder = StateGraph(MessagesState)
builder.add_node("chat", chat_creates_memory_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile(store=store)

config = {"configurable": {"user_id": "u1"}}

r1 = graph.invoke({"messages": [{"role": "user", "content": "My name is waleed"}]}, config)
print("Assistant:", r1["messages"][-1].content)

r2 = graph.invoke({"messages": [{"role": "user", "content": "I like Gaming."}]}, config)
print("\nAssistant:", r2["messages"][-1].content)

for it in store.search(("user", "u1", "details")):
    print(it.value['data'])