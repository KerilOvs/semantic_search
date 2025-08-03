import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from .text_processing import clean_text, read_rtf_files


class Vectorizer:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384
        self.paragraph_index = None
        self.documents = []
        self.doc_to_para_map = []

    def normalize_vectors(self, vectors):
        """Normalize vectors for cosine similarity"""
        faiss.normalize_L2(vectors)
        return vectors

    def process_documents(self, folder_path):
        """Process documents and create embeddings"""
        rtf_data = read_rtf_files(folder_path)

        documents = []
        for doc in rtf_data:
            content = doc['content']
            paragraphs = [p for p in content.split('\n') if p.strip()]
            cleaned_paragraphs = [clean_text(p) for p in paragraphs]

            documents.append({
                'file': doc['name'],
                'original': content,
                'paragraphs': paragraphs,
                'cleaned_paragraphs': cleaned_paragraphs
            })

        all_paragraphs = []
        doc_to_para_map = []
        for doc_idx, doc in enumerate(documents):
            for para in doc['cleaned_paragraphs']:
                all_paragraphs.append(para)
                doc_to_para_map.append(doc_idx)

        paragraph_embeddings = self.model.encode(all_paragraphs)
        paragraph_embeddings = self.normalize_vectors(np.array(paragraph_embeddings).astype('float32'))

        self.paragraph_index = faiss.IndexFlatIP(self.dimension)
        self.paragraph_index.add(paragraph_embeddings)
        self.documents = documents
        self.doc_to_para_map = doc_to_para_map

    def save(self, index_path="data/my_index2.faiss", structure_path="data/doc_structure.pkl"):
        """Save the index and document structure"""
        faiss.write_index(self.paragraph_index, index_path)
        with open(structure_path, 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'doc_to_para_map': self.doc_to_para_map
            }, f)

    @classmethod
    def load(cls, index_path="data/my_index2.faiss", structure_path="data/doc_structure.pkl"):
        """Load a pre-trained vectorizer"""
        vectorizer = cls()
        vectorizer.paragraph_index = faiss.read_index(index_path)
        with open(structure_path, 'rb') as f:
            data = pickle.load(f)
            vectorizer.documents = data['documents']
            vectorizer.doc_to_para_map = data['doc_to_para_map']
        return vectorizer
