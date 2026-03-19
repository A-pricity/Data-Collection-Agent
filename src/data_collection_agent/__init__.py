"""Data-Collection-Agent - LLM 驱动的多源数据智能处理智能体"""

from .config import Settings, get_settings, settings
from .types import (
    ChunkResult,
    CollectionResult,
    DataSource,
    DataType,
    ExecutionResult,
    OutputFormat,
    ParseResult,
    Step,
    TaskIntent,
    TaskType,
)
from .exceptions import (
    ChunkError,
    CollectionError,
    ConfigurationError,
    DataCollectionError,
    ExportError,
    IntentParseError,
    LLMError,
    ParseError,
    TaskPlanError,
    ValidationError,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "Settings",
    "get_settings",
    "settings",
    "TaskIntent",
    "TaskType",
    "DataSource",
    "DataType",
    "OutputFormat",
    "Step",
    "ExecutionResult",
    "ChunkResult",
    "ParseResult",
    "CollectionResult",
    "DataCollectionError",
    "IntentParseError",
    "TaskPlanError",
    "CollectionError",
    "ParseError",
    "ChunkError",
    "LLMError",
    "ExportError",
    "ConfigurationError",
    "ValidationError",
]
