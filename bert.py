import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.decomposition import PCA


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_embeddings(texts):
    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt')
        outputs = model(**inputs)
        sentence_embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        embeddings.append(sentence_embedding)
    
    # make into 2D array
    return np.vstack(embeddings)

texts = ["dog", "cat"]
embeddings = get_embeddings(texts)

# should be (n, 768) using BERT
print("Shape before PCA:", embeddings.shape)

pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

# should be (n, number of dims)
print("Shape after PCA:", reduced_embeddings.shape)

#good for graphing 2D, can use with matplot lib.
