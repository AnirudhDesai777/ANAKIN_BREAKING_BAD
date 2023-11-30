# from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#nltk.download('vader_lexicon')




class SentimentClassifier:

    def __init__(self,compassion=100) :
        self.compassion = compassion
        self.decay_factor  = 1
        self.killing_factor = 1
    def feedData(self,data):
        # self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.data = data

    def output(self):
        vader = SentimentIntensityAnalyzer()

        return vader.polarity_scores(self.data)
    
    
    def modify_compassion(self):

        compassion = self.compassion
        sentiment = self.output()
        compassion += sentiment['compound']*69*self.decay_factor
        if(self.decay_factor<=0.2):
            self.decay_factor = 0.2
        else:
            self.decay_factor -= 0.1
        compassion = min(100,compassion) 
        compassion = max(0,compassion)
        self.compassion = compassion
    
    def modify_kill_compassion(self):

        self.compassion -= 1.5*self.killing_factor
        self.killing_factor +=1
        self.compassion = min(self.compassion,100)
        self.compassion = max(0,self.compassion)
    
    def get_enemies_killed(self):
        return self.killing_factor
    
    
    def get_compassion(self):
        return self.compassion