# Project Files

## parallel_flow.py
This file contains a cricket statistics calculator that:
- Takes inputs: runs, balls, fours, sixes
- Calculates strike rate, boundary percentage, and balls per boundary
- Uses LangGraph parallel flow to process calculations simultaneously
- Returns a summary of all three metrics

## parallel_flow_with_llm.py
This file contains an AI-powered essay evaluation system that:
- Uses Groq LLM (openai/gpt-oss-120b model)
- Evaluates essays on three criteria:
  - COT (Content and Critical Thinking)
  - DOA (Delivery, Organization, and Analysis)
  - Language Quality (grammar, vocabulary, sentence structure)
- Provides feedback and scores (1-10) for each criterion
- Generates a final summary with overall assessment
- Uses LangGraph parallel flow for simultaneous evaluations
