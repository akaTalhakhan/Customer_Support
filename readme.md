# 🤖 AI Support Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/joaomdmoura/crewAI)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform any website into an intelligent support assistant powered by AI agents**

A sophisticated Streamlit web application that leverages [CrewAI](https://github.com/joaomdmoura/crewAI) multi-agent framework to provide accurate, context-aware support responses by intelligently scraping and analyzing website content.

## ✨ Key Features

### 🧠 **Dual-Agent Intelligence**
- **Support Agent**: Analyzes website content and crafts detailed responses
- **QA Reviewer**: Ensures accuracy and quality of all answers
- **Memory System**: Maintains conversation context for better interactions

### 🌐 **Smart Content Processing**
- **Real-time Website Scraping**: Extract content from any public website
- **Intelligent Text Processing**: Clean and structure scraped content for optimal AI analysis
- **Multi-format Support**: Handle various website structures and content types

### 💬 **Modern Chat Experience**
- **Intuitive Interface**: Clean, responsive chat UI with message history
- **Real-time Progress**: Visual feedback showing agent workflow steps
- **Conversation Memory**: Maintains context across multiple questions
- **Error Handling**: Graceful error management with helpful feedback

### 🎨 **Professional Design**
- **Custom Styling**: Modern gradient themes and smooth animations
- **Responsive Layout**: Optimized for desktop and mobile devices
- **Status Indicators**: Visual connection status for API and website
- **Progress Tracking**: Expandable step-by-step agent activity viewer

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/akaTalhakhan/Customer_Support.git
   cd Customer_Support
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`
   - Enter your OpenAI API key in the sidebar
   - Provide a website URL to analyze
   - Start asking questions!

## 📋 Usage Guide

### Step 1: Configuration
- **API Key**: Enter your OpenAI API key in the sidebar (securely handled, not stored)
- **Website URL**: Provide the website you want the assistant to learn from

### Step 2: Interaction
- **Ask Questions**: Type support questions in the chat interface
- **View Progress**: Expand the progress tracker to see agent workflow
- **Continue Conversation**: The assistant remembers context from previous messages

### Step 3: Management
- **Clear History**: Use the sidebar button to reset conversation
- **Change Website**: Update the URL to switch knowledge sources

## 🛠️ Technical Architecture

### Core Components
```
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

### Key Dependencies
- **streamlit**: Web application framework
- **crewai**: Multi-agent AI framework
- **beautifulsoup4**: HTML parsing and content extraction
- **requests**: HTTP client for website scraping
- **langchain**: LLM integration and tooling
- **chromadb**: Vector database for embeddings

### Agent Workflow
1. **Content Extraction**: Scrape and clean website content
2. **Context Building**: Combine website data with conversation history
3. **Support Analysis**: Primary agent generates response using website knowledge
4. **Quality Review**: Secondary agent validates and improves the response
5. **Response Delivery**: Final answer presented to user with progress tracking

## 🔧 Configuration Options

### Environment Variables
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_NAME=gpt-3.5-turbo  # Default model
```

### Customization
- **Model Selection**: Modify `OPENAI_MODEL_NAME` for different GPT models
- **Temperature Settings**: Adjust creativity vs accuracy in agent configurations
- **UI Styling**: Customize CSS in the main application file

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with debug mode
streamlit run main.py --logger.level=debug
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent AI framework
- [Streamlit](https://streamlit.io/) - Web application framework
- [OpenAI](https://openai.com/) - Language model API

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/akaTalhakhan/Customer_Support/issues)
- **Discussions**: [GitHub Discussions](https://github.com/akaTalhakhan/Customer_Support/discussions)
- **Email**: [Contact Developer](mailto:your-email@example.com)

---

<div align="center">
  <strong>Made with ❤️ using Streamlit & CrewAI</strong>
  <br>
  <sub>Transform websites into intelligent support assistants</sub>
</div>