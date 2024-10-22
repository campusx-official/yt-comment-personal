# src/model/model_evaluation.py

import numpy as np
import pandas as pd
import pickle
import logging
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# logging configuration
logger = logging.getLogger('model_evaluation')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('model_evaluation_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        df.fillna('', inplace=True)  # Fill any NaN values
        logger.debug('Data loaded and NaNs filled from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise


def load_model(model_path: str):
    """Load the trained model."""
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logger.debug('Model loaded from %s', model_path)
        return model
    except FileNotFoundError:
        logger.error('Model file not found: %s', model_path)
        raise
    except Exception as e:
        logger.error('Error loading model: %s', e)
        raise


def load_vectorizer(vectorizer_path: str) -> TfidfVectorizer:
    """Load the saved TF-IDF vectorizer."""
    try:
        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)
        logger.debug('TF-IDF vectorizer loaded from %s', vectorizer_path)
        return vectorizer
    except FileNotFoundError:
        logger.error('Vectorizer file not found: %s', vectorizer_path)
        raise
    except Exception as e:
        logger.error('Error loading vectorizer: %s', e)
        raise


def evaluate_model(model, X: np.ndarray, y: np.ndarray, dataset_name: str):
    """Evaluate the model and print the classification report."""
    try:
        y_pred = model.predict(X)
        report = classification_report(y, y_pred, digits=4)
        logger.debug(f"Classification report for {dataset_name}:\n{report}")
        print(f"Classification report for {dataset_name}:\n{report}")
    except Exception as e:
        logger.error(f'Error during model evaluation for {dataset_name}: {e}')
        raise


def get_root_directory() -> str:
    """Get the root directory (two levels up from this script's location)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../../'))


def main():
    try:
        # Get root directory
        root_dir = get_root_directory()

        # Load the model and vectorizer from the root directory
        model = load_model(os.path.join(root_dir, 'lgbm_model.pkl'))
        vectorizer = load_vectorizer(os.path.join(root_dir, 'tfidf_vectorizer.pkl'))

        # Load the training data and test data from the interim directory
        train_data = load_data(os.path.join(root_dir, 'data/interim/train_processed.csv'))
        test_data = load_data(os.path.join(root_dir, 'data/interim/test_processed.csv'))

        # Extract features using the loaded TF-IDF vectorizer
        X_train_tfidf = vectorizer.transform(train_data['clean_comment'].values)
        y_train = train_data['category'].values

        X_test_tfidf = vectorizer.transform(test_data['clean_comment'].values)
        y_test = test_data['category'].values

        # Evaluate on training data
        evaluate_model(model, X_train_tfidf, y_train, "Training Data")

        # Evaluate on test data
        evaluate_model(model, X_test_tfidf, y_test, "Test Data")

    except Exception as e:
        logger.error(f"Failed to complete model evaluation: {e}")
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
