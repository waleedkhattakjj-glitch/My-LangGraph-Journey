# Human-in-the-Loop (HITL) in LangGraph - Day 9

**Human-in-the-Loop Workflow with LangGraph**

## 📌 Overview

This project demonstrates a **Human-in-the-Loop (HITL)** workflow using LangGraph. The system generates social media posts using an LLM and then pauses for human approval before finalizing the submission. This pattern is essential for building trustworthy AI systems that require human oversight.

**Key concept:** The workflow pauses (`interrupt`) at the human node, waits for approval/rejection, and resumes based on human input.

## ✨ Features

- **🤖 AI Content Generation**: Uses Google Gemini to create social media posts
- **👤 Human Approval**: Workflow pauses for human review and decision
- **🔄 State Management**: Maintains conversation state with `InMemorySaver`
- **📝 Structured Output**: Posts are 60 words, unique, and tailored to the topic
- **⏯️ Resume/Interrupt**: Uses LangGraph's `interrupt` and `Command` for HITL

## 🛠️ Tech Stack

- **LangGraph** - Workflow orchestration with HITL support
- **Google Gemini** - LLM for content generation
- **LangChain** - Output parsing and message handling
- **Python 3.13+**
