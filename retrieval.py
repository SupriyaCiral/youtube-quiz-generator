import faiss
import numpy as np


def create_index(vectors):

    dimension = len(vectors[0])

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(vectors)
        .astype("float32")
    )

    return index


def search_index(
    index,
    query_vector,
    k=5
):

    distances, indices = index.search(

        np.array(
            [query_vector]
        ).astype("float32"),

        k
    )

    return indices[0]