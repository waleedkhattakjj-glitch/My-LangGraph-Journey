from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
generator_llm = ChatGroq( model="llama-3.3-70b-versatile" )
evaluator_llm = ChatGroq( model="openai/gpt-oss-120b" )
optimizer_llm = ChatGroq( model='llama-3.3-70b-versatile' )

from typing import TypedDict , Literal
class post_state(TypedDict):
    topic : str
    post : str
    evaluate : Literal['approve' , "rejected"]
    feedback : str
    optimise : str
    runloop : int

from pydantic import BaseModel , Field
from typing import Literal
class checkschema(BaseModel):
    evaluate : Literal['approve' , "rejected"] = Field(description="it is for to check the post weather it is approve or not approve")
    feedback : str = Field(deprecated= 'Short feedback for rejection linkedin post')
structured_model= evaluator_llm.with_structured_output(checkschema)

def topic_func(state : post_state) :
    topic = state['topic']
    prompt1 = f"""
You are a senior LinkedIn content strategist and copywriter. Your task is to write a high engagement and a high quality LinkedIn post about the given topic


Requirements:
- The post must be around 280 words.
- The writing should be professional, engaging, and easy to read.
- Start with a strong hook.
- Maintain a smooth flow.
- Include useful insights or learning.
- Keep the content relevant to the topic.
- Use short paragraphs for better readability.
- Add suitable emojis where appropriate.
- End with a strong conclusion or takeaway.
- Avoid fake claims or misleading information.
- Avoid overly generic AI-generated wording.
- Make the post feel natural and human-written.

Topic:
{topic}

Return ONLY the LinkedIn post.
"""
    result = generator_llm.invoke(prompt1).content
    
    return {'post' : result}

def evaluation_func(state : post_state):
  post = state['post']
  prompt2 =f"""
You are a strict LinkedIn post quality assurance evaluator.

Your ONLY task is to evaluate whether the LinkedIn post meets the required quality standards.

Evaluation Criteria:

1. Clarity
- The post should be easy to understand.
- Sentences should be readable and well-written.

2. Engagement
- The post should have an attention-grabbing hook.
- The content should keep reader interest.

3. Relevance
- The post must stay focused on the topic.

4. Professional Tone
- The tone should be professional and suitable for LinkedIn.

5. Value
- The post should provide useful insights, learning, or information.

6. Originality
- Avoid repetitive or generic AI-generated content.

7. Structure
- The post should contain:
  - Strong opening
  - Proper flow
  - Clear ending or takeaway

8. Length
- The post should be close to 280 words.

Approval Rules:
- Approve only if the post satisfies MOST criteria.
- Reject if the post is unclear, weak, repetitive, poorly structured, or low quality.

IMPORTANT:
- Return ONLY valid structured output.
- evaluation: "approve" or "rejected"
- If the post is rejected, provide clear feedback explaining what needs improvement.
- feedback: Keep feedback short but useful.

Evaluate this LinkedIn post:

{post}
"""
  result = structured_model.invoke(prompt2)
  
  return {'evaluate': result.evaluate ,'feedback': result.feedback }

def output_func(state : post_state):
    post = state['post']
    return print(post)

def optimise_func(state : post_state):
    post = state['post']
    feedback = state['feedback']
    prompt3 = f"""
You are an expert LinkedIn Post Optimizer.

Your task is to improve the rejected LinkedIn post so it can pass the evaluation system.

Optimization Goals:
- Improve clarity and readability
- Improve engagement
- Improve structure and flow
- Improve professionalism
- Improve originality
- Improve the hook and conclusion
- Keep the post around 280 words
- Make the content more natural and human-like

Rules:
- Do NOT change the core topic.
- Do NOT make the content overly long.
- Fix the issues mentioned in the rejection reason.
- Keep the tone professional and engaging.
- Use better formatting and readability.

Rejected Post:
{post}

Rejection Reason:
{feedback}

Return ONLY the improved LinkedIn post.
"""
    result = optimizer_llm.invoke(prompt3).content
    rl = state['runloop'] + 1
    return {'post' : result , 'runloop' : rl}

from langgraph.graph import StateGraph
graph = StateGraph(post_state)

graph.add_node('post_node' , topic_func)
graph.add_node('evaluation_node' , evaluation_func)
graph.add_node('output_node' , output_func)
graph.add_node('optimise_node' , optimise_func)

from typing import Literal
def cond_func(state : post_state) -> Literal['output_node' , 'optimise_node']:
    if state['evaluate'] == 'approve' :
        return 'output_node'
    else :
        return 'optimise_node'

from langgraph.graph import START , END
graph.add_edge(START , 'post_node')
graph.add_edge('post_node' , 'evaluation_node')
graph.add_conditional_edges('evaluation_node' , cond_func)
graph.add_edge('optimise_node' , 'evaluation_node')
graph.add_edge('output_node' , END)

workflow = graph.compile()

result = workflow.invoke({
    'topic': 'loop workflows in LangGraph',
    'runloop': 0
})

print(result['topic'])
print('\n\n')
print(result['post'])
print('\n\n')
print(result['evaluate'])
print('\n\n')
print(result['runloop'])