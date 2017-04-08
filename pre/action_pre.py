import pandas as pd
import numpy as np
from datetime import datetime
import time

action_path_1 = './JData_Action_201602.csv'
action_path_2 = './JData_Action_201603.csv'
action_path_3 = './JData_Action_201604.csv'


action_path_out = './Action_pre.csv'

data_1 = pd.read_csv(action_path_1, index_col=None, encoding='gbk')
data_2 = pd.read_csv(action_path_2, index_col=None, encoding='gbk')
data_3 = pd.read_csv(action_path_3, index_col=None, encoding='gbk')

print('read')

data = pd.concat([data_1,data_2,data_3])
del data_1,data_2,data_3
print(data)
print('concat')

'''
#def parseDateTime(input, format="%Y-%m-%d"):
def parseDateTime(input, format="%Y-%m-%d %H:%M:%S"):
	return datetime.fromtimestamp(time.mktime(time.strptime(input,format)))
data['time']=data['time'].map(parseDateTime)
'''
data = data.sort_index(by='time',ascending=True)
#print(data_1)
print('sort')

data['brand']= data['brand'].map(lambda x : 'BD'+str(x))
data['cate']= data['cate'].map(lambda x : 'C'+str(x))
data['type']= data['type'].map(lambda x : 'T'+str(x))
def model_str(x):
	if x!=np.nan:
		return 'T'+str(int(x))
	else:
		return np.nan
data['model_id']= data['model_id'].map(lambda x : 'MD'+str(int(x)), na_action='ignore')
'''
#def parseDateTime(input, format="%Y-%m-%d"):
def DateTime2String(dt):
	return dt.isoformat()
data['time']=data['time'].map(DateTime2String)
'''
print(data)

data.to_csv(action_path_out, index=False)
print('Done')