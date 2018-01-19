# -*- coding: utf-8 -*-
from bayes import Bayes
import sys

if __name__ == "__main__":
    
    # use as python news_bayes.py feature_file model_file
    
    bays = Bayes()
    
    feature_file = sys.argv[1]
    model_file = sys.argv[2]
    bays.forecast(feature_file,model_file)
