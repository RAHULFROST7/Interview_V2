from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
from math import ceil

class Nlp_trans_SimCalc:
    def __init__(self, model_name='bert-base-nli-mean-tokens'):
        self.model = SentenceTransformer(model_name)

    def calculate_similarity(self, sentences_list, sentence):
        sentence_embeddings = self.model.encode([sentence])
        sentences_embeddings = self.model.encode(sentences_list)

        similarity_scores = []

        cos_similarities = util.pytorch_cos_sim(sentence_embeddings, sentences_embeddings).squeeze()
        cosine_similarity_scores = [ceil(similarity.item() * 100) if similarity.item() > 0 else 0 for similarity in cos_similarities]

        euclidean_distances = [euclidean(sentence_embeddings[0], embedding) for embedding in sentences_embeddings]
        euclidean_similarity_scores = [self.calculate_similarity_score(abs(distance)) for distance in euclidean_distances]

        for cosine_score, euclidean_score in zip(cosine_similarity_scores, euclidean_similarity_scores):
            similarity_scores.append(ceil(0.15 * cosine_score + 0.70 * euclidean_score + 0.15 * cosine_score))

        return max(similarity_scores)

    @staticmethod
    def calculate_similarity_score(distance):
        min_distance = 0.0  # Minimum possible distance
        max_distance = 10.0  # Maximum possible distance

        normalized_distance = (distance - min_distance) / (max_distance - min_distance)
        similarity = 100 * (1 - normalized_distance) * 3.3

        return similarity if 0 < similarity < 100 else 100 if similarity > 100 else 0