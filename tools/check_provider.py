from openai import OpenAI
from assistant.config import get_settings

settings = get_settings()

client = OpenAI(
    base_url = settings.llm_base_url,
    api_key = settings.llm_api_key
)
def test_tool_call():
    print("\n===== 🔧 Tool Calling 测试：北京天气怎么样 =====")
    tools = [
        {
            "type":"function",
            "function":{
                "name": "get_weather",
                "description": "获取当前城市天气",
                "parameters": {
                    "type":"object",
                    "required": ["city"],
                    "properties": {
                        "city": {"type": "string","descriptions": "城市名称"}
                    }
                }
            }
        }
    ]

    resp = client.chat.completions.create(
        model = settings.llm_model,
        messages=[{"role":"user","content":"北京今天天气怎么样"}],
        tools = tools,
        tool_choice= "auto",
        temperature= 0.0,
        stream= False
    )
    choice = resp.choices[0]
    msg = choice.message
    print(f"message.content:{msg.content}")
    print(f"tool_calls原始值:{msg.tool_calls}")
    if msg.tool_calls:
        tc = msg.tool_calls[0]
        print(f"检测到tool_calls")
        print(f"函数名：{tc.function.name}")
        print(f"参数JSON字符串:{tc.function.arguments}")

        assert tc.function.name == "get_weather",f"期望get_weather实际{tc.function.name}"
        import json
        args = json.loads(tc.function.arguments)
        assert "city" in args,"参数缺少city"
        assert args["city"] == "北京",f"期望北京实际{args["city"]}"
        print("tool_call 校验全部通过")
    else:
        print("没有返回 tool_calls,模型没有触发工具调用")
def test_stream():
    print("\n===== 📡 Stream 流式测试：数到5 =====")
    stream = client.chat.completions.create(
        model = settings.llm_model,
        messages = [{"role":"user","content":"数到5只输出1 2 3 4 5"}],
        temperature= 0.0,
        stream=True
    )
    full_text = ""
    for chunk in stream:
        print(chunk.choices[0].delta.content)
if __name__== "__main__":
    # test_tool_call()
    # test_stream()
    print(repr(settings.llm_base_url), repr(settings.llm_model), settings.masked_api_key, len(settings.llm_api_key))