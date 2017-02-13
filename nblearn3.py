import sys
import os.path
import re
import json

# Variables
ReviewsObjectList = []
lists = None
ProbabilityObj=None
TokenList = dict()
stopwords = {"a","an","are","are","as","at","be","by","for","from","has","he","in","is","it","its","of","on","that","the"}

class Record:
    def __init_(self):
        self.identifier=None
        self.review=None
        self.ReviewType=None
        self.ReviewClass=None

    def __init__(self, identifier,review,ReviewType,ReviewClass):
        self.identifier=identifier
        self.review=review
        self.ReviewType=ReviewType
        self.ReviewClass=ReviewClass

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
 

# function check if file exists 
def IsFileExists(path):

    if len(path)>0:
        if os.path.isfile(path):
            file = open(path,"r")
            return file
        else:
            return None
    else:
        return None

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def AddToList(word,List):
    if len(word)>0:
        if word in List:
            count = List[word]
            count = count + 1
            List[word]=count
        else:
            List[word]=1


# reading data from txt files
def ReadingDataFromFiles(reviewFilePath,labelFilePath):

    if len(reviewFilePath)>0 and len(labelFilePath)>0:

        #check if review file exist 
        Reviewfile = IsFileExists(reviewFilePath)
        labelfile = IsFileExists(labelFilePath)

        list1=None

        # reading file 1
        if Reviewfile != None:
            with Reviewfile as f:
                list1 = f.readlines()
        else:
            print ("Unable to read {0} file",reviewFilePath)
            return None

        list2=None 

        # reading file 2
        if labelfile !=None:
            with labelfile as f:
                list2 = f.readlines()
        else:
            print ("Unable to read {0} file",labelFilePath)
            return None

        # reading data and creating object
        if len(list1)>0 and len(list2)>0:
            for line1,line2 in zip(list1, list2):
                id1 = line1.rstrip().split(" ",1)[0]
                review = line1.rstrip().split(" ",1)[1]
                id2 = line2.rstrip().split(" ",1)[0]
                type = line2.rstrip().split(" ",2)[1]
                _class = line2.rstrip().split(" ",2)[2]
                
                if id1 == id2:
                    obj = Record(id1,review,type,_class)
                    ReviewsObjectList.append(obj)


def WriteToFile(_class,filename,_List,count,probability):

    if filename!=None:
        if len(_List)>0 and count>0:
            file = open(filename,"a")
            file.write(_class+" "+str(probability)+" "+str(count)+"\n")
            
            for token in _List:
                file.write(token+" "+str(_List[token])+"\n")
            file.close()


def GetTokens(ReviewList):
    
    if len(ReviewList)>0:

       tempdict = dict()

       for obj in ReviewList:
           str = obj.review

           if len(str)>0:
               #tokens = str.split(" ")
               tokens = re.split(r'[^a-zA-Z0-9]',str)

               if len(tokens)>0:
                   for token in tokens:
                       if len(token)>0 and not is_number(token) and (token not in stopwords):
                           # check if token present in dictonary 
                           token = token.lower()
                           if token in tempdict:
                               tempdict[token]= tempdict[token] +1
                           else:
                               tempdict[token]=1
           #break
           #print (len(tempdict))

       return tempdict




def CalculateProbability(_list, totaltokens):
    _List = dict()
    global TokenList

    if len(_list)>0:
        for token in TokenList:
            tokencount = 0

            if token in _list:
                tokencount = _list[token]
            
            prob = (tokencount+1)/(totaltokens+len(TokenList))
            _List[token]=prob
    return _List


def CalculatePriorProbability():

    global ProbabilityObj
    ProbabilityObj=Probability()
    ProbabilityObj.TotalReviews=len(ReviewsObjectList)
    for obj in ReviewsObjectList:

        if obj.ReviewClass.rstrip() == 'positive':
            ProbabilityObj.PositiveReviews += 1
        else:
            if obj.ReviewClass.rstrip() == 'negative':
                ProbabilityObj.NegativeReviews += 1

        if obj.ReviewType == 'deceptive':
            ProbabilityObj.DeceptiveReviews += 1
        else:
            if obj.ReviewType == 'truthful':
                ProbabilityObj.TruthfulReviews +=1

        ProbabilityObj.PriorPositiveProbability=ProbabilityObj.PositiveReviews/ProbabilityObj.TotalReviews
        ProbabilityObj.PriorNegativeProbability=ProbabilityObj.NegativeReviews/ProbabilityObj.TotalReviews
        ProbabilityObj.PriorTruthfulProbability=ProbabilityObj.TruthfulReviews/ProbabilityObj.TotalReviews
        ProbabilityObj.PriorDeceptiveProbability=ProbabilityObj.DeceptiveReviews/ProbabilityObj.TotalReviews


def calculateTokenProbabilities():
    
    global lists

    # Postovie Review Tokens
    lists.PositiveTokenProbabilityList = CalculateProbability(lists.PositiveTokenList,lists.PositiveTokenCount)

    #Negative tokens list
    lists.NegativeTokenProbabilityList  = CalculateProbability(lists.NegativeTokenList,lists.NegativeTokenCount)

    #Truthful tokens list
    lists.DeceptiveTokenProbabilityList = CalculateProbability(lists.DeceptiveTokenList,lists.DeceptiveTokenCount)

    #Deceptive tokens list
    lists.TruthfulTokenProbabilityList = CalculateProbability(lists.TruthfulTokenList,lists.TruthfulTokenCount)


def CalculateTokensProbability(objectlist):
    if len(objectlist)>0:
        
        CalculatePriorProbability()

        global lists
        lists = Lists()
        for obj in objectlist:

            if len(obj.review):
                line = re.split(r'[^a-zA-Z0-9]',obj.review)
                #line  = obj.review.split(" ")
            
                if len(line)>0:

                    for word in line:
                        if len(word)>1 and not is_number(word) and (word not in stopwords):  # Constraint : Word length should be greater than 0
                            if obj.ReviewClass=="positive":
                                AddToList(word.lower(),lists.PositiveTokenList)
                                lists.PositiveTokenCount=lists.PositiveTokenCount+1

                            if obj.ReviewClass=="negative":
                                AddToList(word.lower(),lists.NegativeTokenList)
                                lists.NegativeTokenCount=lists.NegativeTokenCount+1

                            if obj.ReviewType=="truthful":
                                AddToList(word.lower(),lists.TruthfulTokenList)
                                lists.TruthfulTokenCount=lists.TruthfulTokenCount+1

                            if obj.ReviewType=="deceptive":
                                AddToList(word.lower(),lists.DeceptiveTokenList)
                                lists.DeceptiveTokenCount=lists.DeceptiveTokenCount+1

        #print (lists.DeceptiveTokenCount+lists.NegativeTokenCount+lists.PositiveTokenCount+lists.TruthfulTokenCount)
        calculateTokenProbabilities()           

            


def CreateModel():
    global lists
    global ProbabilityObj

    file = open("nbmodel.txt","wb")
    file.close()



    #writing Positive tokes to file
    WriteToFile("positive","nbmodel.txt",lists.PositiveTokenProbabilityList,lists.PositiveTokenCount, ProbabilityObj.PriorPositiveProbability)

    #writing Negative tokes to file
    WriteToFile("negative","nbmodel.txt",lists.NegativeTokenProbabilityList,lists.NegativeTokenCount,ProbabilityObj.PriorNegativeProbability)

    #writing Truthful tokes to file
    WriteToFile("truthful","nbmodel.txt",lists.TruthfulTokenProbabilityList,lists.TruthfulTokenCount,ProbabilityObj.PriorTruthfulProbability)

    #write deceptive tokes to file
    WriteToFile("deceptive","nbmodel.txt",lists.DeceptiveTokenProbabilityList,lists.DeceptiveTokenCount,ProbabilityObj.PriorDeceptiveProbability)


def StoreModel():
    try:
        file = open("nbmodel.txt","wb")
        file.close()

        global ProbabilityObj
        global lists

        model = Model()
        model.Prioprobabilities=ProbabilityObj
        model.TokenProbabilityLists=lists

        _json = json.dumps(model, default=lambda o: o.__dict__)
        
        if len(_json)>0:
            file = open("nbmodel.txt","w")
            file.write(_json)
            file.close()
    except:
        print ("Error in writing model to txt file")
      
##########################################################################################################################################

# reading command line arguments

if len(sys.argv) == 3:
     #reading data from .txt files  - command line
    ReadingDataFromFiles(sys.argv[1],sys.argv[2])
else:
    ReadingDataFromFiles("train-text.txt","train-labels.txt")
   
if len(ReviewsObjectList)>0:
    TokenList = GetTokens(ReviewsObjectList)

    if len(TokenList)>0:
        CalculateTokensProbability(ReviewsObjectList)

    if lists!=None:
        #CreateModel()
        StoreModel()

