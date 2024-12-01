import pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.vectorstores import Neo4jVector
from langchain.graphs import Neo4jGraph

load = load_dotenv()

class OpenAIClient:
    def __init__(self):
        if load:
          self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
          print('OpenAIClient has been instantiated')
        else:
          print('Failed to instantiate OpenAIClient')

    def create_completion(self, prompt, model="gpt-3.5-turbo", max_tokens=50):
        response = self.client.Completion.create( 
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0,
        )
        return response.choices[0].text.strip()


class OpenAIEmbeddingsClient:
    def __init__(self):
        if load:
            self.client = OpenAIEmbeddings(
                api_key=os.getenv("OPENAI_API_KEY"),
                model="text-embedding-3-large",
                dimensions=EMBEDDING_DIMENSIONS
            )
            print('OpenAIEmbeddingsClient has been instantiated')
        else:
            print('Failed to instantiate OpenAIEmbeddingsClient')

    def get_embeddings(self, content):
        """Get embedding for the given content."""
        return self.client.embed_documents(content)



# class PineconeClient:
#     def __init__(self):
#         if load:
#             self.client = pinecone(api_key=os.getenv("PINECONE_API_KEY"))
#             print('PineconeClient has been instantiated')
#         else:
#             print('Failed to instantiate PineconeClient')

#     def create_index(self, index_name):
#         self.index_name = index_name
#         self.client.create_index(
#             name=index_name,
#             dimension=1536,
#             metric='cosine'
#         )
#     def get_index(self, index_name):
#         return self.client.get_index(index_name)
    
#     def delete_index(self, index_name):
#         self.client.delete_index(index_name)

#     def from_documents(self, documents, embeddings, index_name):
#         return PineconeVectorStore.from_documents(
#             documents=documents,
#             embedding=embeddings,
#             index_name=index_name
#         )

#     def retrieve(self, index_name, top_k = 2):
#       vectorstore = self.client.from_existing_index(index_name)
#       return vectorstore.as_retriever(search_kwargs={"k": top_k})


class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )
        print('Neo4jClient has been instantiated')

    def run_query(self, query, parameters=None):
        parameters = parameters or {}
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return [record.data() for record in result]

    def close(self):
        self.driver.close()
