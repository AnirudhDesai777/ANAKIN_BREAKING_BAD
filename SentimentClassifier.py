from transformers import pipeline

class SentimentClassifier:

    def feedData(self,data):
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.data = data

    def output(self):
        return self.sentiment_pipeline(self.data)