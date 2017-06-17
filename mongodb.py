# -*- coding: utf-8 -*-
from pymongo import MongoClient

# MONGO CFG
MONGO_SERVER = '172.16.234.92'
MONGO_PORT   = 27017
MONGO_DB     = 'erp'

# COLLECTIONS
COL_BASE    = 'bases'
COL_CONTRA  = 'contracts'
COL_CRM     = 'crms'
COL_FINANCE = 'finances'
COL_HRM     = 'hrms'
COL_SCM     = 'scms'

collections = ['bases', 'contracts', 'crms', 'finances', 'hrms', 'scms']

# CONNECT MONGO
db = MongoClient(MONGO_SERVER, MONGO_PORT)[MONGO_DB]

# FUNCTION
def fetchAllData():
	data = []
	for collection_name in collections:
		for row in db[collection_name].find():
			data.append((row['q'], collection_name[:-1].upper()))
	return data;


total = fetchAllData()
print(type(total))
print(len(total))