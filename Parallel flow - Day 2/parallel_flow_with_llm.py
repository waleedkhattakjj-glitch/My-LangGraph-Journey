# parallel_flow_with_llm
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


from typing import TypedDict
class essaystate(TypedDict) :
    essay_text : str
    cot_feedback : str
    doa_feedback : str
    language : str
    final_summary : str


# cot function
def cot_func( state = essaystate ) :
    essay_text = state['essay_text']
    
    prompt1 = f""" 
    You are an expert essay evaluator.

Your task is to evaluate the essay based on Content and Critical Thinking (COT).

Evaluate:
- Quality of ideas
- Depth of explanation
- Relevance to topic
- Critical thinking
- Clarity of arguments

Give:
1. A short constructive feedback (3-5 lines)
2. A score from 1 to 10

IMPORTANT:
- Be fair and professional
- Do not give very long feedback
- Output must follow this exact format

Output Format:

Feedback: <your feedback>

Score: <number>/10

Essay:
{essay_text}
    """
    cot_feedback = model.invoke(prompt1).content
    return { 'cot_feedback' : cot_feedback}


# doa function
def doa_func ( state = essaystate ):
    essay_text = state['essay_text']
    
    prompt2 = f"""
    You are an expert essay evaluator.

Your task is to evaluate the essay based on DOA (Delivery, Organization, and Analysis).

Evaluate:
- Structure of essay
- Paragraph organization
- Flow between ideas
- Clarity of presentation
- Logical arrangement

Give:
1. A short constructive feedback (3-5 lines)
2. A score from 1 to 10

IMPORTANT:
- Be fair and professional
- Keep feedback concise
- Output must follow this exact format

Output Format:

Feedback: <your feedback>

Score: <number>/10

Essay:
{essay_text}
    """
    doa_feedback = model.invoke(prompt2).content
    return {'doa_feedback' : doa_feedback}


# language function
def language_func ( state = essaystate):
    essay_text = state['essay_text']
    
    prompt3 = f"""
    You are an expert English language evaluator.

Your task is to evaluate the essay based on language quality.

Evaluate:
- Grammar
- Vocabulary
- Sentence structure
- Spelling
- Readability

Give:
1. A short constructive feedback (3-5 lines)
2. A score from 1 to 10

IMPORTANT:
- Be fair and professional
- Keep feedback concise
- Output must follow this exact format

Output Format:

Feedback: <your feedback>

Score: <number>/10

Essay:
{essay_text}
    """
    language = model.invoke(prompt3).content
    return { 'language' : language }


def summary_func ( state = essaystate):
    cot_text = cot_func()
    doa_text = doa_func()
    language = language_func
    
    final_prompt = f"""You are a final essay assessment expert.

You will receive:
- COT feedback and score
- DOA feedback and score
- Language feedback and score

Your task:
1. Analyze all evaluations
2. Write a final overall feedback summary
3. Calculate the average final score
4. Give the final score out of 10

IMPORTANT:
- Keep the final summary concise and professional
- Mention both strengths and weaknesses
- Do not repeat all evaluator feedback exactly

Output Format:

Final Feedback:
<overall summary>

Final Score:
<average score>/10

COT Evaluation:
{cot_text}

DOA Evaluation:
{doa_text}

Language Evaluation:
{language}"""
    final_summary = model.invoke(final_prompt).content
    return {'final_summary' : final_summary}


from langgraph.graph import StateGraph
graph = StateGraph(essaystate)


graph.add_node('cot_node' , cot_func)
graph.add_node('doa_node' , doa_func)
graph.add_node('langauge_node' , language_func)
graph.add_node('summary_node' , summary_func)


from langgraph.graph import START , END
graph.add_edge(START , 'cot_node')
graph.add_edge(START , 'doa_node')
graph.add_edge(START , 'langauge_node')

graph.add_edge('cot_node' , 'summary_node')
graph.add_edge('doa_node' ,'summary_node' )
graph.add_edge('langauge_node' , 'summary_node')

graph.add_edge('summary_node' , END)


workflow = graph.compile()
workflow


s_essay = """The Impact of Artificial Intelligence on Education

Artificial Intelligence (AI) is rapidly transforming the education sector across the world. It is changing the way students learn, teachers teach, and educational institutions operate. AI-powered tools are making learning more personalized, efficient, and accessible.

One of the major benefits of AI in education is personalized learning. Every student learns at a different pace, and AI systems can adapt lessons according to individual needs. For example, intelligent tutoring systems can identify weak areas of a student and provide targeted practice to improve understanding.

Another important impact is automation of administrative tasks. Teachers often spend a lot of time grading assignments and managing records. AI can help automate these tasks, allowing teachers to focus more on teaching and mentoring students.

AI also improves accessibility in education. Students from remote areas can access online learning platforms powered by AI. Features like speech recognition and translation help students with disabilities or language barriers learn more effectively.

However, there are also challenges. Over-reliance on AI may reduce human interaction in learning. There are also concerns about data privacy and the ethical use of student information. Therefore, it is important to use AI responsibly in education.

In conclusion, AI has the potential to revolutionize education by making it more personalized, efficient, and inclusive. At the same time, careful implementation is necessary to ensure that it benefits all learners equally."""
final_ans = workflow.invoke({
    'essay_text' : s_essay
})


print(final_ans)


print(final_ans['cot_feedback'])


print(final_ans['doa_feedback'])


print(final_ans['language'])


print(final_ans['final_summary'])