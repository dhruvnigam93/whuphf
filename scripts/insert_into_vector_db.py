import numpy as np
import pandas as pd
from annoy import AnnoyIndex


def prepare_annoy_index(dim: int, n_trees: int = 10) -> AnnoyIndex:
    """Creates an Annoy index for storing vectors."""
    index = AnnoyIndex(dim, 'euclidean')
    return index


def serialize_to_annoy_format(embedding_df):
    """Converts DataFrame embeddings to numpy format required by Annoy."""
    embeddings = np.vstack(embedding_df["context_embeddings"].values).astype('float32')
    ids = embedding_df["id"].values.astype('int64')
    return ids, embeddings


# Load data
embedding_df = pd.read_pickle("../data/the-office-lines-embeddings.pkl")

# Annoy setup
dim = len(embedding_df["context_embeddings"].iloc[0])  # assuming all embeddings have the same dimension
index = prepare_annoy_index(dim)

# Add vectors to the Annoy index
ids, embeddings = serialize_to_annoy_format(embedding_df)
for i, embedding in zip(ids, embeddings):
    index.add_item(i, embedding)

# Build the Annoy index
index.build(10)  # 10 trees

# Save the index to disk
index.save("../data/office-lines-vec-db.ann")
