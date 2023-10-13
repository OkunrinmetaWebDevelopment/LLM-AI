from beam import App, Runtime, Image, Output, Volume, VolumeType
import aiofiles
from pathlib import Path
import os





app = App(
    name="UploadFile",
    runtime=Runtime(
        image=Image(
            python_version="python3.10",
            python_packages=[
                "aiofiles",
                "aiosmtplib",
                "anyio",
                "passlib",
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


SOURCE_DIRECTORY = "./model_weights/data"
@app.rest_api(keep_warm_seconds = 100, outputs = [Output(path="./model_weights/data")])
def upload_file(files: list):
    filenames = []
    for file in files:
        # Create the file path
        data_folder = Path(SOURCE_DIRECTORY)
        data_folder.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        file_name = os.path.basename(file)
        destination_file_path = data_folder / file_name
        with open(destination_file_path, 'wb') as out_file:
            with open(file, 'rb') as in_file:
                out_file.write(in_file.read())
        filenames.append(file_name)

    return {}



