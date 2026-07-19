Short-Term Memory in LangGraph - Day 11
Implementing Memory and Context Management in LangGraph

📌 Overview
Today I learned about Short-Term Memory (STM) in LangGraph - two different approaches to maintain conversation context and manage message history in AI workflows.

What is Short-Term Memory?
Short-term memory in LangGraph allows the system to remember previous interactions within a conversation session. This enables contextual responses and coherent multi-turn conversations.

✨ Two Methods Learned
Method 1: CheckPointers
CheckPointers save the entire state of the graph at each step, allowing the workflow to resume from where it left off.

How it works:

Saves complete graph state

Uses thread_id to track different conversation sessions

Perfect for long-running conversations

InMemorySaver for development, SQLite/PostgreSQL for production

Method 2: Trimming
Trimming manages token limits by keeping only the most recent messages.

How it works:

Uses trim_messages function

Keeps only the last N tokens/messages

Prevents context window overflow

Maintains conversation flow within budget

🛠️ Tech Stack
LangGraph - Workflow orchestration

Google Gemini - LLM provider

Python 3.13
🎯 Use Cases
CheckPointers:

Customer support chatbots

Long research conversations

Complex multi-step workflows

Resume interrupted sessions

Trimming:

High-volume chat applications

Cost-sensitive deployments

Simple Q&A systems

API budget constraints
