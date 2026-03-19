# Architecture - Data-Collection-Agent

**最后更新**: 2026-03-19

---

## 1. 目录结构

```
data-collection-agent/
├── src/
│   └── data_collection_agent/
│       ├── __init__.py
│       ├── __main__.py              # CLI 入口
│       ├── agent.py                 # 主 Agent 类
│       ├── core/                    # 核心引擎
│       │   ├── __init__.py
│       │   ├── intent_parser.py     # 意图理解
│       │   ├── task_planner.py      # 任务规划
│       │   └── executor.py          # 执行引擎
│       ├── tools/                   # 工具层
│       │   ├── __init__.py
│       │   ├── base.py              # 工具基类
│       │   ├── collectors/          # 采集器
│       │   │   ├── __init__.py
│       │   │   ├── arxiv.py
│       │   │   ├── web.py
│       │   │   └── file.py
│       │   ├── parsers/            # 解析器
│       │   │   ├── __init__.py
│       │   │   ├── pdf.py
│       │   │   └── docx.py
│       │   ├── chunker.py          # 智能分块
│       │   ├── llm_caller.py       # LLM 调用
│       │   └── exporters.py        # 导出工具
│       ├── skills/                  # Skills (HelloAgents 兼容)
│       │   └── data_collection_skill.py
│       └── utils/
│           ├── __init__.py
│           ├── config.py            # 配置管理
│           └── exceptions.py        # 异常定义
├── tests/
│   ├── __init__.py
│   ├── test_intent_parser.py
│   ├── test_task_planner.py
│   ├── test_collectors.py
│   └── test_exporters.py
├── memory-bank/                      # 记忆库
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

---

## 2. 模块设计

### 2.1 核心引擎层 (core/)

#### IntentParser
```
职责: 将用户自然语言转换为结构化任务
输入: str (用户描述)
输出: TaskIntent (Pydantic 模型)
依赖: LLMCaller
```

#### TaskPlanner
```
职责: 根据意图生成执行流程
输入: TaskIntent
输出: List[Step]
依赖: 流程模板
```

#### Executor
```
职责: 按顺序执行任务步骤
输入: List[Step]
输出: ExecutionResult
依赖: ToolRegistry, 各类工具
```

### 2.2 工具层 (tools/)

#### 采集器 (collectors/)
```
ArXivCollector    - ArXiv 论文采集
WebCollector     - 网页采集
FileCollector    - 本地文件采集
```

#### 解析器 (parsers/)
```
PDFParser        - PDF 文本提取
DocxParser       - Word 文档解析
```

#### 其他工具
```
Chunker          - 智能分块
LLMCaller        - LLM 统一调用
Exporters        - 多格式导出
```

---

## 3. 数据流

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户输入                                  │
│              "翻译 ArXiv 论文 2312.09875 为中文"                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      IntentParser                               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ LLM 解析 → TaskIntent{                                    │  │
│  │   data_source: "arxiv",                                   │  │
│  │   task_type: "translate",                                 │  │
│  │   source_lang: "en",                                      │  │
│  │   target_lang: "zh"                                       │  │
│  │ }                                                         │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TaskPlanner                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 生成步骤:                                                  │  │
│  │ 1. collect_arxiv (2312.09875)                             │  │
│  │ 2. parse_pdf                                              │  │
│  │ 3. chunk_text                                             │  │
│  │ 4. translate (en→zh)                                     │  │
│  │ 5. export_excel                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Executor                                 │
│                                                                   │
│  Step 1: ArXivCollector.download(2312.09875)                     │
│     → /tmp/2312.09875.pdf                                       │
│                                                                   │
│  Step 2: PDFParser.extract(/tmp/2312.09875.pdf)                 │
│     → "Paper content text..."                                   │
│                                                                   │
│  Step 3: Chunker.chunk("Paper content...")                      │
│     → ["Chunk 1", "Chunk 2", ...]                              │
│                                                                   │
│  Step 4: LLMCaller.translate(chunks, en→zh)                     │
│     → ["中文Chunk 1", "中文Chunk 2", ...]                      │
│                                                                   │
│  Step 5: ExcelExporter.export(chunks)                           │
│     → result.xlsx                                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        输出结果                                  │
│                    /path/to/result.xlsx                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 关键接口设计

### 4.1 TaskIntent (Pydantic 模型)

```python
class TaskIntent(BaseModel):
    """意图理解结果"""
    data_source: Literal["arxiv", "web", "github", "file"]
    data_type: Literal["pdf", "docx", "txt", "html"]
    task_type: Literal["translate", "summarize", "extract", "summarize"]
    source_lang: str = "auto"
    target_lang: str = "zh"
    output_format: Literal["excel", "json", "csv", "docx"]
    model: Optional[str] = None
    raw_input: str  # 原始用户输入
```

### 4.2 工具基类

```python
class BaseTool(ABC):
    """工具基类"""
    name: str
    description: str
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """执行工具"""
        pass
```

### 4.3 LLM 调用接口

```python
class LLMCaller:
    """LLM 统一调用"""
    
    def __init__(self, base_url: str, model_id: str, api_key: str):
        ...
    
    async def translate(
        self, 
        text: str, 
        source_lang: str = "auto", 
        target_lang: str = "zh"
    ) -> str:
        """翻译文本"""
        ...
    
    async def summarize(self, text: str, max_length: int = 500) -> str:
        """摘要文本"""
        ...
    
    async def extract(self, text: str, schema: dict) -> dict:
        """信息抽取"""
        ...
```

---

## 5. 配置管理

### 5.1 环境变量

```python
# src/data_collection_agent/utils/config.py

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    
    # LLM 配置
    llm_base_url: str = "https://api.deepseek.com"
    llm_model_id: str = "deepseek-chat"
    llm_api_key: str = ""
    
    # 采集配置
    collection_timeout: int = 30
    collection_max_retries: int = 3
    
    # 分块配置
    chunk_max_tokens: int = 2000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## 6. 异常处理

```python
# src/data_collection_agent/utils/exceptions.py

class DataCollectionError(Exception):
    """基础异常"""
    pass

class IntentParseError(DataCollectionError):
    """意图解析失败"""
    pass

class CollectionError(DataCollectionError):
    """采集失败"""
    pass

class ParseError(DataCollectionError):
    """解析失败"""
    pass

class LLMError(DataCollectionError):
    """LLM 调用失败"""
    pass

class ExportError(DataCollectionError):
    """导出失败"""
    pass
```

---

## 7. HelloAgents 集成

### 7.1 工具注册

```python
from hello_agents import ToolRegistry
from hello_agents.tools.builtin import ...

registry = ToolRegistry()
registry.register_tool(ArxivCollectorTool())
registry.register_tool(WebCollectorTool())
registry.register_tool(PDFParserTool())
registry.register_tool(ChunkerTool())
registry.register_tool(LLMCallerTool())
registry.register_tool(ExcelExporterTool())
```

### 7.2 Agent 配置

```python
from hello_agents import ReActAgent, HelloAgentsLLM

llm = HelloAgentsLLM()
agent = ReActAgent(
    name="data-collection-agent",
    llm=llm,
    tool_registry=registry
)
```

---

## 8. 扩展点

### 8.1 新增采集器
```python
class BaseCollector(ABC):
    @abstractmethod
    async def collect(self, source: str) -> bytes: ...

class GitHubCollector(BaseCollector):
    async def collect(self, source: str) -> bytes:
        # GitHub API 实现
        ...
```

### 8.2 新增解析器
```python
class BaseParser(ABC):
    @abstractmethod
    async def parse(self, content: bytes) -> str: ...

class MarkdownParser(BaseParser):
    async def parse(self, content: bytes) -> str:
        # Markdown 解析实现
        ...
```

### 8.3 新增导出格式
```python
class BaseExporter(ABC):
    @abstractmethod
    async def export(self, data: Any, path: Path) -> None: ...

class MarkdownExporter(BaseExporter):
    async def export(self, data: Any, path: Path) -> None:
        # Markdown 导出实现
        ...
```

---

## 9. 相关文档

- [[PRD.md]] - 产品需求文档
- [[tech-stack.md]] - 技术栈详情
- [[implementation-plan.md]] - 实施计划

---

*使用 Vibe Coding 方法论生成*
