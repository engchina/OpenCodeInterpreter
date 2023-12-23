import gradio as gr
import numpy as np


def snap(image):
    # return np.flipud(image)
    return np.rot90(image, 4)


# demo = gr.Interface(snap, gr.Image(source="webcam", streaming=True), "image", live=True)
demo = gr.Interface(snap, gr.Image(source="webcam", streaming=True), "image")

if __name__ == "__main__":
    demo.launch()
