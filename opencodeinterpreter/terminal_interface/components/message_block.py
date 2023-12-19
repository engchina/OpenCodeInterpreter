import re

from rich.box import MINIMAL
from rich.markdown import Markdown
from rich.panel import Panel

from .base_block import BaseBlock


class MessageBlock(BaseBlock):
    def __init__(self):
        super().__init__()

        self.type = "message"
        self.message = ""

    def refresh(self, cursor=True):
        # 将Markdown中的所有代码块去除样式，以与我们的代码块区分开来。
        content = textify_markdown_code_blocks(self.message)

        if cursor:
            content += "●"

        markdown = Markdown(content.strip())
        panel = Panel(markdown, box=MINIMAL)
        self.live.update(panel)
        self.live.refresh()


def textify_markdown_code_blocks(text):
    """
    为了将CodeBlocks与Markdown代码区分开来，我们只需将所有的Markdown代码
    （如'```python...'）转换为文本代码块（'```text'），这样代码就会变成黑白的。
    """
    replacement = "```text"
    lines = text.split("\n")
    inside_code_block = False

    for i in range(len(lines)):
        # 如果行与```符号（可选择的语言说明符）匹配
        if re.match(r"^```(\w*)$", lines[i].strip()):
            inside_code_block = not inside_code_block

            # 如果我们刚刚进入了代码块，替换标记
            if inside_code_block:
                lines[i] = replacement

    return "\n".join(lines)
