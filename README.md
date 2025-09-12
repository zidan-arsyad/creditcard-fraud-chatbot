# 💳 Credit Card Fraud Detection Chatbot

A **Streamlit-based conversational AI assistant** for analyzing credit card fraud data and documentation.  
Uses **LLM agents**, **SQL**, and **vector search** to answer queries interactively.

## 🌟 Features

- 🗨️ Chat UI with Streamlit
- 🧠 Groq Llama 4 LLM (configurable)
- 🛠 Multi-tool agent system (SQL + Document)
- 📊 SQLite3 database integration
- 📚 Document Q&A via FAISS vector store
- 🔎 Monitoring with LangSmith
- ⚡ Two modes: **Simple** (1 agent) & **Advanced** (multi-agent)

## 🛠 Technical Stack

| Component      | Tool / Library |
|---------------|----------------|
| **Frontend**  | Streamlit |
| **LLM**       | Groq Llama 4 |
| **Database**  | SQLite3 |
| **Vector DB** | FAISS |
| **Embeddings**| Hugging Face |
| **Framework** | LangChain |
| **Monitoring**| LangSmith |

## 📁 Project Structure

```
src/
├── data/                    # Data storage and processing
│   ├── documents/           # PDF documentation
│   ├── processed/           # Processed data files
│   └── raw/                 # Raw CSV datasets
├── scripts/
│   ├── agents/              # Agent implementations
│   ├── inputs/              # Prompt templates
│   ├── tools/               # Tool definitions
│   └── utils/               # Utility functions
│── start_simple.py          # Main application entry point
└── start_adv.py             # Multi-agent entry point
```

## 🧰 Preparation

Before running the project, download the required datasets:

1. Go to [Kaggle Fraud Detection Dataset](https://www.kaggle.com/datasets/kartik2112/fraud-detection/data?select=fraud%20dataset)
2. Download **fraudTrain.csv** and **fraudTest.csv**
3. Place them inside:
   
```
src/data/raw/
```

Your project structure should look like:

```
src/data/raw/
├── fraudTrain.csv
└── fraudTest.csv
```

4. Follow the steps in `src/data/csv_to_db.ipynb` to convert CSV files into SQLite3 database


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
export GROQ_API_KEY=your_groq_key
export LANGSMITH_API_KEY=your_langsmith_key  # optional
```

4. Run the application:

```bash
# Simple mode
streamlit run src/start_simple.py

# Advanced mode
streamlit run src/start_adv.py # [in construction] wait until this README.md gets updated again
```

## 🧠 Simple vs Advanced Mode

| Mode           | How It Works                                   | Pros                              | Cons                                |
|---------------|-----------------------------------------------|----------------------------------|------------------------------------|
| **Simple**    | Single `MainAgent` with combined prompt + tools | ✅ Easy to deploy<br>✅ Fewer components<br>✅ Fast | ❌ Harder to debug<br>❌ Long prompt |
| **Advanced**  | Preprocessor → Supervisor → SQL & Doc agents    | ✅ Modular<br>✅ Easier to debug<br>✅ Extensible | ❌ More config<br>❌ Slightly slower |

## 📊 Architecture Graphs

| Simple Mode (Placeholder) | Advanced Mode (Placeholder) |
|-------------|---------------|
| ![Simple](https://i.pinimg.com/474x/16/3d/cb/163dcb920d747eb5e11490f8551561b8.jpg) | ![Advanced](https://camo.githubusercontent.com/3396240bff15f09c0c6ab76bc471043812867b5d2ee8fc9588da0f3785b8feef/68747470733a2f2f692e70696e696d672e636f6d2f343734782f64342f63612f64332f64346361643363653832393165393735393633313036643665353966333239362e6a7067) |

## 💡 How It Works (Simple)

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

- "Show me the distribution of fraudulent transactions by amount."
- "What are the main types of credit card fraud according to the EBA report?"
- "Calculate the fraud rate for transactions above $1000."
- "List top 10 highest-risk users in the last 30 days."

## 🙏 Acknowledgments

- Mekari for the opportunity
- Groq for providing the LLM API
- LangChain for the agent framework
- Hugging Face for embeddings
- FAISS for vector similarity search
