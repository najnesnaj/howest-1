from azure.ai.ml import command
from azure.ai.ml import Input, Output
import os

training_component = command(
    name="training",
    display_name="Training an AI model",
    description="Trains an AI model by inputting a lot of training and testing data.",
    inputs={
        "training_folder": Input(type="uri_folder"),
        "testing_folder": Input(type="uri_folder"),
        "epochs": Input(type="number") # The percentage of the data to use as testing data, always a positive value
    },
    outputs={
        "output_model": Output(type="uri_file", mode="rw_mount"),
    },
    # The source folder of the component
    code=os.path.join("components", "training", "code"),
    command="""python train.py \
            --training_folder ${{inputs.training_folder}} \
            --testing_folder ${{inputs.testing_folder}} \
            --output_folder ${{outputs.output_model}} \
            --epochs ${{inputs.epochs}} \
            """,
    environment=f"aml-training@latest",
)