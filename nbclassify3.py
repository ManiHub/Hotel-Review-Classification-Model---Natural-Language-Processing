import sys
import json
import os.path
import re


class Result:
    def __init__(self):
        self.ID=0
        self.PositeProbability=0
        self.NegativeProbability=0
        self.TruthfulProbability=0
        self.DeceptiveProbability=0
        self.ReviewTypee=None
        self.ReviewClass=None

class Line:
    def __init__(self, **kwargs):
        self.Tokens=dict()
        self.ID=None
        self.Line = None

class Review:
    def __init__(self, **kwargs):
        self.count=0
        self.Lines=[]

class Lists:
    def __init__(self):
        self.PositiveTokenList=dict()
        self.PositiveTokenProbabilityList=dict()
        self.NegativeTokenList=dict()
        self.NegativeTokenProbabilityList=dict()
        self.TruthfulTokenList=dict()
        self.TruthfulTokenProbabilityList=dict()
        self.DeceptiveTokenList=dict()
        self.DeceptiveTokenProbabilityList=dict()
        self.PositiveTokenCount=0
        self.PositiveTokenCount=0
        self.NegativeTokenCount=0
        self.TruthfulTokenCount=0
        self.DeceptiveTokenCount=0

class Probability:
    def __init__(self):
        self.TotalReviews=0
        self.PositiveReviews=0
        self.NegativeReviews=0
        self.TruthfulReviews=0
        self.DeceptiveReviews=0
        self.PriorPositiveProbability=0
        self.PriorNegativeProbability=0
        self.PriorTruthfulProbability=0
        self.PriorDeceptiveProbability =0

class Model:
    def __init__(self):
        self.Prioprobabilities=Probability()
        self.TokenProbabilityLists=Lists()




def ReadModel():
    try:
        file = open("nbmodel.txt","r")
        _json = file.readlines()

        if len(_json)>0:
            model = Model()
            model = json.loads(_json[0],Model)

            return model
    except:
        return None


def IsFileExists(path):

    if len(path)>0:
        if os.path.isfile(path):
            file = open(path,"r")
            return file
        else:
            return None
    else:
        return None


def AddLineToCollection(line):
    global _Review

    try:

        _Line = Line()
        _Line.ID=line.split(" ",1)[0]
        _Line.Line=line.split(" ",1)[1]

        tokens = re.split(r'[^a-zA-Z0-9]',_Line.Line)
        if len(tokens)>0:
            for token in tokens:
                if len(token)>0:
                    token = token.lower()
                    if token in _Line.Tokens:
                        count = _Line.Tokens[token]
                        count = count+1
                        _Line.Tokens[token]=count
                    else:
                        _Line.Tokens[token]=1

        _Review.Lines.append(_Line)
        _Review.count = _Review.count+1
    except Exception as e:
        x=10

        

def ReadTestDataFile(filepath):
    try:
        if len(filepath)>0:
            file = IsFileExists(filepath)

            if file != None:
                with file as f:
                    data = f.readlines()

                    if len(data)>0:

                        for line in data:
                            line = line.rstrip()
                            AddLineToCollection(line)
            
    except :
        return None


def CalculateTokenProbability():
    global _Review
    global model
    global result

    try:
        if _Review.count>0:

            _Probabilities = model["Prioprobabilities"]
            _tokens = model["TokenProbabilityLists"]
            _positiveTokesn = _tokens["PositiveTokenProbabilityList"]
            _negativeTokesn = _tokens["NegativeTokenProbabilityList"]
            _truthfulTokesn = _tokens["TruthfulTokenProbabilityList"]
            _deceptiveTokesn = _tokens["DeceptiveTokenProbabilityList"]

            for review in _Review.Lines:
                if len(review.Tokens)>0:
                    _result = Result()
                    _result.ID=review.ID
                    
                    _posprob = _Probabilities["PriorPositiveProbability"]
                    _negprob = _Probabilities["PriorNegativeProbability"]
                    _truprob = _Probabilities["PriorTruthfulProbability"]
                    _decprob = _Probabilities["PriorDeceptiveProbability"]

                    for token in review.Tokens:
                        if token in _positiveTokesn:
                            _posprob = _posprob  * _positiveTokesn[token]

                        if token in _negativeTokesn:
                            _negprob = _negprob  * _negativeTokesn[token]

                        if token in _truthfulTokesn:
                            _truprob = _truprob * _truthfulTokesn[token]

                        if token in _deceptiveTokesn:
                            _decprob = _decprob * _deceptiveTokesn[token]

                    _result.PositeProbability=_posprob
                    _result.NegativeProbability=_negprob
                    _result.DeceptiveProbability=_decprob
                    _result.TruthfulProbability=_truprob

                    if _posprob > _negprob:
                        _result.ReviewTypee="positive"
                    else:
                        _result.ReviewTypee="negative"

                    if _decprob > _truprob:
                        _result.ReviewClass="deceptive"
                    else:
                        _result.ReviewClass="truthful"

                    result.append(_result)

    except Exception as e:
        x=10


def WriteResultsToFile():
    if len(result)>0:
        try:
            file = open("nboutput.txt","w+")
            for res in result:
                file.write(str(res.ID+" "+res.ReviewClass+" "+res.ReviewTypee+"\n"))
            file.close()
        except Exception as e:
            x=10


#variables 
_Review = Review()
result = []
model = Model()
filepath=""

if len(sys.argv)==2:
    filepath = sys.argv[1]
else:
    filepath = "train-text.txt"
# reading JSON
model = ReadModel()
    
if model!=None:
    ReadTestDataFile(filepath)
    CalculateTokenProbability()
    WriteResultsToFile()
















































































































































































