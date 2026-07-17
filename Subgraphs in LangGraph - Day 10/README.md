Subgraphs in LangGraph - Day 10
Learning  Subgraphs in LangGraph

📌 Overview
Today I learned about Subgraphs in LangGraph - a powerful pattern for building modular, reusable workflows. I implemented two different approaches to create subgraphs and integrate them into parent graphs.

What are Subgraphs?
Subgraphs are self-contained LangGraph workflows that can be nested inside larger graphs. They promote code reusability, maintainability, and clean separation of concerns.

✨ Two Types OF SubGraph In LangGraph
Method 1: Direct Subgraph Integration
In this approach, the subgraph is compiled separately and then added as a node to the parent graph.

How it works:

Define subgraph state

Build and compile subgraph

Add subgraph as a node in parent graph

Parent graph invokes subgraph like any other node

Example: English → Urdu translation subgraph

Method 2: Functional Subgraph
In this approach, the subgraph is called as a function within a parent node.

How it works:

Define subgraph state

Build and compile subgraph

In parent node function, call childgraph.invoke()

Pass state between graphs

Example: Question answering → Translation pipeline

🛠️ Tech Stack
LangGraph - Graph-based workflow orchestration

Google Gemini - LLM provider

Python 3.13+
