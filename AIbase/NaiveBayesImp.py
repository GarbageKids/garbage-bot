from nltk import NaiveBayesClassifier as nbc
from nltk.tokenize import word_tokenize
from itertools import chain

training_data = [('I love this sandwich.', 'pos'),
('This is an amazing place!', 'pos'),
('I feel very good about these beers.', 'pos'),
('This is my best work.', 'pos'),
("What an awesome view", 'pos'),
('I do not like this restaurant', 'neg'),
('I am tired of this stuff.', 'neg'),
("I can't deal with this", 'neg'),
('He is my sworn enemy!', 'neg'),
('My boss is horrible.', 'neg')]

vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in training_data]))

feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary},tag) for sentence, tag in training_data]
for feature in feature_set:
    print(feature)

classifier = nbc.train(feature_set)

test_sentence = "This is band is horrible !"
featurized_test_sentence =  {i:(i in word_tokenize(test_sentence.lower())) for i in vocabulary}
print(featurized_test_sentence)

print("test_sent:",test_sentence)
print("tag:",classifier.classify(featurized_test_sentence))