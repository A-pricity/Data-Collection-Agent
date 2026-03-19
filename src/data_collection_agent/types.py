"""类型定义模块

使用 Pydantic 定义项目的数据结构和类型
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class DataSource(str, Enum):
    """数据源枚举"""

    ARXIV = "arxiv"
    WEB = "web"
    GITHUB = "github"
    FILE = "file"


class DataType(str, Enum):
    """数据类型枚举"""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"


class TaskType(str, Enum):
    """任务类型枚举"""

    TRANSLATE = "translate"
    SUMMARIZE = "summarize"
    EXTRACT = "extract"
    SUMMARY = "summary"


class OutputFormat(str, Enum):
    """输出格式枚举"""

    EXCEL = "excel"
    JSON = "json"
    CSV = "csv"
    DOCX = "docx"
    MARKDOWN = "markdown"


class TaskIntent(BaseModel):
    """意图理解结果

    将用户自然语言解析为结构化任务
    """

    # 必填字段
    data_source: DataSource
    data_type: DataType
    task_type: TaskType

    # 可选字段
    source_lang: str = "auto"
    target_lang: str = "zh"
    output_format: OutputFormat = OutputFormat.JSON

    # 原始输入
    raw_input: str = ""

    # 额外参数
    extra: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class Step(BaseModel):
    """任务步骤

    表示执行流程中的一个步骤
    """

    name: str
    description: str = ""
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    retry: int = 3
    required: bool = True


class ExecutionResult(BaseModel):
    """执行结果

    表示任务执行的最终结果
    """

    status: Literal["success", "failed", "partial"]
    message: str = ""
    output_file: Optional[str] = None
    data: Optional[Any] = None
    steps_executed: List[str] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    stats: Dict[str, int] = Field(default_factory=dict)


class ChunkResult(BaseModel):
    """分块结果"""

    chunks: List[str]
    total_tokens: int = 0
    chunk_count: int = 0


class ParseResult(BaseModel):
    """解析结果"""

    text: str
    page_count: int = 0
    file_path: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CollectionResult(BaseModel):
    """采集结果"""

    content: bytes
    source: str
    source_type: DataSource
    metadata: Dict[str, Any] = Field(default_factory=dict)
