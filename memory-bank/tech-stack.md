# Tech Stack - Data-Collection-Agent

**最后更新**: 2026-03-19

---

## 1. 技术选型

| 类别 | 技术 | 版本 | 选型理由 |
|:---|:---|:---|:---|
| **运行时** | Python | 3.10+ | HelloAgents 框架要求 |
| **Agent 框架** | HelloAgents | 1.0.0 | 生产级多智能体框架，16 项核心能力 |
| **LLM 调用** | OpenAI SDK | 1.x | 兼容所有 OpenAI 格式接口 |
| **PDF 解析** | PyPDF2 | 3.x | 轻量级、纯 Python 实现 |
| **Word 解析** | python-docx | 1.x | 事实标准、API 简洁 |
| **HTTP 客户端** | httpx | 0.27.x | 同步/异步支持、现代化 API |
| **数据处理** | pandas | 2.x | 数据处理标准库 |
| **Excel 导出** | openpyxl | 3.x | xlsx 格式完整支持 |
| **环境管理** | uv | - | 极速 Python 包管理 |
| **类型检查** | pydantic | 2.x | 数据验证与序列化 |
| **环境变量** | python-dotenv | 1.x | .env 文件加载 |
| **日志** | loguru | 4.x | 简化日志配置 |

---

## 2. 开发环境

### 2.1 uv 环境配置

```bash
# 安装 uv（如未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
cd data-collection-agent
uv sync

# 激活环境
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 添加依赖
uv add hello-agents pypdf2 python-docx httpx pandas openpyxl pydantic python-dotenv loguru

# 锁定依赖
uv lock
```

### 2.2 pyproject.toml 配置

```toml
[project]
name = "data-collection-agent"
version = "0.1.0"
description = "LLM-powered data collection and processing agent"
requires-python = ">=3.10"
dependencies = [
    "hello-agents>=1.0.0",
    "pypdf2>=3.0.0",
    "python-docx>=1.0.0",
    "httpx>=0.27.0",
    "pandas>=2.0.0",
    "openpyxl>=3.0.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "loguru>=0.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
]
```

### 2.3 环境变量 (.env.example)

```bash
# LLM 配置
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=sk-your-api-key

# 可选：备用 LLM
# LLM_BASE_URL_FALLBACK=https://api.openai.com/v1
# LLM_MODEL_ID_FALLBACK=gpt-4o-mini

# 采集配置
COLLECTION_TIMEOUT=30
COLLECTION_MAX_RETRIES=3

# 分块配置
CHUNK_MAX_TOKENS=2000
```

---

## 3. 构建与部署

### 3.1 开发模式

```bash
# 同步依赖
uv sync

# 运行测试
uv run pytest tests/

# 类型检查
uv run mypy src/

# 代码格式化
uv run ruff format src/
```

### 3.2 生产部署

```bash
# 构建
uv build

# 安装
uv pip install dist/data_collection_agent-*.whl

# 或直接安装
uv pip install -e .
```

---

## 4. 依赖关系图

```
┌─────────────────────────────────────────────────────────────┐
│                    Data-Collection-Agent                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │  Intent     │────▶│   Task      │────▶│  Executor   │  │
│  │  Parser     │     │   Planner   │     │             │  │
│  └─────────────┘     └─────────────┘     └─────────────┘  │
│         │                                       │           │
│         ▼                                       ▼           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    Tools Layer                        │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │Collector │  │  Parser  │  │ Exporter │          │   │
│  │  │  (httpx) │  │ (PyPDF2) │  │ (pandas) │          │   │
│  │  └──────────┘  └──────────┘  └──────────┘          │   │
│  │  ┌──────────┐  ┌──────────┐                        │   │
│  │  │ Chunker  │  │ LLMCall  │                        │   │
│  │  │          │  │  (OpenAI)│                        │   │
│  │  └──────────┘  └──────────┘                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                               │
│                            ▼                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              HelloAgents Framework                   │   │
│  │  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌─────────┐  │   │
│  │  │ LLM     │ │ Tools    │ │ Skills │ │ Context │  │   │
│  │  │ Adapter │ │ Registry  │ │ System │ │ Manager │  │   │
│  │  └─────────┘ └──────────┘ └────────┘ └─────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. 外部依赖来源

| 依赖 | 来源 | 许可证 | 用途 |
|:---|:---|:---|:---|
| hello-agents | [GitHub](https://github.com/jjyaoao/HelloAgents) | CC BY-NC-SA 4.0 | Agent 框架 |
| pypdf2 | PyPI | BSD-3-Clause | PDF 解析 |
| python-docx | PyPI | MIT | Word 解析 |
| httpx | PyPI | BSD-3-Clause | HTTP 客户端 |
| pandas | PyPI | BSD-3-Clause | 数据处理 |
| openpyxl | PyPI | MIT | Excel 支持 |
| pydantic | PyPI | MIT | 数据验证 |

---

## 6. 相关文档

- [[PRD.md]] - 产品需求文档
- [[implementation-plan.md]] - 实施计划
- [[architecture.md]] - 详细架构文档

---

*使用 Vibe Coding 方法论生成*
