from rich import print as rich_print
from rich.markdown import Markdown
from rich.rule import Rule


def display_markdown_message(message):
    """
    显示 Markdown 信息。支持具有大量缩进的多行字符串。
    自动使单行 > 标签更美观。
    Display markdown message. Works with multiline strings with lots of indentation.
    Will automatically make single line > tags beautiful.
    """

    for line in message.split("\n"):
        line = line.strip()
        if line == "":
            print("")
        elif line == "---":
            rich_print(Rule(style="white"))
        else:
            rich_print(Markdown(line))

    if "\n" not in message and message.startswith(">"):
        # 审美选择。对于这些标签，它们需要在下面留有空间。
        # Aesthetic choice. For these tags, they need a space below them
        print("")
