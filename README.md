# Bakadream 的小助手

这是一个基于 Python 的命令行 AI 助手示例项目，通过 OpenAI 兼容的 Chat Completions 接口调用大语言模型。

项目启动时会读取 `.env` 中的模型服务配置，显示当前应用、接口地址和模型信息，然后发送一条示例消息并打印模型回复。

## 项目结构

```text
.
├── assistant/
│   ├── __init__.py
│   └── config.py              # 配置读取与校验
├── tools/
│   └── check_provider.py      # 模型供应商能力检查脚本
├── .env.example               # 环境变量模板
├── main.py                    # 命令行入口
└── requirements.txt           # Python 依赖
```

## 环境要求

- Python 3.12 或更高版本
- 一个支持 OpenAI 兼容接口的模型服务或网关
- 模型服务的 API Key、Base URL 和模型名称

## 安装依赖

在项目根目录执行以下命令。

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果 PowerShell 阻止虚拟环境脚本运行，可以改用当前用户范围的执行策略：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然后重新执行激活命令。

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 配置 `.env`

复制环境变量模板：

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

打开项目根目录下的 `.env`，填写模型服务配置：

```dotenv
# OpenAI 兼容模型服务地址，必须使用 https://或http://
# 通常以 /v1 结尾，且不要带末尾斜杠
LLM_BASE_URL=https://your-gateway.example/v1

# 模型服务 API Key
LLM_API_KEY=sk-your-key-here

# 要调用的模型名称
LLM_MODEL=your-model-name
```

必填配置如下：

| 变量 | 说明 |
| --- | --- |
| `LLM_BASE_URL` | OpenAI 兼容接口的 Base URL，必须以 `https://`或`http://` 开头；通常以 `/v1` 结尾 |
| `LLM_API_KEY` | 模型服务 API Key，请勿提交到 Git |
| `LLM_MODEL` | 模型服务支持的模型名称 |

代码还支持以下可选配置：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `LLM_TEMPERATURE` | `0.0` | 模型温度配置 |
| `LLM_TIMEOUT` | `60.0` | API 请求超时时间，单位为秒 |
| `APP_NAME` | `Bakadream的小助手` | 启动时显示的应用名称 |
| `DATA_DIR` | `data` | 数据目录 |
| `WORKSPACE_DIR` | `sandbox` | 工作区目录 |

`.env` 已被加入 `.gitignore`，请不要把真实 API Key 提交到版本库。

## 运行

确认已激活虚拟环境，并且已在 `.env` 中填写必填配置后，在项目根目录执行：

```powershell
python main.py
```

macOS / Linux 也可以使用：

```bash
python3 main.py
```

启动成功后，程序会显示模型服务信息，并请求模型回答示例问题。程序当前的示例请求会要求模型用文言文回答。

## 检查模型供应商

`tools/check_provider.py` 提供了基础的供应商检查入口。目前默认会打印已加载的 Base URL、模型名称和脱敏后的 API Key：

```powershell
python tools/check_provider.py
```

脚本中还提供了两项可选测试函数：

- `test_tool_call()`：测试模型是否支持函数工具调用（Tool Calling）
- `test_stream()`：测试流式输出（Streaming）

如需运行这两项测试，请编辑 `tools/check_provider.py`，取消对应函数调用前的注释，再执行上面的命令。

## 常见问题

### 启动时报 `LLM_API_KEY 未配置`

请确认项目根目录存在 `.env`，并且其中的 `LLM_API_KEY` 已填写。可以重新执行：

```powershell
Copy-Item .env.example .env
```

### 启动时报 `LLM_BASE_URL 格式错误`

`LLM_BASE_URL` 必须以 `https://`或`http://` 开头，例如：

```dotenv
LLM_BASE_URL=https://api.example.com/v1
```


### 找不到模块，例如 `No module named 'openai'`

请确认虚拟环境已激活，然后重新安装依赖：

```powershell
python -m pip install -r requirements.txt
```

### 请求失败或模型不存在

请检查以下内容：

1. `LLM_BASE_URL` 是否为服务商提供的 OpenAI 兼容接口地址。
2. `LLM_API_KEY` 是否有效且有调用权限。
3. `LLM_MODEL` 是否与服务商支持的模型名称完全一致。
4. 当前网络是否可以访问模型服务地址。
