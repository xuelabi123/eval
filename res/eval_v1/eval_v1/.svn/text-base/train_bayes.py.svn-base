# -*- coding: utf-8 -*-
from bayes import Bayes
import sys

if __name__ == "__main__":
    
    #use as python buid_bayes.py training_file feature_file model_file test_file
    
    bays = Bayes()
    
    training_file = sys.argv[1]
    feature_file = sys.argv[2]
    model_file = sys.argv[3]
    test_file = sys.argv[4]
    
    bays.get_train_txt(training_file)
    bays.get_test_txt(test_file,limit=120)
    bays.feature_words(training_file,feature_file)
    bays.train_bayes(training_file,feature_file,model_file)
#    bays.predict(feature_file,model_file,test_file)

