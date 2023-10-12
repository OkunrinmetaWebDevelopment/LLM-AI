from beam import App, Runtime, Image, Output, Volume, VolumeType

import os
import torch
from io import BytesIO
import base64
from transformers import LlamaForCausalLM, LlamaTokenizer
from langchain import PromptTemplate
from langchain.llms import CTransformers
from huggingface_hub import hf_hub_download


# The environment your code will run on
app = App(
    name="StudentChatBot",
    runtime=Runtime(
        cpu=8,
        memory="32Gi",
        gpu="A10G",
        image=Image(
            python_version="python3.10",
            python_packages=[
                "accelerate>=0.16.0,<1",
                "transformers[torch]>=4.28.1,<5",
                "torch>=1.13.1,<2",
                "langchain",
                "sentencepiece",
                "xformers",
                "huggingface_hub",
                "protobuf",
                "ctransformers",
            ],
        ),
    ),
    volumes=[
        Volume(
            name="model_weights",
            path="./model_weights",
        )
    ],
)


my_secret_key = os.environ['HUGGINGFACEHUB_API_TOKEN']

# Cached model
cache_path = "./model_weights"
# Huggingface model
model_id = "TheBloke/Llama-2-7B-Chat-GGML"


# Load the LLM model
def load_models():
    """
    Load the LLM (Language Model) if not already loaded.

    Returns:
        CTransformers: The loaded LLM model.
    """
    model = CTransformers(
            model=hf_hub_download(repo_id=model_id, filename="llama-2-7b-chat.ggmlv3.q2_K.bin",cache_dir=cache_path),
            model_type="llama",
            max_new_tokens=512,
            temperature=0.5
        )
    return model


@app.rest_api(loader=load_models)
def predict(**inputs):
    # Retrieve cached model from loader
    model = inputs["context"]

    # Do something with the model and tokenizer..
    return {}
