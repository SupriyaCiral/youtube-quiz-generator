from transcript import get_transcript
from chunking import split_text
from quiz_generator import generate_quiz

from embeddings import get_embedding
from retrieval import create_index
from retrieval import search_index


video_id = "JxgmHe2NyeY"

print("Fetching Transcript...")

transcript = get_transcript(
    video_id
)

print("Creating Chunks...")

chunks = split_text(
    transcript
)

print("Creating Embeddings...")

vectors = []

for chunk in chunks:

    vectors.append(
        get_embedding(chunk)
    )

print("Creating FAISS Index...")

index = create_index(
    vectors
)

print("Searching Relevant Chunks...")

query = """
Important concepts, definitions,
formulas, examples and interview questions
"""

query_vector = get_embedding(
    query
)

indices = search_index(
    index,
    query_vector,
    k=5
)

print("Retrieved Chunk Indices:")
print(indices)

print(
    "Retrieved Chunks:",
    indices
)

context = ""

for idx in indices:

    context += chunks[idx]
    context += "\n\n"

print("Generating Quiz...")

quiz = generate_quiz(
    context
)

print(quiz)