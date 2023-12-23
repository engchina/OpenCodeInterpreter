import contextlib
import io

import gradio as gr

import opencodeinterpreter as interpreter

interpreter.api_base = "http://192.168.31.15:8000/v1"
interpreter.api_key = "fake_key"
interpreter.auto_run = True
interpreter.local = False


def chat_with_interpreter(message, history, openai_api_key):
    # interpreter.api_key = openai_api_key
    if message == 'reset':
        interpreter.reset()
    # Redirect stdout to capture the streamed output
    new_stdout = io.StringIO()
    with contextlib.redirect_stdout(new_stdout):
        interpreter.chat(message)
    output = new_stdout.getvalue()

    # Return this output so Gradio's ChatInterface can display it
    return output


openai_api_key = gr.Textbox(label='OpenAI API Key', interactive=True)
additional_inputs = [openai_api_key]
examples = [["what is 2+2?"],
            ["Can you solve for x: 10x -65=0?"],
            ["What are top 10 headlines from BBC from last week?"]
            ],

demo = gr.ChatInterface(fn=chat_with_interpreter,
                        title="Open-Interpreter Gradio ChatInterface",
                        description="Open Interpreter lets LLMs run code (Python, Javascript, Shell, and more) locally",
                        clear_btn=None,
                        retry_btn=None,
                        undo_btn=None,
                        # examples=examples,
                        additional_inputs=additional_inputs,
                        additional_inputs_accordion_name="OpenAI API Key",
                        ).queue()
demo.launch(debug=True)
