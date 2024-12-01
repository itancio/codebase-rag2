from langchain_experimental.text_splitter import SemanticChunker

from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter
)
import json
from langchain.schema import Document
from app.clients import OpenAIEmbeddingsClient
from app.language_support import LanguageSupport


class BaseChunkingStrategy:
    """Base class with shared chunk size, overlap, and a default splitter."""
    chunk_size = 1024
    chunk_overlap = 200
    name = "BaseChunkingStrategy"

    @classmethod
    def splitter(cls):
        """Lazily initialize and return the default splitter."""
        return CharacterTextSplitter(
            chunk_size=cls.chunk_size,
            chunk_overlap=cls.chunk_overlap,
            add_start_index=True
        )

    @classmethod
    def create_documents(cls, doc):
        content = doc.page_content
        metadata = doc.metadata
        """Split text using the default splitter."""
        return cls.splitter().create_documents(
            [content], 
            [metadata]
        )


class SemanticChunkingStrategy(BaseChunkingStrategy):
    """Semantic chunking strategy with a shared splitter."""
    def __init__(self):
        self.name = "SemanticChunkingStrategy"
        self.splitter = SemanticChunker(
            OpenAIEmbeddingsClient(),
            breakpoint_threshold_type="percentile",
            add_start_index=True
        )

    def create_documents(self, doc):
        content = doc.page_content
        metadata = doc.metadata
        try:
            return self.splitter.create_documents(
                [content], 
                [metadata]
            )
        except Exception:
            # Fallback to default splitter
            return BaseChunkingStrategy.create_documents(doc)


class CodeChunkingStrategy(BaseChunkingStrategy):
    """Code chunking strategy with instance-specific language."""
    def __init__(self, language=None):
        self.name = "CodeChunkingStrategy"
        self.language = language
        if language:
            self.splitter = RecursiveCharacterTextSplitter.from_language(
                language=self.language,
                chunk_size=BaseChunkingStrategy.chunk_size,
                chunk_overlap=BaseChunkingStrategy.chunk_overlap,
                add_start_index=True
            )
        else:
            self.splitter = BaseChunkingStrategy.splitter()

    def create_documents(self, doc):
        content = doc.page_content
        metadata = doc.metadata
        try:
            return self.splitter.create_documents(
                [content], 
                [metadata]
            )
        except Exception:
            # Fallback to default splitter
            return BaseChunkingStrategy.create_documents(doc)


class IpynbChunkingStrategy(BaseChunkingStrategy):
    """Chunking strategy for Python Notebook."""
    
    def __init__(self):
        self.name = "IpynbChunkingStrategy"
        self.splitter = CodeChunkingStrategy(language="python")

    def preprocess(self, doc):
        metadata = doc.metadata
        content = doc.page_content
        json_data = json.loads(content)
        cells = json_data.get('cells', [])

        # Separate code and markdown cells
        code_cells = ['\n'.join(cell['source']) for cell in cells if cell['cell_type'] == 'code']
        markdown_cells = ['\n'.join(cell['source']) for cell in cells if cell['cell_type'] == 'markdown']

        return {
            "code": Document(page_content='\n'.join(code_cells), metadata=metadata),
            "markdown": Document(page_content='\n'.join(markdown_cells), metadata=metadata)
        }

    def create_documents(self, doc):
        processed_docs = self.preprocess(doc)
        code_doc = processed_docs['code']
        markdown_doc = processed_docs['markdown']

        try:
            # Split code using CodeChunkingStrategy
            code_chunks = self.splitter.create_documents(code_doc)
            # Use BaseChunkingStrategy for markdown
            markdown_chunks = CodeChunkingStrategy(language="markdown").create_documents(markdown_doc)
            return code_chunks + markdown_chunks
        except Exception:
            # Fallback to default splitter
            return BaseChunkingStrategy.create_documents(doc)


class ChunkingManager:
    """Manager to select appropriate chunking strategy."""
    def __init__(self):
        self.code_splitter = lambda lang: CodeChunkingStrategy(lang)
        self.ipynb_splitter = IpynbChunkingStrategy()
        self.semantic_splitter = SemanticChunkingStrategy()

    def get_splitter(self, language):
        """Return the appropriate splitter based on file type."""
        if language == "ipynb":
            splitter = self.ipynb_splitter
            print(f"Splitter adopted: {splitter.name}")
            return splitter
        elif language:
            splitter = self.code_splitter(language)
            print(f"Splitter adopted: {splitter.name} for language {language}")
            return splitter
        else:
            splitter = self.semantic_splitter
            print(f"Splitter adopted: {splitter.name} (default for unsupported file type)")
            return splitter

    def create_documents(self, doc):
        metadata = doc.metadata
        filename = metadata.get('filename')
        extension = '.' + filename.split('.')[-1]
        if LanguageSupport.is_supported_language(extension):
            lang = LanguageSupport.get_language(extension)
        else:
            lang = None
        print('language: ', lang)
        """Create documents using the appropriate splitter."""
        splitter = self.get_splitter(lang)
        return splitter.create_documents(doc)
