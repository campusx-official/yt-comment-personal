import pytest
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow

# Set your remote tracking URI
mlflow.set_tracking_uri("http://ec2-54-196-109-131.compute-1.amazonaws.com:5000/")

@pytest.mark.parametrize("model_name, stage, holdout_data_path, vectorizer_path", [
    ("my_model", "staging", "data/interim/test_processed.csv", "tfidf_vectorizer.pkl"),  # Replace with your actual paths
])
def test_model_performance(model_name, stage, holdout_data_path, vectorizer_path):
    try:
        # Load the model from MLflow
        client = mlflow.tracking.MlflowClient()
        latest_version_info = client.get_latest_versions(model_name, stages=[stage])
        latest_version = latest_version_info[0].version if latest_version_info else None

        assert latest_version is not None, f"No model found in the '{stage}' stage for '{model_name}'"

        model_uri = f"models:/{model_name}/{latest_version}"
        model = mlflow.pyfunc.load_model(model_uri)

        # Load the vectorizer
        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)

        # Load the holdout test data
        holdout_data = pd.read_csv(holdout_data_path)
        X_holdout_raw = holdout_data.iloc[:, :-1].squeeze()  # Raw text features (assuming text is in the first column)
        y_holdout = holdout_data.iloc[:, -1]  # Labels

        # Handle NaN values in the text data
        X_holdout_raw = X_holdout_raw.fillna("")

        # Apply TF-IDF transformation
        X_holdout_tfidf = vectorizer.transform(X_holdout_raw)
        X_holdout_tfidf_df = pd.DataFrame(X_holdout_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

        # Predict using the model
        y_pred_new = model.predict(X_holdout_tfidf_df)

        # Calculate performance metrics
        accuracy_new = accuracy_score(y_holdout, y_pred_new)
        precision_new = precision_score(y_holdout, y_pred_new, zero_division=1)
        recall_new = recall_score(y_holdout, y_pred_new, zero_division=1)
        f1_new = f1_score(y_holdout, y_pred_new, zero_division=1)

        # Define expected thresholds for the performance metrics
        expected_accuracy = 0.40
        expected_precision = 0.40
        expected_recall = 0.40
        expected_f1 = 0.40

        # Assert that the new model meets the performance thresholds
        assert accuracy_new >= expected_accuracy, f'Accuracy should be at least {expected_accuracy}, got {accuracy_new}'
        assert precision_new >= expected_precision, f'Precision should be at least {expected_precision}, got {precision_new}'
        assert recall_new >= expected_recall, f'Recall should be at least {expected_recall}, got {recall_new}'
        assert f1_new >= expected_f1, f'F1 score should be at least {expected_f1}, got {f1_new}'

        print(f"Performance test passed for model '{model_name}' version {latest_version}")

    except Exception as e:
        pytest.fail(f"Model performance test failed with error: {e}")
