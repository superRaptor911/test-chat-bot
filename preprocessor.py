from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from utility import pickle_object
import os


def load_data():
    txt_loader = DirectoryLoader("./data/", glob="**/*.txt")
    code_loader = DirectoryLoader("./data/", glob="**/*.py")

    loaders = [txt_loader, code_loader]
    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    print(f"Total number of documents: {len(documents)}")
    return documents


def split_data(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(documents)
    return documents


if __name__ == "__main__":
    documents = load_data()
    documents = split_data(documents)

    if not os.path.exists("output"):
        os.mkdir("output")
    pickle_object(documents, "output/documents.bin")
    print("saved to output/documents.bin")
