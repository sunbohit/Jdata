import pandas as pd
import numpy as np
from datetime import datetime
import time

user_path = './JData_User.csv'
user_path_out = './User_pre.csv'
data = pd.read_csv(user_path, index_col='user_id', encoding='gbk')


print(data)
#
print(set(data.age))
'''
{nan, '36-45岁', '56岁以上', '46-55岁', '15岁以下', '-1', '16-25岁', '26-35岁'}
'''

'''
-1 -1
15岁以下 0
16-25岁 1
26-35岁 2
36-45岁 3
46-55岁 4
56岁以上 5
'''
age_dict={'36-45岁':3, '56岁以上':'5', '16-25岁':1, '46-55岁':4, '-1':np.nan, '15岁以下':0, '26-35岁':2}
for key,value in age_dict.items():
	#print(key) 
	data['age'][data.age==key] = value

print(set(data['sex']))
sex_dict={0:'M', 1:'F', 2:np.nan}
for key,value in sex_dict.items():
	#print(key) 
	data['sex'][data.sex==key] = value

#print(data)

#
print(data['user_reg_tm'])


'''
def parseDateTime(input, format="%Y-%m-%d"):
#def parseDateTime(input, format="%Y-%m-%d %H:%M:%S"):
	return datetime.fromtimestamp(time.mktime(time.strptime(input,format)))

data['user_reg_tm']=data['user_reg_tm'].map(parseDateTime)
'''
print(data['user_reg_tm'])

print(set(data['user_lv_cd']))
'''
{1, 2, 3, 4, 5}
'''

print(data['user_lv_cd'])
print(data)

data.to_csv(user_path_out)