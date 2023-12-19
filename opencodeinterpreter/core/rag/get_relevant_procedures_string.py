import requests

from ..utils.convert_to_openai_messages import convert_to_openai_messages


def get_relevant_procedures_string(interpreter):
    # Open Procedures 是一个开源的小型、实时更新的编程教程数据库。
    # 我们可以使用最后两条消息对其进行语义查询，并将相关的教程/过程附加到我们的系统消息中。

    # 将最后两条消息转换为所需的OpenAI兼容的`messages`列表。
    messages = convert_to_openai_messages(
        interpreter.messages[-2:], function_calling=False, vision=False
    )
    messages = [{"role": "system", "content": interpreter.system_message}] + messages
    query = {"query": messages}
    url = "https://open-procedures.replit.app/search/"

    response = requests.post(url, json=query).json()

    if interpreter.debug_mode:
        print(response)

    relevant_procedures = response["procedures"]
    relevant_procedures = "[Recommended Procedures]\n" + "\n---\n".join(
        relevant_procedures
    )
    if not interpreter.os and not interpreter.vision:
        # 在您的计划中，**包括具体的步骤以及针对相关的弃用通知，
        # 确保保留相关的代码片段**——这些通知将在您执行第一行代码时消失，所以现在就把它们记下来。
        relevant_procedures += ("\nIn your plan, include steps and, for relevant deprecation notices, "
                                "**EXACT CODE SNIPPETS** -- these notices will VANISH "
                                "once you execute your first line of code, so WRITE THEM DOWN NOW if you need them.")

    return relevant_procedures
