from knowledge_agent import collect_articles
from clean_new_data import clean_articles
from chunk_new_data import create_chunks
from update_vector_db import update_index


def update_pipeline():

    print("Starting knowledge update...")

    collect_articles()

    clean_articles()

    create_chunks()

    update_index()

    print("Knowledge base updated successfully")


if __name__ == "__main__":

    update_pipeline()