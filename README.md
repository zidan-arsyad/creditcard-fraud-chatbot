# Credit Card Fraud Detection Chatbot

A Streamlit-powered conversational AI assistant that helps analyze credit card fraud data and documentation using LLM agents, vector stores, and SQL queries.

## 🌟 Features

- Interactive chat interface built with Streamlit
- Powered by Groq's Llama 4 language model
- Multi-tool agent system for handling different types of queries
- SQL database integration for fraud data analysis
- Document Q&A capabilities using vector similarity search
- Automated tool selection based on user queries

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Language Model**: Groq Llama 4
- **Database**: SQLite3
- **Vector Store**: FAISS
- **Embeddings**: Hugging Face Embeddings
- **Agent Framework**: LangChain

## 📁 Project Structure

```
src/
├── data/                      # Data storage and processing
│   ├── documents/            # PDF documentation
│   ├── processed/           # Processed data files
│   └── raw/                 # Raw CSV datasets
├── scripts/
│   ├── agents/             # Agent implementations
│   ├── inputs/             # Prompt templates
│   ├── tools/              # Tool definitions
│   └── utils/              # Utility functions
└── start_simple.py         # Main application entry point
```

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/creditcard-fraud-chat.git
cd creditcard-fraud-chat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
GROQ_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run src/start_simple.py
```

## 💡 How It Works

1. **User Input Processing**: The system receives natural language queries about credit card fraud.

2. **Agent Routing**: The main agent (`main_agent.py`) analyzes the query and determines the appropriate tool:
   - SQL Tool: For data analysis and statistical queries
   - Document Tool: For questions about fraud documentation and policies

3. **Query Execution**: 
   - SQL queries are executed against the SQLite database
   - Document queries use FAISS vector store for similarity search
   - Results are processed and formatted for user presentation

## 📊 Available Data Sources

- Credit card transaction dataset (fraudTrain.csv, fraudTest.csv)
- EBA/ECB Report on Payment Fraud
- Credit Card Fraud Understanding Documentation

## 🔍 Query Examples

- "Show me the distribution of fraudulent transactions by amount"
- "What are the main types of credit card fraud according to the EBA report?"
- "Calculate the fraud rate for transactions above $1000"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Groq for providing the LLM API
- LangChain for the agent framework
- Hugging Face for embeddings
- FAISS for vector similarity search