from beam import App, Runtime, Image, Output, Volume, VolumeType
import aiofiles
from pathlib import Path
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter





app = App(
    name="UploadFile",
    runtime=Runtime(
        image=Image(
            python_version="python3.10",
            python_packages=[
                "aiofiles",
                "langchain",
                "pypdf",
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
DB_FAISS_PATH = "./model_weights/vectorstore"


# Create vector database
@app.run()
def create_vector_db():
    print("vector store")
    data_folder = Path(DB_FAISS_PATH)
    data_folder.mkdir(parents=True, exist_ok=True)
    loader = DirectoryLoader(SOURCE_DIRECTORY,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)


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
        create_vector_db()
    return {}


