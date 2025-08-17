"""
国际化完整性测试
验证所有翻译键是否在中英文中都有对应的翻译
"""

from utils.i18n import TRANSLATIONS

def test_translation_completeness():
    """测试翻译完整性"""
    zh_keys = set(TRANSLATIONS['zh'].keys())
    en_keys = set(TRANSLATIONS['en'].keys())
    
    print("🌐 国际化完整性测试")
    print("=" * 50)
    
    # 检查中文缺失的翻译
    missing_in_zh = en_keys - zh_keys
    if missing_in_zh:
        print("❌ 中文翻译中缺失的键:")
        for key in sorted(missing_in_zh):
            print(f"   - {key}")
    else:
        print("✅ 中文翻译完整")
    
    # 检查英文缺失的翻译
    missing_in_en = zh_keys - en_keys
    if missing_in_en:
        print("❌ 英文翻译中缺失的键:")
        for key in sorted(missing_in_en):
            print(f"   - {key}")
    else:
        print("✅ 英文翻译完整")
    
    # 统计信息
    print(f"\n📊 翻译统计:")
    print(f"   中文翻译条目: {len(zh_keys)}")
    print(f"   英文翻译条目: {len(en_keys)}")
    print(f"   总计翻译键: {len(zh_keys | en_keys)}")
    
    # 检查是否完全匹配
    if zh_keys == en_keys:
        print("\n🎉 国际化完整性测试通过！所有翻译键都有对应的中英文翻译。")
        return True
    else:
        print(f"\n⚠️  发现 {len(missing_in_zh) + len(missing_in_en)} 个缺失的翻译")
        return False

def show_translation_categories():
    """显示翻译分类"""
    print("\n📋 翻译分类:")
    print("-" * 30)
    
    categories = {
        "主界面": ["app_title", "app_subtitle", "select_function"],
        "教学方法": ["simulate_teaching", "interactive_teaching", "exercise_teaching", "knowledge_summary", "assessment_teaching"],
        "API管理": ["api_key_management", "zhipu_ai", "save_api_key"],
        "模型配置": ["model_configuration", "select_chat_model", "temperature_randomness"],
        "知识库": ["upload_files", "search_files", "view_knowledge_base"],
        "通用操作": ["start", "send", "save", "cancel", "loading"]
    }
    
    zh_translations = TRANSLATIONS['zh']
    
    for category, keys in categories.items():
        print(f"\n{category}:")
        for key in keys:
            if key in zh_translations:
                print(f"   ✅ {key}: {zh_translations[key]}")
            else:
                print(f"   ❌ {key}: 缺失翻译")

if __name__ == "__main__":
    # 运行完整性测试
    is_complete = test_translation_completeness()
    
    # 显示翻译分类
    show_translation_categories()
    
    if is_complete:
        print("\n🚀 LRBTeacher 国际化系统已完整实现！")
    else:
        print("\n🔧 请修复缺失的翻译后重新测试。")