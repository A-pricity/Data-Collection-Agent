"""自定义异常模块

定义项目专用的异常类型，便于错误处理和日志记录
"""

from typing import Any, Dict, Optional


class DataCollectionError(Exception):
    message: str
    details: Dict[str, Any]

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class IntentParseError(DataCollectionError):
    def __init__(self, message: str, raw_input: str = ""):
        super().__init__(
            message=f"意图解析失败: {message}", details={"raw_input": raw_input}
        )


class TaskPlanError(DataCollectionError):
    pass


class CollectionError(DataCollectionError):
    def __init__(self, message: str, source: str = ""):
        super().__init__(message=f"采集失败: {message}", details={"source": source})


class ParseError(DataCollectionError):
    def __init__(self, message: str, file_path: str = ""):
        super().__init__(
            message=f"解析失败: {message}", details={"file_path": file_path}
        )


class ChunkError(DataCollectionError):
    pass


class LLMError(DataCollectionError):
    def __init__(self, message: str, model: str = ""):
        super().__init__(message=f"LLM 调用失败: {message}", details={"model": model})


class ExportError(DataCollectionError):
    def __init__(self, message: str, format: str = ""):
        super().__init__(message=f"导出失败: {message}", details={"format": format})


class ConfigurationError(DataCollectionError):
    pass


class ValidationError(DataCollectionError):
    pass
