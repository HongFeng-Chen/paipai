from typing import Dict, Any
import tomllib  # Python 3.11+ 支持 TOML，否则用第三方库

class PromptManager:
    """提示词管理器，支持从文件或字典加载模板"""
    def __init__(self, templates: Dict[str, str] = None, file_path: str = None):
        self.templates = {}
        if file_path:
            self.load_from_file(file_path)
        if templates:
            self.templates.update(templates)

    def load_from_file(self, file_path: str):
        """从 TOML 文件加载模板（也可用 JSON/YAML）"""
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
        self.templates.update(data.get("prompts", {}))

    def render(self, template_name: str, **kwargs) -> str:
        """渲染指定模板，用 kwargs 替换变量"""
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        return template.format(**kwargs)