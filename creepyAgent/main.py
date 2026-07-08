import os 
import re
from langchain_core.documents import Document


# Loop through data and read
def read_file(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()

def get_data():       
    documents = []
    files = os.listdir('./data')
    for f in files:
        content = read_file("./data/" + f)
        metadata = re.search(r"^#\s{1}(.+)\n", content).group(1)
        documents.append(Document(page_content=content, metadata={"source" : metadata}))
    return documents

print(get_data())

# Chunk data 

# Merge chunks into embeddings
# Insert into vector store