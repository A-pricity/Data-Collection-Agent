# Data-Collection-Agent

LLM 驱动的多源数据智能处理智能体

## 项目概述

Data-Collection-Agent 是一个基于 HelloAgents 框架构建的自动化数据处理智能体。用户只需输入一句自然语言，Agent 就能自主完成：

- 数据采集（ArXiv、网页、本地文件）
- 文档解析（PDF、Word）
- 智能分块
- LLM 处理（翻译、摘要、信息抽取）
- 多格式导出（Excel、JSON、CSV、Word）

## 核心价值

**用户输入 → Agent 全自动执行 → 直接交付文件**

无需配置、无需代码，真正实现大数据智能处理自动化。

## 技术栈

- **框架**: HelloAgents 1.0.0
- **语言**: Python 3.10+
- **LLM**: DeepSeek / Qwen / OpenAI（通过环境变量配置）
- **PDF 解析**: PyPDF2
- **Word 解析**: python-docx
- **数据处理**: pandas + openpyxl
- **环境管理**: uv

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-repo/data-collection-agent.git
cd data-collection-agent

# 安装依赖
uv sync
```

### 配置

复制 `.env.example` 为 `.env` 并配置 LLM：

```bash
cp .env.example .env
# 编辑 .env 填写 API Key
```

### 使用

```python
from data_collection_agent import DataCollectionAgent

agent = DataCollectionAgent()

# 自然语言输入
result = agent.run(
    "帮我翻译 ArXiv 上的论文 2312.09875，输出 Excel"
)

print(result.output_file)
```

## 项目结构

```
data-collection-agent/
├── src/data_collection_agent/
│   ├── core/              # 核心引擎
│   │   ├── intent_parser.py   # 意图理解
│   │   ├── task_planner.py    # 任务规划
│   │   └── executor.py       # 执行引擎
│   ├── tools/             # 工具集
│   │   ├── collectors/   # 采集器
│   │   ├── parsers/      # 解析器
│   │   ├── chunker.py    # 智能分块
│   │   ├── llm_caller.py # LLM 调用
│   │   └── exporters.py  # 导出工具
│   └── ...
├── tests/                # 测试
├── memory-bank/           # 记忆库
└── ...
```

## 开发

```bash
# 运行测试
uv run pytest tests/

# 代码格式化
uv run ruff format src/

# 类型检查
uv run mypy src/
```

## 相关资源

- [HelloAgents 框架](https://github.com/jjyaoao/HelloAgents)
- [hello-agents 教程](https://github.com/datawhalechina/hello-agents)
- [在线文档](https://datawhalechina.github.io/hello-agents/)

## License

CC BY-NC-SA 4.0
