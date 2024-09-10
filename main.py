from fasthtml.common import *
import pandas as pd
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import sys

app, rt = fast_app(live=True)

# Load the Sentence Transformer model
model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# Load the Annoy index
index = AnnoyIndex(1024, 'euclidean')
index.load('data/office-lines-vec-db.ann')
dialogues_df = pd.read_csv('data/dilogues.csv')

from loguru import logger

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Adding a console handler with the custom format
logger.add(
    sys.stdout,
    format=log_format,
    level="INFO",
    colorize=True
)

# Adding a file handler that also logs to a file
logger.add(
    "file.log",
    format=log_format,
    level="DEBUG",
    rotation="10 MB",  # Automatically rotate the log file after it reaches 10MB
    compression="zip"  # Compress old logs to save space
)


@rt("/")
def get():
    return Titled("Reverse Text App",
                  Form(method="post")(
                      Label("Enter text:", Input(name="query", type="text")),
                      Button("Reverse", type="submit")
                  ),
                  Div(id="result")
                  )


@rt("/")
def post(query: str):
    # Convert the query to an embedding
    logger.info(f"Searching for: {query}")
    query_embedding = model.encode([query])[0]  # Get the first (and only) embedding
    logger.info(f"Query embedding shape: {query_embedding.shape}")
    # Perform similarity search
    nearest_ids = index.get_nns_by_vector(query_embedding, 1)
    nearest_id = nearest_ids[0]
    logger.info(f"Nearest ID: {nearest_id}")
    # Fetch the corresponding dialogue text
    dialogue_text = dialogues_df[dialogues_df['id'] == nearest_id]['line_text'].values[0]
    logger.info(f"Dialogue: {dialogue_text}")
    return Div(
        P(f'Search results for "{query}":'),
        Ul(Li(dialogue_text))
    )


serve()
