from assistant.config import get_settings
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
settings = get_settings()
settings.require_llm_config()

client = OpenAI(
    base_url = settings.llm_base_url,
    api_key = settings.llm_api_key,
    timeout = settings.llm_timeout
)
console = Console()
text = Text()
text.append(f"🚀 {settings.app_name} 正在启动\n", style="bold bright_cyan")
text.append(f"模型地址: ", style="gray")
text.append(f"{settings.masked_base_url}\n", style="blue")
text.append(f"模型名称: ", style="gray")
text.append(f"{settings.llm_model}\n", style="blue")
text.append(f"API‑Key: ", style="gray")
text.append(settings.masked_api_key, style="yellow")
panel = Panel(
    text,
    title="[red]System Boot[/red]",
    subtitle=f"[red]{settings.app_name}[/red]",
    border_style="bright_green",
    expand=False
)
console.print(panel)
resp = client.chat.completions.create(
    model = settings.llm_model,
    messages = [
        {"role":"user","content":"你好介绍一下你自己"},
        {"role":"system","content":"你只能用文言文回答"}
    ]
)
console.print(f"系统提示词放后面：{resp.choices[0].message.content}")