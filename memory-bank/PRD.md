# Data-Collection-Agent PRD

**项目名称**: Data-Collection-Agent（多源数据智能处理智能体）
**创建日期**: 2026-03-19
**框架基础**: HelloAgents (jjyaoao/HelloAgents)
**项目类型**: LLM 应用 / Agent

---

## 1. 项目概述 (Overview)

### 1.1 产品定位

LLM 驱动的企业级数据处理自动化 Agent，面向大数据智能处理、工作流构建、开源数据采集、富文本解析等场景。

### 1.2 核心价值

**用户输入一句自然语言 → Agent 自主决策、自主执行、自主串联全流程 → 直接交付最终文件**

### 1.3 目标用户

- 项目经理 / 产品经理（不会代码）
- 大模型应用实习生
- 数据智能处理岗位求职者
- 需要快速处理数据的非技术人员

### 1.4 解决的问题

| 痛点 | 解决方案 |
|:---|:---|
| 人工处理数据成本极高 | 采集→解析→处理→导出全自动 |
| 大模型使用门槛高 | Agent 自主处理长文本分块、API 调用 |
| 工具碎片化 | 统一 Agent 框架串联所有工具 |
| 不会代码无法搭建流程 | 自然语言输入，无需配置 |

---

## 2. 功能需求 (Functional Requirements)

### 2.1 核心功能矩阵

| 模块 | 功能 | 优先级 | 验收标准 |
|:---|:---|:---|:---|
| **意图理解引擎** | 自然语言 → 结构化任务 JSON | P0 | 能解析数据源、数据类型、处理任务、语种、输出格式 |
| **任务规划引擎** | 自动生成执行流程 | P0 | 根据意图生成：采集→解析→分块→LLM→导出 |
| **数据采集工具** | 采集网页/ArXiv/GitHub/本地文件 | P0 | 支持 requests/httpx/aiohttp 异步采集 |
| **文档解析工具** | PDF/Word 解析 | P0 | PyPDF2 解析 PDF，python-docx 解析 Word |
| **智能分块工具** | 长文本语义分块 | P0 | 支持按语义/段落/窗口大小分块 |
| **LLM 调用工具** | 统一调用多种大模型 | P0 | 支持 DeepSeek/Qwen/OpenAI，通过环境变量配置 |
| **导出工具** | Excel/JSON/CSV/Word 导出 | P0 | pandas + openpyxl 导出 |
| **异常自治引擎** | 失败重试/跳过/报错 | P1 | 采集失败重试、解析失败标记、LLM 调用自动重试 |

### 2.2 意图理解引擎 - 必解析字段

```json
{
  "data_source": "ArXiv | 网页 | GitHub | 本地文件",
  "data_type": "PDF | 文本 | Excel | Word",
  "task_type": "翻译 | 摘要 | 信息抽取 | 总结",
  "source_lang": "中文 | 英文 | 其他",
  "target_lang": "中文 | 英文 | 其他",
  "output_format": "Excel | JSON | Word | CSV",
  "model": "通过环境变量配置"
}
```

### 2.3 任务规划引擎 - 流程示例

```
输入: "帮我把 ArXiv 上的这篇论文翻译成中文，输出 Excel"

生成流程:
1. 采集 ArXiv PDF
2. 下载 PDF 文件
3. 解析 PDF 文本
4. 智能分块（按段落）
5. 调用 LLM 翻译
6. 格式转换（JSON → Excel）
7. 导出最终文件
```

---

## 3. 技术架构 (Technical Architecture)

### 3.1 框架选型

**基础框架**: [HelloAgents](https://github.com/jjyaoao/HelloAgents)
- 28.7k stars 的 Datawhale hello-agents 教程配套框架
- 885 stars 生产级实现
- CC BY-NC-SA 4.0 许可证

**框架核心能力**:
- 工具响应协议（ToolResponse）
- 上下文工程（HistoryManager/TokenCounter）
- 会话持久化（SessionStore）
- 子代理机制（TaskTool）
- 熔断器（CircuitBreaker）
- Skills 知识外化系统
- TodoWrite 进度管理
- DevLog 决策记录
- SSE 流式输出
- 异步生命周期

### 3.2 技术栈

| 层级 | 技术 | 版本 | 说明 |
|:---|:---|:---|:---|
| **运行时** | Python | 3.10+ | |
| **Agent 框架** | HelloAgents | 1.0.0 | 核心框架 |
| **LLM 调用** | OpenAI SDK | 1.x | 兼容 DeepSeek/Qwen |
| **PDF 解析** | PyPDF2 | 3.x | PDF 文本提取 |
| **Word 解析** | python-docx | 1.x | DOCX 解析 |
| **HTTP 客户端** | httpx | 0.27.x | 同步/异步 HTTP |
| **数据处理** | pandas | 2.x | 数据框架 |
| **Excel 导出** | openpyxl | 3.x | xlsx 支持 |
| **环境管理** | uv | - | 虚拟环境 + 包管理 |
| **类型检查** | pydantic | 2.x | 数据验证 |

### 3.3 项目结构

```
data-collection-agent/
├── src/
│   └── data_collection_agent/
│       ├── __init__.py
│       ├── core/                    # 核心模块
│       │   ├── __init__.py
│       │   ├── intent_parser.py     # 意图理解引擎
│       │   ├── task_planner.py     # 任务规划引擎
│       │   └── executor.py         # 执行引擎
│       ├── tools/                   # 工具集
│       │   ├── __init__.py
│       │   ├── collectors/         # 采集工具
│       │   │   ├── __init__.py
│       │   │   ├── web_collector.py
│       │   │   ├── arxiv_collector.py
│       │   │   └── file_collector.py
│       │   ├── parsers/            # 解析工具
│       │   │   ├── __init__.py
│       │   │   ├── pdf_parser.py
│       │   │   └── docx_parser.py
│       │   ├── chunker.py         # 智能分块
│       │   ├── llm_caller.py      # LLM 调用
│       │   └── exporters.py       # 导出工具
│       ├── skills/                 # Skills（HelloAgents）
│       │   ├── __init__.py
│       │   ├── data_collection_skill.py
│       │   └── ...
│       └── utils/
│           ├── __init__.py
│           └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── test_intent_parser.py
│   ├── test_collectors.py
│   └── test_parsers.py
├── memory-bank/
│   ├── PRD.md                      # 本文件
│   ├── tech-stack.md               # 技术栈详情
│   ├── implementation-plan.md      # 实施计划
│   ├── progress.md                 # 开发进度
│   └── architecture.md             # 架构文档
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

---

## 4. 模块详细设计

### 4.1 意图理解引擎 (IntentParser)

**输入**: 用户自然语言描述

**输出**: 结构化任务 JSON

**实现要点**:
- 使用 LLM 解析用户意图
- Prompt 模板定义必解析字段
- Pydantic 模型验证输出

### 4.2 任务规划引擎 (TaskPlanner)

**输入**: 意图理解结果

**输出**: 执行步骤列表

**实现要点**:
- 根据 data_source 和 task_type 生成流程
- 支持的条件分支：
  - data_source=ArXiv → ArXivCollector
  - data_source=网页 → WebCollector
  - data_type=PDF → PDFParser
  - data_type=Word → DocxParser
  - task_type=翻译 → LLM.translate()
  - task_type=摘要 → LLM.summarize()

### 4.3 执行引擎 (Executor)

**职责**:
- 按顺序执行任务步骤
- 异常捕获与重试
- 进度追踪

### 4.4 数据采集工具

| 采集器 | 数据源 | 实现 |
|:---|:---|:---|
| ArXivCollector | ArXiv 论文 | arXiv API + PDF 下载 |
| WebCollector | 网页 | httpx 异步采集 |
| GitHubCollector | GitHub | GitHub API |
| FileCollector | 本地文件 | pathlib |

### 4.5 文档解析工具

| 解析器 | 文件类型 | 实现 |
|:---|:---|:---|
| PDFParser | .pdf | PyPDF2 文本提取 |
| DocxParser | .docx | python-docx |

### 4.6 智能分块工具 (Chunker)

**分块策略**:
- 按段落分块
- 按语义分块（LLM 判断）
- 按窗口大小分块（token 数量）

### 4.7 LLM 调用工具

**统一接口**:
```python
class LLMCaller:
    def translate(self, text: str, source: str, target: str) -> str
    def summarize(self, text: str) -> str
    def extract(self, text: str, schema: dict) -> dict
```

**环境变量配置**:
```bash
export BASE_URL="https://api.deepseek.com"  # 或其他 API 地址
export MODEL_ID="deepseek-chat"             # 模型名称
export API_KEY="sk-xxx"                      # API 密钥
```

### 4.8 导出工具 (Exporters)

**支持格式**:
- Excel: pandas + openpyxl
- JSON: 内置 json 模块
- CSV: pandas
- Word: python-docx

---

## 5. 非功能需求 (Non-Functional Requirements)

### 5.1 性能要求

- 异步采集：支持并发 10+ 请求
- 单个 PDF 解析：< 5 秒
- LLM 调用：支持批量处理

### 5.2 可用性要求

- 用户只需输入自然语言
- 无需配置文件
- 错误信息友好

### 5.3 可扩展性

- 新的采集器可通过继承扩展
- 新的 LLM 提供商可通过适配器支持

---

## 6. 里程碑 (Milestones)

### V1.0 (1-2 天) - MVP

- [ ] 意图理解引擎
- [ ] 任务规划引擎
- [ ] PDF 解析接入
- [ ] LLM API 接入（多模型配置）
- [ ] 智能分块
- [ ] Excel/JSON/CSV 导出

### V1.1 (后续迭代)

- [ ] Web 采集器
- [ ] ArXiv 采集器
- [ ] Word 解析
- [ ] 异常自治引擎完善

---

## 7. 环境配置

### 7.1 依赖安装

```bash
# 使用 uv 管理
uv sync

# 或手动安装
uv add hello-agents pypdf2 python-docx httpx pandas openpyxl pydantic python-dotenv
```

### 7.2 环境变量 (.env)

```bash
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=sk-xxx
```

---

## 8. 使用示例

### 8.1 基本使用

```python
from data_collection_agent import DataCollectionAgent

agent = DataCollectionAgent()

# 自然语言输入
result = agent.run(
    "帮我翻译 ArXiv 上的论文 2312.09875，输出 Excel"
)

# 查看结果
print(result.output_file)  # /path/to/result.xlsx
```

### 8.2 多模型配置

```python
from data_collection_agent import DataCollectionAgent

# 使用 Qwen
agent = DataCollectionAgent(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model_id="qwen-plus"
)
```

---

## 9. 风险与依赖

| 风险 | 影响 | 缓解措施 |
|:---|:---|:---|
| LLM API 不可用 | 无法处理数据 | 熔断器降级、本地缓存 |
| PDF 加密/损坏 | 解析失败 | 异常捕获、友好提示 |
| 网络超时 | 采集失败 | 重试机制、超时配置 |

---

## 10. 参考资料

- [HelloAgents 框架](https://github.com/jjyaoao/HelloAgents)
- [hello-agents 教程](https://github.com/datawhalechina/hello-agents)
- [Datawhale 教程在线阅读](https://datawhalechina.github.io/hello-agents/)

---

*使用 Vibe Coding 方法论 + spec 开发规范生成*
