# LRBTeacher - 小红书内容创作教练

<div align="center">
  <img src="static/LBRTeacher.svg" alt="LRBTeacher Logo" width="200"/>
  
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  
  **一个由大语言模型驱动的智能小红书内容创作教练**
  
  [English](README_EN.md) | 中文
</div>

## 📖 项目简介

LRBTeacher 是一个基于智谱AI GLM模型的智能内容创作助手，专门为小红书内容创作者设计。通过多种教学模式和智能知识库管理，帮助用户提升内容创作技能，生成高质量的小红书笔记。

## ✨ 核心功能

### 🎯 多样化教学模式
- **模拟教学方法**: 基于用户输入生成个性化人设，并创作相应风格的小红书笔记
- **互动式教学方法**: 通过知识点问答和实时反馈提升创作技能
- **练习式教学方法**: 提供实战练习机会，巩固学习成果
- **知识总结式教学方法**: 系统化整理创作知识点
- **评估式教学方法**: 对创作内容进行专业评估和改进建议

### 📚 智能知识库管理
- **文档上传**: 支持PDF、TXT等多种格式文档上传
- **向量化存储**: 使用FAISS进行高效的向量检索
- **智能问答**: 基于知识库内容进行精准问答
- **知识图谱**: 自动生成结构化知识图谱可视化

### 🔍 辅助功能
- **网络搜索**: 集成DuckDuckGo搜索，获取最新信息
- **图像生成**: 支持AI图像生成功能
- **流式响应**: 实时显示AI生成内容
- **配置管理**: 灵活的API配置和参数调整

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Streamlit
- 智谱AI API密钥

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/LRBTeacher.git
cd LRBTeacher
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API密钥**
启动应用后，在侧边栏的"🔑 API密钥管理"面板中设置你的智谱AI API密钥。

注意：为了安全起见，智谱AI API密钥不再在配置文件中硬编码，而是通过应用界面动态配置。Bing搜索功能已内置API密钥。

4. **运行应用**
```bash
streamlit run main.py
```

5. **访问应用**
在浏览器中打开 `http://localhost:8501`

## 📁 项目结构

```
LRBTeacher/
├── main.py                 # 主应用入口
├── know_app.py            # 知识图谱生成应用
├── quiz_app.py            # 测验应用
├── requirements.txt       # 依赖包列表
├── config/               # 配置文件
│   ├── config.py         # 主配置文件
│   └── model_config_example.py
├── methods/              # 教学方法模块
│   ├── simulate_teaching.py      # 模拟教学
│   ├── interactive_teaching.py   # 互动教学
│   ├── exercise_teaching.py      # 练习教学
│   ├── knowledge_summary.py      # 知识总结
│   └── assessment_teaching.py    # 评估教学
├── knowledge_base/       # 知识库管理
│   └── knowledge_base_management.py
├── utils/               # 工具模块
│   ├── api_client.py    # API客户端
│   ├── chat_helpers.py  # 聊天助手
│   ├── stream_handler.py # 流处理
│   └── css_styles.py    # 样式文件
├── internet_search/     # 网络搜索模块
├── static/             # 静态资源
└── docs/               # 文档
```

## 🎮 使用指南

### 教学模式使用

1. **选择教学方法**: 在侧边栏选择适合的教学模式
2. **输入内容**: 根据提示输入相关信息
3. **获取指导**: 系统将提供个性化的创作指导
4. **实践应用**: 根据建议创作内容

### 知识库管理

1. **上传文档**: 点击"知识库管理"上传相关文档
2. **向量化处理**: 系统自动处理并存储文档向量
3. **智能检索**: 通过问答方式检索相关知识
4. **可视化展示**: 查看知识图谱结构

## 🛠️ 技术栈

- **前端框架**: Streamlit
- **AI模型**: 智谱AI GLM-4.5
- **向量数据库**: FAISS
- **文档处理**: PyMuPDF
- **网络搜索**: DuckDuckGo Search
- **图形可视化**: Graphviz, Pyvis

## 📊 API配置

项目支持灵活的API配置，可在 `config/config.py` 中调整：

```python
# 模型配置
DEFAULT_MODEL = "glm-4.5"
IMAGE_MODEL = "cogview-4-250304"

# 模型参数
MODEL_PARAMS = {
    "max_tokens": 4096,
    "temperature": 0.7,
    "stream": True,
}
```

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详情。

### 如何贡献
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [智谱AI](https://www.zhipuai.cn/) - 提供强大的GLM模型支持
- [Streamlit](https://streamlit.io/) - 优秀的Web应用框架
- [FAISS](https://github.com/facebookresearch/faiss) - 高效的向量检索库

## 📞 联系我们

- 项目主页: [GitHub Repository](https://github.com/yourusername/LRBTeacher)
- 问题反馈: [Issues](https://github.com/yourusername/LRBTeacher/issues)
- 邮箱: your.email@example.com

---

<div align="center">
  <p>如果这个项目对你有帮助，请给我们一个 ⭐️</p>
  <p>© 2025 LRBTeacher. All rights reserved. Powered by GLM</p>
</div>