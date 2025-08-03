import numpy as np


class Searcher:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def find_similar_paragraphs(self, query_text, top_k=5):
        """Find similar paragraphs to the query"""
        query_vector = self.vectorizer.model.encode([query_text])
        query_vector = self.vectorizer.normalize_vectors(np.array(query_vector).astype('float32'))

        D, I = self.vectorizer.paragraph_index.search(query_vector, top_k)

        results = []
        for idx, score in zip(I[0], D[0]):
            doc_idx = self.vectorizer.doc_to_para_map[idx]
            original_para = self.vectorizer.documents[doc_idx]['paragraphs'][idx % len(self.vectorizer.documents[doc_idx]['paragraphs'])]

            results.append({
                'score': float(score),
                'document': self.vectorizer.documents[doc_idx]['file'],
                'paragraph': original_para,
                'document_index': doc_idx,
                'paragraph_index': idx
            })

        return results
