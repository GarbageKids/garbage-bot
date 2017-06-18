from BayesClassifierCore import BayesClassifierCore
from utilities.databaseWorker import Settings

BayesClassifierCore.process()
BayesClassifierCore.save_core(Settings.get_model_file())