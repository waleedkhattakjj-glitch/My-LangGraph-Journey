# LLM (model)
# pip install langchain-groq
# pip install python-dotenv
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=1.5,
)

p = "what is the capital of pakistan"
r = model.invoke(p)
print(r.content)


from pydantic import BaseModel,Field
from typing import Literal
class sentimentscheema(BaseModel):
    reviews : Literal[ 'positive' , 'negative'] = Field(description =" sentiment of the feedback" )  
structureoutput_model = model.with_structured_output(sentimentscheema)


from typing import TypedDict
class sentiment_state(TypedDict):
    review : str
    result : str
    positive_response : str
    negative_response : str


def sentiment_check(state : sentiment_state):
    review = state['review']
    prompt1 = f' find the sentiment of following review /n {review}'
    result = structureoutput_model.invoke(prompt1).reviews
    state['result'] = result
    return state


def positive_func( state : sentiment_state):
    result = state['result']
    prompt2 = f'write a warm thank you message in response to this review /n/n {state['review']} '
    response = model.invoke(prompt2).content
    state['positive_response'] = response
    return state


def negative_func(state : sentiment_state):
    result = state['result']
    prompt3 = f'write a appology message in response to this review /n/n {state['review']}'
    result = model.invoke(prompt3).content
    state['negative_response'] = result
    return state


from langgraph.graph import StateGraph
graph = StateGraph(sentiment_state)


from typing import Literal
def conditional_func( state : sentiment_state ) -> Literal[ 'positive_node' , 'negative_node' ] :
    if state['result'] == 'positive':
        return 'positive_node'
    else :
        return 'negative_node'


graph.add_node('sentiment_check_node' , sentiment_check)
graph.add_node( 'positive_node' , positive_func)
graph.add_node( 'negative_node' , negative_func)


from langgraph.graph import START , END
graph.add_edge(START , 'sentiment_check_node')
graph.add_conditional_edges('sentiment_check_node' , conditional_func)
graph.add_edge('positive_node',END)
graph.add_edge('negative_node' , END)


workflow = graph.compile()


feedback= {'review' :"The workflow structure is confusing and difficult to follow."}
result = workflow.invoke(feedback)
print(result)


print("\nReview:")
print(result["review"])

print("\nResult:")
print(result["result"])

print("\nNegative Response:")
print(result["negative_response"])