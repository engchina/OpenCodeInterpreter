import traceback

from .rag.get_relevant_procedures_string import get_relevant_procedures_string
from .utils.get_user_info_string import get_user_info_string


def generate_system_message(interpreter):
    """
    动态生成一条系统消息。

    接受一个解释器实例，
    返回一个字符串。

    这很容易替换!
    只需用另一个函数替换 `opencodeinterpreter.generate_system_message` 即可。
    """

    # 开始使用静态系统消息

    system_message = interpreter.system_message

    # 添加动态组件，如用户的操作系统、用户名、相关程序等

    system_message += "\n" + get_user_info_string()

    # DISABLED
    # because wait, they'll have terminal open, no text will be selected. if we find a way to call `--os` mode from anywhere, this will be cool though.
    # if interpreter.os:
    #     # Add the user's selection to to the system message in OS mode
    #     try:
    #         selected_text = interpreter.computer.clipboard.get_selected_text()
    #         if len(selected_text) > 20:
    #             system_message += "\nThis is a preview of the user's selected text: " + selected_text[:20] + "..." + selected_text[-20:]
    #     except:
    #         pass

    if not interpreter.local and not interpreter.disable_procedures:
        try:
            system_message += "\n" + get_relevant_procedures_string(interpreter)
        except:
            if interpreter.debug_mode:
                print(traceback.format_exc())
            # It's okay if they can't. This just fixes some common mistakes it makes.

    for language in interpreter.computer.terminal.languages:
        if hasattr(language, "system_message"):
            system_message += "\n\n" + language.system_message

    return system_message.strip()
