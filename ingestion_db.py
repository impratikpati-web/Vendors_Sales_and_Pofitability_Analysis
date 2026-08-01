import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Logging Configuration
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Database Connection
engine = create_engine('sqlite:///inventory.db')


def ingest_db(chunk, table_name, engine, first_chunk):
    """
    Ingest dataframe chunk into database
    """

    if_exists_type = 'replace' if first_chunk else 'append'

    chunk.to_sql(
        name=table_name,
        con=engine,
        if_exists=if_exists_type,
        index=False
    )


def load_raw_data():
    """
    Load CSV files in chunks and ingest into database
    """

    start = time.time()

    data_path = 'data'

    for file in os.listdir(data_path):

        if file.endswith('.csv'):

            file_path = os.path.join(data_path, file)
            table_name = file[:-4]

            logging.info(f"Started ingesting: {file}")

            try:

                # Read CSV in chunks
                chunk_iter = pd.read_csv(
                    file_path,
                    chunksize=50000   # Adjust based on RAM
                )

                first_chunk = True

                for chunk in chunk_iter:

                    ingest_db(
                        chunk,
                        table_name,
                        engine,
                        first_chunk
                    )

                    first_chunk = False

                    logging.info(
                        f"{len(chunk)} rows ingested into {table_name}"
                    )

                logging.info(f"Completed ingesting: {file}")

            except Exception as e:

                logging.error(
                    f"Error while processing {file}: {str(e)}"
                )

    end = time.time()

    total_time = (end - start) / 60

    logging.info("------ INGESTION COMPLETE ------")
    logging.info(f"Total time taken: {total_time:.2f} Minutes")


if __name__ == '__main__':
    load_raw_data()