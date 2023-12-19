from rich.box import MINIMAL
from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from .base_block import BaseBlock


class CodeBlock(BaseBlock):
    """
    代码块显示不同语言的代码和输出。您还可以设置active line！
    """

    def __init__(self):
        super().__init__()

        self.type = "code"

        # 为IDE自动补全功能定义这些
        # Define these for IDE auto-completion
        self.language = ""
        self.output = ""
        self.code = ""
        self.active_line = None
        self.margin_top = True

    def end(self):
        self.active_line = None
        self.refresh(cursor=False)
        super().end()

    def refresh(self, cursor=True):
        if not self.code and not self.output:
            return

        # 获取代码
        code = self.code

        # 为代码创建一个table
        code_table = Table(
            show_header=False, show_footer=False, box=None, padding=0, expand=True
        )
        code_table.add_column()

        # 添加cursor
        if cursor:
            code += "●"

        # 将每行代码添加到表格中
        code_lines = code.strip().split("\n")
        for i, line in enumerate(code_lines, start=1):
            if i == self.active_line:
                # 这是active line，用白色背景打印它
                syntax = Syntax(
                    line, self.language, theme="bw", line_numbers=False, word_wrap=True
                )
                code_table.add_row(syntax, style="black on white")
            else:
                # 这不是active line，正常打印
                syntax = Syntax(
                    line,
                    self.language,
                    theme="monokai",
                    line_numbers=False,
                    word_wrap=True,
                )
                code_table.add_row(syntax)

        # 为代码创建一个面板
        code_panel = Panel(code_table, box=MINIMAL, style="on #272722")

        # 创建一个用于输出的面板（如果有输出的话）
        if self.output == "" or self.output == "None":
            output_panel = ""
        else:
            output_panel = Panel(self.output, box=MINIMAL, style="#FFFFFF on #3b3b37")

        # 创建一个包含代码表和输出面板的组。
        group_items = [code_panel, output_panel]
        if self.margin_top:
            # 这添加了顶部的一些空间。看起来很棒！
            group_items = [""] + group_items
        group = Group(*group_items)

        # 更新实时显示
        self.live.update(group)
        self.live.refresh()
