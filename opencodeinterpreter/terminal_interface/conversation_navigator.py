"""
This file handles conversations.
"""

import json
import os
import platform
import subprocess

import inquirer

from .render_past_conversation import render_past_conversation
from .utils.display_markdown_message import display_markdown_message
from .utils.local_storage_path import get_storage_path


def conversation_navigator(interpreter):
    conversations_dir = get_storage_path("conversations")

    display_markdown_message(
        f"""> Conversations are stored in "`{conversations_dir}`".

    Select a conversation to resume.
    """
    )

    # 检查对话目录是否存在
    if not os.path.exists(conversations_dir):
        print(f"No conversations found in {conversations_dir}")
        return None

    # 获取目录中所有的JSON文件，按照修改时间进行排序，最新的排在前面
    json_files = sorted(
        [f for f in os.listdir(conversations_dir) if f.endswith(".json")],
        key=lambda x: os.path.getmtime(os.path.join(conversations_dir, x)),
        reverse=True,
    )

    # 获取目录中所有的JSON文件，按照修改时间进行排序，最新的排在前面
    # Make a dict that maps reformatted
    # "First few words... (September 23rd)" -> "First_few_words__September_23rd.json" (original file name)
    readable_names_and_filenames = {}
    for filename in json_files:
        name = (
                filename.replace(".json", "")
                .replace(".JSON", "")
                .replace("__", "... (")
                .replace("_", " ")
                + ")"
        )
        readable_names_and_filenames[name] = filename

    # 添加打开文件夹的选项。这不映射到文件名，我们会捕捉它
    # Add the option to open the folder. This doesn't map to a filename, we'll catch it
    readable_names_and_filenames["> Open folder"] = None

    # 使用inquirer让用户选择文件
    questions = [
        inquirer.List(
            "name",
            message="",
            choices=readable_names_and_filenames.keys(),
        ),
    ]
    answers = inquirer.prompt(questions)

    # 如果用户选择打开文件夹，那么执行相应操作并返回。
    if answers["name"] == "> Open folder":
        open_folder(conversations_dir)
        return

    selected_filename = readable_names_and_filenames[answers["name"]]

    # 打开所选文件并加载JSON数据
    with open(os.path.join(conversations_dir, selected_filename), "r") as f:
        messages = json.load(f)

    # 将数据传递给render_past_conversation
    render_past_conversation(messages)

    # 将解释器的设置设定为加载的消息
    interpreter.messages = messages
    interpreter.conversation_filename = selected_filename

    # 开始聊天
    interpreter.chat()


def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        # 假设它是Linux
        subprocess.run(["xdg-open", path])
