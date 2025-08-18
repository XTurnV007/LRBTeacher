# LRBTeacher - Little Red Book Content Creation Coach

<div align="center">
  <img src="static/LBRTeacher.svg" alt="LRBTeacher Logo" width="200"/>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  
  **An AI-powered intelligent content creation coach for Little Red Book (Little Red Book)**
  
  English | [中文](README.md)
</div>

## 📖 Project Overview

LRBTeacher is an intelligent content creation assistant powered by Zhipu AI's GLM model, specifically designed for Little Red Book content creators. Through various teaching modes and intelligent knowledge base management, it helps users improve their content creation skills and generate high-quality Little Red Book posts.

## ✨ Core Features

### 🎯 Diverse Teaching Modes
- **Simulation Teaching**: Generate personalized personas based on user input and create corresponding Little Red Book posts
- **Interactive Teaching**: Improve creation skills through knowledge Q&A and real-time feedback
- **Exercise Teaching**: Provide hands-on practice opportunities to consolidate learning
- **Knowledge Summary Teaching**: Systematically organize creation knowledge points
- **Assessment Teaching**: Professional evaluation and improvement suggestions for created content

### 📚 Intelligent Knowledge Base Management
- **Document Upload**: Support multiple formats including PDF, TXT, etc.
- **Vector Storage**: Efficient vector retrieval using FAISS
- **Smart Q&A**: Precise question-answering based on knowledge base content
- **Knowledge Graph**: Automatically generate structured knowledge graph visualization

### 🔍 Auxiliary Features
- **Web Search**: Integrated DuckDuckGo search for latest information
- **Image Generation**: AI image generation capabilities
- **Streaming Response**: Real-time display of AI-generated content
- **Configuration Management**: Flexible API configuration and parameter adjustment

## 🚀 Quick Start

### Requirements
- Python 3.8+
- Streamlit
- Zhipu AI API Key

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/LRBTeacher.git
cd LRBTeacher
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**
After starting the application, set your Zhipu AI API key in the "🔑 API Key Management" panel in the sidebar.

Note: For security reasons, the Zhipu AI API key is no longer hardcoded in configuration files, but is dynamically configured through the application interface. Bing search functionality has a built-in API key.

4. **Run the Application**
```bash
streamlit run main.py
```

5. **Access the Application**
Open `http://localhost:8501` in your browser

## 📁 Project Structure

```
LRBTeacher/
├── main.py                 # Main application entry
├── know_app.py            # Knowledge graph generation app
├── quiz_app.py            # Quiz application
├── requirements.txt       # Dependencies list
├── config/               # Configuration files
│   ├── config.py         # Main configuration
│   └── model_config_example.py
├── methods/              # Teaching method modules
│   ├── simulate_teaching.py      # Simulation teaching
│   ├── interactive_teaching.py   # Interactive teaching
│   ├── exercise_teaching.py      # Exercise teaching
│   ├── knowledge_summary.py      # Knowledge summary
│   └── assessment_teaching.py    # Assessment teaching
├── knowledge_base/       # Knowledge base management
│   └── knowledge_base_management.py
├── utils/               # Utility modules
│   ├── api_client.py    # API client
│   ├── chat_helpers.py  # Chat helpers
│   ├── stream_handler.py # Stream processing
│   └── css_styles.py    # Style files
├── internet_search/     # Web search module
├── static/             # Static resources
└── docs/               # Documentation
```

## 🎮 Usage Guide

### Teaching Mode Usage

1. **Select Teaching Method**: Choose appropriate teaching mode from sidebar
2. **Input Content**: Enter relevant information as prompted
3. **Get Guidance**: System provides personalized creation guidance
4. **Apply in Practice**: Create content based on suggestions

### Knowledge Base Management

1. **Upload Documents**: Click "Knowledge Base Management" to upload documents
2. **Vector Processing**: System automatically processes and stores document vectors
3. **Smart Retrieval**: Retrieve relevant knowledge through Q&A
4. **Visualization**: View knowledge graph structure

## 🛠️ Tech Stack

- **Frontend Framework**: Streamlit
- **AI Model**: Zhipu AI GLM-4.5
- **Vector Database**: FAISS
- **Document Processing**: PyMuPDF
- **Web Search**: DuckDuckGo Search
- **Graph Visualization**: Graphviz, Pyvis

## 📊 API Configuration

The project supports flexible API configuration in `config/config.py`:

```python
# Model configuration
DEFAULT_MODEL = "glm-4.5"
IMAGE_MODEL = "cogview-4-250304"

# Model parameters
MODEL_PARAMS = {
    "max_tokens": 4096,
    "temperature": 0.7,
    "stream": True,
}
```

## 🤝 Contributing

We welcome all forms of contributions! Please check the [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Zhipu AI](https://www.zhipuai.cn/) - Providing powerful GLM model support
- [Streamlit](https://streamlit.io/) - Excellent web application framework
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient vector retrieval library

## 📞 Contact Us

- Project Homepage: [GitHub Repository](https://github.com/yourusername/LRBTeacher)
- Issue Reports: [Issues](https://github.com/yourusername/LRBTeacher/issues)
- Email: your.email@example.com

---

<div align="center">
  <p>If this project helps you, please give us a ⭐️</p>
  <p>© 2025 LRBTeacher. All rights reserved. Powered by GLM</p>
</div>