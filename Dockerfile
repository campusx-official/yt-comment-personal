FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgomp1

COPY flask_app/ /app/

COPY tfidf_vectorizer.pkl /app/tfidf_vectorizer.pkl

RUN pip install -r requirements.txt

RUN python -m nltk.downloader stopwords wordnet

EXPOSE 5000

CMD ["python", "app.py"]