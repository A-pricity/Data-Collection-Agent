"""交互式 CLI 模块

提供用户友好的命令行交互界面
"""

import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm, Prompt, PromptType
    from rich.table import Table
except ImportError:
    Console = None
    Panel = None
    Confirm = None
    Prompt = None
    Table = None

from .config import settings
from .types import DataSource, DataType, OutputFormat, TaskIntent, TaskType


console = Console() if Console else None


class InteractiveCLI:
    def __init__(self):
        self.current_intent: Optional[TaskIntent] = None

    def print_welcome(self):
        if console:
            console.print(
                Panel.fit(
                    "[bold cyan]Data-Collection-Agent[/bold cyan]\n"
                    "LLM 驱动的多源数据智能处理智能体",
                    border_style="cyan",
                )
            )
        else:
            print("=" * 50)
            print("Data-Collection-Agent")
            print("LLM 驱动的多源数据智能处理智能体")
            print("=" * 50)

    def get_task_input(self) -> str:
        if console:
            task_input = Prompt.ask(
                "[bold green]请输入任务描述[/bold green]",
                default="帮我翻译 ArXiv 论文 2312.09875 为中文",
            )
        else:
            task_input = input("请输入任务描述: ")
        return task_input

    def confirm_task(self, task_description: str) -> bool:
        if console:
            return Confirm.ask(f"[yellow]确认执行任务:[/yellow] {task_description}")
        else:
            response = input(f"确认执行任务: {task_description} (y/n): ")
            return response.lower() in ("y", "yes")

    def select_data_source(self) -> DataSource:
        if console:
            choice = Prompt.ask(
                "[bold blue]选择数据源[/bold blue]",
                choices=["1", "2", "3", "4"],
                default="1",
            )
        else:
            print("1. ArXiv")
            print("2. 网页")
            print("3. GitHub")
            print("4. 本地文件")
            choice = input("选择数据源 [1]: ") or "1"

        source_map = {
            "1": DataSource.ARXIV,
            "2": DataSource.WEB,
            "3": DataSource.GITHUB,
            "4": DataSource.FILE,
        }
        return source_map.get(choice, DataSource.ARXIV)

    def select_task_type(self) -> TaskType:
        if console:
            choice = Prompt.ask(
                "[bold blue]选择任务类型[/bold blue]",
                choices=["1", "2", "3", "4"],
                default="1",
            )
        else:
            print("1. 翻译")
            print("2. 摘要")
            print("3. 信息抽取")
            print("4. 总结")
            choice = input("选择任务类型 [1]: ") or "1"

        task_map = {
            "1": TaskType.TRANSLATE,
            "2": TaskType.SUMMARIZE,
            "3": TaskType.EXTRACT,
            "4": TaskType.SUMMARY,
        }
        return task_map.get(choice, TaskType.TRANSLATE)

    def select_output_format(self) -> OutputFormat:
        if console:
            choice = Prompt.ask(
                "[bold blue]选择输出格式[/bold blue]",
                choices=["1", "2", "3", "4", "5"],
                default="1",
            )
        else:
            print("1. JSON")
            print("2. Excel")
            print("3. CSV")
            print("4. Word")
            print("5. Markdown")
            choice = input("选择输出格式 [1]: ") or "1"

        format_map = {
            "1": OutputFormat.JSON,
            "2": OutputFormat.EXCEL,
            "3": OutputFormat.CSV,
            "4": OutputFormat.DOCX,
            "5": OutputFormat.MARKDOWN,
        }
        return format_map.get(choice, OutputFormat.JSON)

    def show_progress(self, message: str):
        if console:
            console.print(f"[cyan]{message}[/cyan]")
        else:
            print(f"[进度] {message}")

    def show_result(self, result: dict):
        if console:
            table = Table(title="执行结果")
            table.add_column("状态", style="green")
            table.add_column("信息")
            table.add_row(result.get("status", "unknown"), result.get("message", ""))
            console.print(table)
        else:
            print("=" * 50)
            print(f"状态: {result.get('status', 'unknown')}")
            print(f"信息: {result.get('message', '')}")
            print("=" * 50)

    def show_error(self, error: str):
        if console:
            console.print(f"[bold red]错误:[/bold red] {error}")
        else:
            print(f"[错误] {error}")

    def run_interactive(self):
        self.print_welcome()

        task_input = self.get_task_input()
        if not task_input:
            self.show_error("任务描述不能为空")
            return

        if console:
            console.print(f"\n[dim]正在解析任务...[/dim]\n")

        self.current_intent = TaskIntent(
            data_source=self.select_data_source(),
            data_type=DataType.PDF,
            task_type=self.select_task_type(),
            output_format=self.select_output_format(),
            raw_input=task_input,
        )

        if self.confirm_task(task_input):
            self.show_progress("开始执行任务...")
            return self.current_intent
        else:
            self.show_error("任务已取消")
            return None


def main():
    cli = InteractiveCLI()
    intent = cli.run_interactive()
    if intent:
        print(f"\n任务配置: {intent.model_dump()}")
        print("\n提示: 请使用 Python API 执行完整任务")


if __name__ == "__main__":
    main()
