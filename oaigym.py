from sentence_transformers import SentenceTransformer
model = SentenceTransformer('distilbert-base-nli-mean-tokens')

sentences = ['you are a bad','you are a miserable person. You are a disgrace to your father. You should consider killing everyone and yourself too','you are bad bad bad bad bad bad']
sentence_embeddings = model.encode(sentences)
print(len(sentence_embeddings))


from sentence_transformers import SentenceTransformer, util
print(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1]).item())
print(util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[2])[0])
print(util.pytorch_cos_sim(sentence_embeddings[1], sentence_embeddings[2])[0])

new_text = 'anirudh is awesome'

new_sentence_embeddings = model.encode(new_text)
print(len(sentence_embeddings))