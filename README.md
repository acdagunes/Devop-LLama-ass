# AI DevOps Agent

An intelligent DevOps automation agent powered by LlamaIndex and ChromaDB, capable of understanding and executing DevOps tasks through natural language interactions.

## 🚀 Features

- **AI-Powered Automation**: Natural language interface for DevOps tasks
- **Intelligent Document Processing**: RAG (Retrieval-Augmented Generation) using LlamaIndex
- **Vector Database**: ChromaDB for efficient document storage and retrieval
- **Multi-LLM Support**: Integration with OpenAI and Google Gemini models
- **DevOps Expertise**: Specialized in infrastructure automation and management

## 🛠️ Tech Stack

### Core Framework
- **Python 3.13**
- **LlamaIndex 0.14.8** - Data framework for LLM applications
- **ChromaDB 1.3.5** - Vector database for embeddings storage

### AI/ML Models
- **OpenAI** - GPT models integration
- **Google Gemini** - Gemini AI models
- **LlamaCloud Services** - Cloud-based AI services
- **HuggingFace** - Model hosting and inference

### Data Processing
- **Pandas 2.2.3** - Data manipulation and analysis
- **NumPy 2.3.5** - Numerical computing
- **BeautifulSoup4** - HTML/XML parsing
- **PyPDF** - PDF document processing

### DevOps & Automation
- **Kubernetes Client** - Kubernetes cluster management
- **ONNX Runtime** - ML model inference optimization
- **SQLAlchemy** - Database toolkit

### Web & API
- **Uvicorn** - ASGI web server
- **HTTPX/AIOHTTP** - Async HTTP clients
- **Pydantic** - Data validation

### Utilities
- **python-dotenv** - Environment variable management
- **NLTK** - Natural language processing
- **Tiktoken** - OpenAI tokenization
- **Rich** - Terminal formatting

## 📋 Prerequisites

- Python 3.13+
- Virtual environment tool
- OpenAI API key (optional)
- Google Gemini API key (optional)

## 🔧 Installation

1. **Clone the repository**
\\\ash
git clone https://github.com/acdagunes/ai-devops-agent.git
cd ai-devops-agent
\\\

2. **Create virtual environment**
\\\ash
python -m venv ai_env
ai_env\Scripts\activate  # Windows
# source ai_env/bin/activate  # Linux/Mac
\\\

3. **Install dependencies**
\\\ash
pip install -r requirements.txt
\\\

4. **Configure environment variables**
\\\ash
# Create .env file
cp .env.example .env
# Add your API keys
\\\

## 🚦 Usage

\\\python
# Example usage
python agent.py
\\\

## 📁 Project Structure

\\\
python/
├── ai_env/              # Virtual environment
├── chroma_db/           # ChromaDB storage (gitignored)
├── devops_files/        # DevOps documentation and files
├── agent.py             # Main agent script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (gitignored)
└── README.md           # This file
\\\

## 🔐 Environment Variables

Create a \.env\ file in the root directory:

\\\env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here
# Add other configuration as needed
\\\

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Nikoloz Acdagunes**
- GitHub: [@acdagunes](https://github.com/acdagunes)

## 🙏 Acknowledgments

- LlamaIndex team for the amazing framework
- ChromaDB for the vector database
- OpenAI and Google for AI model APIs

---

**Note**: This is an AI-powered automation tool. Use responsibly and ensure proper security measures when handling sensitive infrastructure.
