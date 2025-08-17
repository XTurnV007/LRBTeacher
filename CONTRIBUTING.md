# 贡献指南 / Contributing Guide

感谢您对 LRBTeacher 项目的关注！我们欢迎所有形式的贡献。

Thank you for your interest in the LRBTeacher project! We welcome all forms of contributions.

## 中文版

### 如何贡献

#### 报告问题
- 在提交问题之前，请先搜索现有的 [Issues](https://github.com/yourusername/LRBTeacher/issues)
- 使用清晰、描述性的标题
- 提供详细的问题描述，包括：
  - 操作系统和Python版本
  - 错误信息和堆栈跟踪
  - 重现步骤
  - 预期行为和实际行为

#### 提交功能请求
- 描述您希望添加的功能
- 解释为什么这个功能对项目有用
- 如果可能，提供实现思路

#### 代码贡献

1. **Fork 项目**
   ```bash
   git clone https://github.com/yourusername/LRBTeacher.git
   cd LRBTeacher
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **设置开发环境**
   ```bash
   pip install -r requirements.txt
   ```

4. **进行更改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 确保代码通过测试

5. **提交更改**
   ```bash
   git add .
   git commit -m "Add: 简洁描述您的更改"
   ```

6. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 提供清晰的PR标题和描述
   - 链接相关的Issues
   - 描述您的更改内容

### 代码规范

- 使用Python PEP 8编码规范
- 函数和类需要添加文档字符串
- 变量和函数名使用有意义的命名
- 保持代码简洁和可读性

### 提交信息规范

使用以下格式：
- `Add: 新增功能`
- `Fix: 修复问题`
- `Update: 更新功能`
- `Docs: 文档更新`
- `Style: 代码格式调整`
- `Refactor: 代码重构`

---

## English Version

### How to Contribute

#### Reporting Issues
- Search existing [Issues](https://github.com/yourusername/LRBTeacher/issues) before submitting
- Use clear, descriptive titles
- Provide detailed issue description including:
  - Operating system and Python version
  - Error messages and stack traces
  - Steps to reproduce
  - Expected vs actual behavior

#### Feature Requests
- Describe the feature you'd like to add
- Explain why this feature would be useful
- Provide implementation ideas if possible

#### Code Contributions

1. **Fork the Project**
   ```bash
   git clone https://github.com/yourusername/LRBTeacher.git
   cd LRBTeacher
   ```

2. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Setup Development Environment**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make Changes**
   - Follow existing code style
   - Add necessary comments
   - Ensure code passes tests

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

6. **Push Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Provide clear PR title and description
   - Link related Issues
   - Describe your changes

### Code Standards

- Follow Python PEP 8 coding standards
- Add docstrings to functions and classes
- Use meaningful variable and function names
- Keep code clean and readable

### Commit Message Format

Use the following format:
- `Add: new feature`
- `Fix: bug fix`
- `Update: feature update`
- `Docs: documentation update`
- `Style: code formatting`
- `Refactor: code refactoring`

## 开发环境设置 / Development Setup

### 依赖安装 / Install Dependencies
```bash
pip install -r requirements.txt
```

### 配置API密钥 / Configure API Keys
启动应用后，在侧边栏的"🔑 API密钥管理"面板中设置智谱AI API密钥 / After starting the app, set Zhipu AI API key in the "🔑 API Key Management" panel in the sidebar.

注意：智谱AI API密钥现在通过应用界面动态配置，不再在配置文件中硬编码。Bing搜索已内置API密钥 / Note: Zhipu AI API key is now dynamically configured through the app interface, no longer hardcoded in config files. Bing search has built-in API key.

### 运行测试 / Run Tests
```bash
# 运行应用 / Run application
streamlit run main.py
```

## 联系方式 / Contact

如有任何问题，请通过以下方式联系我们：
For any questions, please contact us via:

- GitHub Issues: [Issues页面 / Issues Page](https://github.com/yourusername/LRBTeacher/issues)
- Email: your.email@example.com

感谢您的贡献！/ Thank you for your contributions!