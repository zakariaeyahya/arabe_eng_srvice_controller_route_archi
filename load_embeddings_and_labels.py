import pandas as pd
import logging

logger = logging.getLogger(__name__)

combined_embeddings_file = r'D:\bureau\stage\exe 2\second try\combined_embeddings_all-mpnet-base-v2.csv'
excel_file_path = r'd:\bureau\stage\exe 2\second try\classeur1.ods'

def load_embeddings_and_labels():
    try:
        logger.info(f"Attempting to load embeddings from {combined_embeddings_file}")
        df_embeddings = pd.read_csv(combined_embeddings_file)
        logger.info(f"Successfully loaded embeddings. Shape: {df_embeddings.shape}")

        logger.info(f"Attempting to load labels from {excel_file_path}")
        df_labels = pd.read_excel(excel_file_path, engine='odf')
        logger.info(f"Successfully loaded labels. Shape: {df_labels.shape}")

        embeddings = df_embeddings.values
        labels = df_labels['preferredLabel'].values
        return embeddings, labels
    except Exception as e:
        logger.error(f"Error loading embeddings or Excel file: {str(e)}")
        raise RuntimeError(f"Error loading embeddings or Excel file: {str(e)}")