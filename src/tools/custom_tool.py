from crewai.tools import BaseTool
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from markitdown import MarkItDown

load_dotenv()

class DocumentSearchToolInput(BaseModel):
    """Input schema for DocumentSearchTool"""
    query: str = Field(..., description="Query that we want to search our document with.")

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Searching a document based on a given query (aka input)"
    args_schema: type[BaseModel] = DocumentSearchToolInput

    model_config = ConfigDict(extra="allow")

    def __init__(self, docs_folder: str):
        # breakpoint()  # 1️⃣ Pause at start of __init__
        super().__init__()
        self.docs_folder = docs_folder          
        self.embedder    = OpenAIEmbeddings()
        self.index       = self._build_index()

    def _extract_documents(self) -> list[str]:
        loader = MarkItDown()
        texts = []
        for fname in os.listdir(self.docs_folder):
            path = os.path.join(self.docs_folder, fname)
            texts.append(loader.convert(path).text_content)
        return texts

    def _create_chunks(self, texts: list[str]) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = []
        for doc in texts:
            chunks.extend(splitter.split_text(doc))
        return chunks
    
    def _build_index(self) -> FAISS:
        # breakpoint()  # 2️⃣ Pause at top of _build_index
        docs   = self._extract_documents()
        chunks = self._create_chunks(docs)
        faiss_index = FAISS.from_texts(texts=chunks, embedding=self.embedder)
        return faiss_index

    def _run(self, query: str) -> str:
        # breakpoint()  # 3️⃣ Pause at start of _run
        # print("we are in run _run")
        results = self.index.similarity_search(query, k=3)
        # breakpoint()  # 4️⃣ Inspect `results`
        # print("RESULTS:", results)
        # print("TYPES:", [type(item) for item in results])
        passages = [doc.page_content for doc in results]
        # breakpoint()  # 5️⃣ Verify `passages` before joining
        return "\n\n---\n\n".join(passages)
