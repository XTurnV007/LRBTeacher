# LRBTeacher 国际化支持 / Internationalization Support

## 概述 / Overview

LRBTeacher 现在支持中英文双语界面，用户可以在应用中随时切换语言。

LRBTeacher now supports bilingual interface in Chinese and English, users can switch languages anytime in the application.

## 功能特性 / Features

### 🌐 多语言支持 / Multi-language Support
- **中文（默认）**: 完整的中文界面支持
- **English**: Full English interface support
- **实时切换**: 无需重启应用即可切换语言
- **Real-time switching**: Switch languages without restarting the app

### 📱 界面元素国际化 / UI Elements Internationalization
- 主界面标题和导航
- 教学方法名称和描述
- 按钮和表单标签
- 错误消息和提示信息
- 版权信息

## 使用方法 / Usage

### 1. 语言切换 / Language Switching

在侧边栏底部找到语言选择器：
Find the language selector at the bottom of the sidebar:

```
语言 / Language
├── 中文 (默认)
└── English
```

### 2. 开发者使用 / Developer Usage

#### 添加新的翻译文本 / Adding New Translation Text

在 `utils/i18n.py` 文件中的 `TRANSLATIONS` 字典中添加新的键值对：

```python
TRANSLATIONS = {
    'zh': {
        'new_key': '中文文本',
        # ... 其他翻译
    },
    'en': {
        'new_key': 'English Text',
        # ... other translations
    }
}
```

#### 在代码中使用翻译 / Using Translations in Code

```python
from utils.i18n import t

# 简单翻译
st.title(t('app_title'))

# 带参数的翻译
st.write(t('question_number', 1))  # 问题 1 / Question 1
```

#### 初始化国际化 / Initialize Internationalization

在每个应用文件的开头：

```python
from utils.i18n import init_i18n, t, language_selector

def main():
    # 初始化国际化
    init_i18n()
    
    # 显示语言选择器（可选）
    language_selector()
    
    # 使用翻译
    st.title(t('app_title'))
```

## 文件结构 / File Structure

```
├── utils/
│   └── i18n.py                 # 国际化核心模块
├── main.py                     # 主应用（已更新）
├── know_app.py                 # 知识图谱应用（已更新）
├── quiz_app.py                 # 测验应用（已更新）
├── methods/
│   ├── simulate_teaching.py    # 模拟教学（已更新）
│   ├── interactive_teaching.py # 互动教学（已更新）
│   └── exercise_teaching.py    # 练习教学（已更新）
├── demo_i18n.py               # 国际化演示
└── README_I18N.md             # 本文档
```

## 演示 / Demo

运行国际化演示：
Run the internationalization demo:

```bash
streamlit run demo_i18n.py
```

## 支持的应用 / Supported Applications

✅ **主应用 (main.py)**: 完整的中英文支持
✅ **知识图谱生成器 (know_app.py)**: 界面元素国际化
✅ **测验应用 (quiz_app.py)**: 界面元素国际化
✅ **模拟教学方法**: 完整的界面国际化
✅ **互动式教学方法**: 完整的界面国际化
✅ **练习式教学方法**: 完整的界面国际化

## 技术实现 / Technical Implementation

### 核心组件 / Core Components

1. **翻译函数 `t()`**: 根据当前语言返回对应文本
2. **语言管理**: 使用 Streamlit session state 管理当前语言
3. **语言选择器**: 侧边栏组件，支持实时切换
4. **初始化函数**: 确保国际化系统正确初始化

### 特性 / Features

- **会话持久化**: 语言选择在会话期间保持
- **实时切换**: 切换语言后立即生效
- **格式化支持**: 支持带参数的文本格式化
- **回退机制**: 如果翻译不存在，显示原始键名

## 扩展指南 / Extension Guide

### 添加新语言 / Adding New Languages

1. 在 `TRANSLATIONS` 字典中添加新的语言代码
2. 提供完整的翻译文本
3. 更新语言选择器选项

```python
TRANSLATIONS = {
    'zh': { ... },
    'en': { ... },
    'ja': {  # 日语示例
        'app_title': 'LRBTeacher',
        'start': '開始',
        # ... 其他翻译
    }
}
```

### 最佳实践 / Best Practices

1. **一致性**: 保持翻译键名的一致性
2. **简洁性**: 使用简短、描述性的键名
3. **完整性**: 确保所有语言都有对应的翻译
4. **测试**: 在不同语言下测试界面布局

## 故障排除 / Troubleshooting

### 常见问题 / Common Issues

1. **翻译不显示**: 检查键名是否正确
2. **语言不切换**: 确保调用了 `init_i18n()`
3. **格式化错误**: 检查参数数量和类型

### 调试技巧 / Debugging Tips

```python
# 检查当前语言
from utils.i18n import get_language
print(f"Current language: {get_language()}")

# 检查翻译是否存在
from utils.i18n import TRANSLATIONS
print(TRANSLATIONS.get('zh', {}).get('your_key', 'Not found'))
```

## 贡献 / Contributing

欢迎为国际化功能贡献翻译和改进！
Contributions to internationalization features and translations are welcome!

1. Fork 项目
2. 添加或改进翻译
3. 测试功能
4. 提交 Pull Request

---

**注意**: 本功能为 LRBTeacher v2.0 的新特性，确保使用最新版本以获得完整的国际化支持。

**Note**: This feature is new in LRBTeacher v2.0, make sure to use the latest version for full internationalization support.