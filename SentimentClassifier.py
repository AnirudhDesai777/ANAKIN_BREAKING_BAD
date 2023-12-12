# from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('distilbert-base-nli-mean-tokens')
from sentence_transformers import SentenceTransformer, util


#nltk.download('vader_lexicon')




class SentimentClassifier:

    def __init__(self,compassion=100) :
        self.compassion = compassion
        self.decay_factor  = 1
        self.killing_factor = 1
        self.input_history = []
        self.sentence_embeddings = []

    def feedData(self,data):
        # self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.data = data
        self.input_history.append(data)
            

    def output(self):
        vader = SentimentIntensityAnalyzer()

        return vader.polarity_scores(self.data)
    
    
    def modify_compassion(self):

        new_embedding = model.encode(self.data)
        self.sentence_embeddings.append(new_embedding)

        embed_values = []
        for i in range(len(self.sentence_embeddings)-1):
            embed_values.append(util.pytorch_cos_sim(self.sentence_embeddings[i], self.sentence_embeddings[-1]).item())
        
        compassion = self.compassion
        sentiment = self.output()
        compassion += sentiment['compound']*69*(1-max(embed_values, default=0))*self.decay_factor
        if(self.decay_factor<=0.5):
            self.decay_factor = 0.5
        else:
            self.decay_factor -= 0.1
        compassion = min(100,compassion) 
        compassion = max(0,compassion)
        self.compassion = compassion
    
    def modify_kill_compassion(self):

        self.compassion -= 4*self.killing_factor
        self.killing_factor +=1
        self.compassion = min(self.compassion,100)
        self.compassion = max(0,self.compassion)
    
    def get_enemies_killed(self):
        return self.killing_factor
    

    def get_compassion(self):
        return self.compassion