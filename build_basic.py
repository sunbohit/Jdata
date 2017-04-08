import pandas as pd
import numpy as np
import time 

now = time.time()

user_path = './pre/User_pre.csv'
comment_path = './pre/Comment_pre.csv'
product_path = './pre/Product_pre.csv'
action_path = './pre/Action_pre.csv'

#action_data = pd.read_csv(action_path, index_col=None)
#action_data.to_pickle('./Action_pre.pkl')

action_data = pd.read_pickle('./Action_pre.pkl')
print(action_data) #user_id,sku_id,time,model_id,type,cate,brand

#action_data = pd.read_csv('./simple_Action_pre.csv', index_col=None)

basic_data = action_data.loc[:,['user_id','sku_id']]
del action_data
basic_data = basic_data.drop_duplicates()
print(basic_data)

product_data = pd.read_csv(product_path, index_col=None)
product_set = set(product_data['sku_id'])

def in_product(in_str):
	if in_str in product_set:
		return in_str
	else:
		return None
basic_data['sku_id'] = basic_data['sku_id'].map(in_product)
basic_data = basic_data.dropna()
print(basic_data)

user_data = pd.read_csv(user_path, index_col=None)
user_set = set(user_data['user_id'])

def in_user(in_str):
	if in_str in user_set:
		return in_str
	else:
		return None
basic_data['user_id'] = basic_data['user_id'].map(in_user)
basic_data = basic_data.dropna()
print(basic_data)
'''
basic_data = pd.merge(basic_data,product_data,on=['sku_id'],how='left')
del product_data
print(basic_data)


basic_data = pd.merge(basic_data,user_data,on=['user_id'],how='left')
del user_data
print(basic_data)
'''
basic_data.to_pickle('./basic_data.pkl')

cost_time = time.time()-now
print("end ......",'\n',"cost time:",cost_time,"(s)......")