import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        self.positives=[]
        self.negatives=[]
        
        file=open(positives,"r")
        for line in file:
            if not line.startswith(";"):
                self.positives.append(line.strip())
        file.close()
        
        file=open(negatives,"r")
        for line in file:
            if not line.startswith(";"):
                self.negatives.append(line.strip())
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text.strip().lower())
        score=0;
        for token in tokens:
            if token in self.positives:
                score+=1
            elif token in self.negatives:
                score-=1
        
        return score
