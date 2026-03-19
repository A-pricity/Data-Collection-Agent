"""Data-Collection-Agent CLI

交互式命令行入口
"""

from data_collection_agent.cli import InteractiveCLI


def main():
    cli = InteractiveCLI()
    cli.print_welcome()

    task_input = cli.get_task_input()
    if not task_input:
        cli.show_error("任务描述不能为空")
        return

    cli.show_progress(f"已接收任务: {task_input}")
    cli.show_progress("提示: 请使用 Python API 执行完整任务")


if __name__ == "__main__":
    main()
