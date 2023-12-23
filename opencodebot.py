import gradio as gr

import opencodeinterpreter as interpreter
from gr_components.utils.prompts import PROMPTS


def save_settings(api_base, api_key, conversation):
    interpreter.api_base = api_base
    interpreter.api_key = api_key
    interpreter.model = "gpt-3.5-turbo"
    interpreter.conversation_filename = conversation + ".txt"
    interpreter.conversation_history = True
    interpreter.context_window = 4096
    interpreter.temperature = 0.00
    interpreter.max_tokens = 2048
    interpreter.system_message = PROMPTS.system_message
    interpreter.auto_run = True
    interpreter.local = True
    return gr.update(selected="chatbot")


def add_file(history, file):
    # print(f"history: {history}")
    user_msg = "Uploaded file to: `" + file.name + "`"
    history = history + [(user_msg, file.name)]
    interpreter.messages = history
    # print(f"history: {history}")
    return history


def add_file_bot(history):
    history[-1][1] = "Uploaded file to: `" + history[-1][1] + "` successfully"
    yield history


def convert_to_interpreter_messages(history):
    messages = []
    for message in history:
        messages.append({"role": "user", "message": message[0], "content": message[1]})
    return messages


def add_user_msg(history, user_msg):
    interpreter.messages = convert_to_interpreter_messages(history)
    # print(f"history: {history}")
    history = history + [(user_msg, None)]
    # print(f"history: {history}")
    return history, gr.update(value="", interactive=False)


def chat(history):
    print(f"history: {history}")
    user_message = history[-1][0]
    history[-1][1] = ""
    active_block_type = ""
    print(f"interpreter.messages: {interpreter.messages}")
    for chunk in interpreter.chat(user_message, stream=True, display=False):

        # Message
        if "message" in chunk:
            if active_block_type != "message":
                active_block_type = "message"
            history[-1][1] += chunk["message"]
            yield history

        # Code
        if "language" in chunk:
            language = chunk["language"]
        if "code" in chunk:
            if active_block_type != "code":
                active_block_type = "code"
                history[-1][1] += f"\n```{language}\n"
            history[-1][1] += chunk["code"]
            yield history

        # Output
        if "executing" in chunk:
            history[-1][1] += "\n```\n\n```text\n"
            yield history
        if "output" in chunk:
            if chunk["output"] != "KeyboardInterrupt":
                history[-1][1] += chunk["output"] + "\n"
                yield history
        if "end_of_execution" in chunk:
            history[-1][1] = history[-1][1].strip()
            history[-1][1] += "\n```\n"
            yield history
        print(f"history: {history}")


with gr.Blocks() as opencodebot:
    with gr.Tabs() as tabs:
        with gr.TabItem(label="Settings", id="settings"):
            api_base_txt = gr.Textbox(placeholder="API Base", lines=1, container=False,
                                      value="http://192.168.31.12:8000/v1")
            api_key_txt = gr.Textbox(placeholder="API Key", lines=1, container=False, value="sk-123456",
                                     type="password")
            conversation_txt = gr.Textbox(placeholder="Conversation Name", lines=1, container=False,
                                          value="demo_conversation")
            save_btn = gr.Button(value="Save", variant="primary")
            save_btn.click(save_settings,
                           inputs=[api_base_txt, api_key_txt, conversation_txt],
                           outputs=[tabs],
                           api_name="save_settings"
                           )
        with gr.TabItem(label="Chatbot", id="chatbot"):
            chatbot = gr.Chatbot([], show_label=False, elem_id="chatbot", height=750, show_copy_button=True)

            with gr.Row():
                with gr.Column(scale=9):
                    msg_txt = gr.Textbox(
                        show_label=False,
                        placeholder="Enter text and press enter, or upload a file",
                        container=False,
                    )
                with gr.Column(scale=1, min_width=0):
                    # btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])
                    upload_btn = gr.UploadButton("📁", type="file", file_types=["file"], file_count="single")
            with gr.Row():
                clear_btn = gr.ClearButton(value="Clear", components=[chatbot, msg_txt])
                # with gr.Column(scale=5):
                #     clear_btn = gr.ClearButton(value="Clear", components=[chatbot, msg_txt])
                # with gr.Column(scale=5):
                #     stop_btn = gr.Button(value="Stop", variant="stop")

            msg_txt_submit = msg_txt.submit(add_user_msg, [chatbot, msg_txt], [chatbot, msg_txt], queue=True).then(
                chat, chatbot, chatbot
            ).then(lambda: gr.update(interactive=True), None, [msg_txt], queue=True)
            upload_btn.upload(add_file, [chatbot, upload_btn], [chatbot], queue=True).then(
                add_file_bot, chatbot, chatbot
            )
            # stop_btn.click(
            #     None,
            #     None,
            #     None,
            #     cancels=[msg_txt_submit],
            #     api_name=False,
            #     queue=True,
            # )


def random_response(message, history):
    pass


demo = gr.ChatInterface(random_response)

opencodebot.queue()
if __name__ == "__main__":
    opencodebot.launch(debug=True)
