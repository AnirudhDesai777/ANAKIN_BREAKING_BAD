# from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# nltk.download('vader_lexicon')




class SentimentClassifier:

    def __init__(self,compassion=100) :
        self.compassion = compassion
        self.decay_factor  = 1
    def feedData(self,data):
        # self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.data = data

    def output(self):
        vader = SentimentIntensityAnalyzer()

        return vader.polarity_scores(self.data)
    
    
    def modify_compassion(self):

        compassion = self.compassion
        sentiment = self.output()
        compassion += sentiment['compound']*10
        
        compassion = min(100,compassion) 
        compassion = max(0,compassion)
        self.compassion = compassion
    
    def get_compassion(self):
        return self.compassion