from fasthtml.common import *
import pandas as pd
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

app, rt = fast_app(live=True)

# Load the Sentence Transformer model
model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# Load the Annoy index
index = AnnoyIndex(768, 'euclidean')  # Assuming the embedding dimension is 768
index.load('office-lines.ann')

# Load the dialogues DataFrame
dilogues_df = pd.read_csv('dilogues.csv')

@rt('/', methods=['GET'])
def index():
    return Div(
        Form(
            Input(type='text', name='query', placeholder='Search...'),
            Button('Search', type='submit'),
            method='GET',
            action='/search'
        )
    )

@rt('/search', methods=['GET'])
def search(query):
    # Convert the query to an embedding
    query_embedding = model.encode(query)

    # Perform similarity search
    nearest_id = index.get_nns_by_vector(query_embedding, 1)[0]

    # Fetch the corresponding dialogue text
    dialogue_text = dilogues_df[dilogues_df['id'] == nearest_id]['dialogue'].values[0]

    return Div(
        P(f'Search results for "{query}":'),
        Ul(Li(dialogue_text))
    )