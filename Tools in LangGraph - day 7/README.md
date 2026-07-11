🚀 LangGraph Journey - Tools in LangGraph
A complete implementation of a LangGraph-based AI agent that can perform calculations and search the web using DuckDuckGo. This project demonstrates the power of LangGraph for building stateful, multi-tool AI agents.

✨ Features
🤖 AI-Powered Chat: Powered by Google's Gemini 3.1 Flash Lite model

🧮 Calculator Tool: Perform basic arithmetic operations (add, subtract, multiply, divide)

🔍 Web Search: Real-time search capabilities using DuckDuckGo

🔄 Smart Tool Routing: Automatically decides when to use tools vs. when to respond directly

📊 State Management: Built with LangGraph's stateful graph architecture

🛠️ Tech Stack
LangChain: Framework for building LLM applications

LangGraph: Graph-based agent orchestration

Google Gemini: LLM provider

DuckDuckGo: Web search integration

Python 3.13+

📦 Installation
Clone the repository

bash
git clone https://github.com/yourusername/langgraph-journey.git
cd langgraph-journey
Create and activate virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install langchain-google-genai langchain-community langgraph python-dotenv
Set up environment variables
Create a .env file in the project root:

env
GOOGLE_API_KEY=your_google_api_key_here
🚀 Usage
Run the agent:

python
python tools.py
The agent will process your query and return results. Example query:

text
"What is today's latest news about AI Engineer Role and what is 25 * 6"
📁 Project Structure
text
langgraph-journey/
├── tools.py           # Main application file
├── .env              # Environment variables
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
🔧 How It Works
Model Setup: Initializes Google Gemini model with tool bindings

Tool Definition:

calculatur: Performs basic math operations

search_tool: DuckDuckGo search functionality

Graph Construction:

chat_node: Handles LLM interactions

tools_node: Executes tool calls

Conditional Routing: Automatically routes between chat and tools based on LLM decisions

State Management: Maintains conversation state using TypedDict with message history

🎯 Key Concepts Demonstrated
Tool Binding: Connecting LLM with external tools

State Graphs: Building stateful agent workflows

Conditional Edges: Dynamic routing based on LLM output

Message History: Maintaining conversation context

Tool Execution: Handling tool calls and returning results

📝 Example Output
The agent can handle queries that require:

Mathematical calculations: "What is 25 * 6?" → Returns 150

Web searches: "Latest AI Engineer trends" → Returns search results

Combined queries: Mix of calculations and information retrieval

🤝 Contributing
Feel free to fork this repository and experiment with:

Adding new tools

Customizing the graph structure

Integrating different LLM providers

Adding memory/persistence

📄 License
This project is open source and available under the MIT License.

🙏 Acknowledgments
LangChain & LangGraph communities

Google Gemini team

DuckDuckGo for search capabilities

