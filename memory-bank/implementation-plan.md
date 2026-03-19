# Implementation Plan - Data-Collection-Agent

**创建日期**: 2026-03-19
**最后更新**: 2026-03-19
**预计工期**: 1-2 天 (MVP)

---

## 阶段 1: 项目初始化 ✅

### 目标
完成项目基础结构和依赖配置

### 完成的任务
- [x] 初始化 uv 虚拟环境
- [x] 配置 pyproject.toml
- [x] 创建项目目录结构
- [x] 配置 .env.example
- [x] 创建 README.md
- [x] 创建 config.py - Settings 配置类
- [x] 创建 exceptions.py - 自定义异常
- [x] 创建 types.py - Pydantic 类型定义
- [x] 创建 cli.py - 交互式 CLI
- [x] 创建 __main__.py - CLI 模块入口
- [x] 创建 __init__.py - 包入口导出

### 验收标准
```bash
uv sync  # ✅ 成功执行
uv run python -c "from data_collection_agent import ..."  # ✅ 无报错
```

### 交付物
```
src/data_collection_agent/
├── __init__.py          # 包入口，导出主要类
├── __main__.py          # CLI: uv run python -m data_collection_agent
├── config.py            # Settings 配置类
├── exceptions.py        # 自定义异常
├── types.py             # Pydantic 模型
└── cli.py               # 交互式 CLI 入口
```

---

## 阶段 2: 核心引擎开发

### 2.1 意图理解引擎 (IntentParser)

**目标**: 将自然语言转换为结构化任务

#### 任务
- [ ] 创建 `src/data_collection_agent/core/intent_parser.py`
- [ ] 定义 TaskIntent Pydantic 模型
- [ ] 实现 LLM 调用解析
- [ ] 编写 Prompt 模板

#### 验收标准
```python
parser = IntentParser()
result = parser.parse("翻译 ArXiv 论文 2312.09875 为中文")
assert result.data_source == "arxiv"
assert result.task_type == "translate"
assert result.target_lang == "zh"
```

### 2.2 任务规划引擎 (TaskPlanner)

**目标**: 根据意图生成执行流程

#### 任务
- [ ] 创建 `src/data_collection_agent/core/task_planner.py`
- [ ] 实现流程模板系统
- [ ] 支持条件分支逻辑

#### 验收标准
```python
planner = TaskPlanner()
intent = TaskIntent(data_source="arxiv", task_type="translate")
steps = planner.plan(intent)
assert "collect_arxiv" in steps
assert "parse_pdf" in steps
assert "translate" in steps
```

### 2.3 执行引擎 (Executor)

**目标**: 按顺序执行任务步骤

#### 任务
- [ ] 创建 `src/data_collection_agent/core/executor.py`
- [ ] 实现步骤执行器
- [ ] 实现进度追踪

#### 验收标准
```python
executor = Executor(tools=tool_registry)
result = executor.execute(steps)
assert result.status == "success"
```

---

## 阶段 3: 工具开发

### 3.1 数据采集工具

#### ArXivCollector
- [ ] 创建 `src/data_collection_agent/tools/collectors/arxiv_collector.py`
- [ ] 实现 arxiv API 调用
- [ ] 实现 PDF 下载

#### WebCollector
- [ ] 创建 `src/data_collection_agent/tools/collectors/web_collector.py`
- [ ] 实现 httpx 异步采集
- [ ] 实现重试机制

#### FileCollector
- [ ] 创建 `src/data_collection_agent/tools/collectors/file_collector.py`
- [ ] 支持本地文件读取

### 3.2 文档解析工具

#### PDFParser
- [ ] 创建 `src/data_collection_agent/tools/parsers/pdf_parser.py`
- [ ] 实现 PyPDF2 文本提取
- [ ] 实现异常处理

#### DocxParser
- [ ] 创建 `src/data_collection_agent/tools/parsers/docx_parser.py`
- [ ] 实现 python-docx 解析

### 3.3 智能分块工具

#### Chunker
- [ ] 创建 `src/data_collection_agent/tools/chunker.py`
- [ ] 实现按段落分块
- [ ] 实现按窗口大小分块

### 3.4 LLM 调用工具

#### LLMCaller
- [ ] 创建 `src/data_collection_agent/tools/llm_caller.py`
- [ ] 实现统一接口
- [ ] 实现 translate/summarize/extract 方法
- [ ] 配置环境变量读取

### 3.5 导出工具

#### Exporters
- [ ] 创建 `src/data_collection_agent/tools/exporters.py`
- [ ] 实现 ExcelExporter
- [ ] 实现 JsonExporter
- [ ] 实现 CsvExporter
- [ ] 实现 DocxExporter

---

## 阶段 4: 集成与测试

### 4.1 端到端集成

- [ ] 创建主入口 `DataCollectionAgent` 类
- [ ] 集成所有模块
- [ ] 创建 CLI 入口

### 4.2 测试

- [ ] 单元测试（意图解析、任务规划）
- [ ] 集成测试（完整流程）
- [ ] Mock LLM 调用测试

### 验收标准
```bash
uv run pytest tests/ -v  # 全部通过
```

---

## 阶段 5: 文档与发布

- [ ] 完善 README.md
- [ ] 添加使用示例
- [ ] 提交 Git 并打标签

---

## 依赖关系

```
阶段1 (初始化) ✅
    │
    ▼
阶段2 (核心引擎)
    │
    ▼
阶段3 (工具开发)
    │
    ▼
阶段4 (集成测试)
    │
    ▼
阶段5 (文档发布)
```

---

## 每日目标

| 日期 | 目标 | 状态 |
|:---|:---|:---|
| Day 1 AM | 项目初始化 + 意图理解引擎 | 阶段1完成 |
| Day 1 PM | 任务规划引擎 + 执行引擎 | 待完成 |
| Day 2 AM | 采集器 + 解析器 | 待完成 |
| Day 2 PM | 分块 + LLM + 导出 + 集成测试 | 待完成 |

---

*使用 Vibe Coding 方法论生成*
