import pandas as pd
import numpy as np
import time
import datetime as dt 
from util import rand_day,parseDateTime

now = time.time()

#basic_data = pd.read_pickle('./basic_data.pkl')
#print(basic_data)

user_path = './pre/User_pre.csv'
comment_path = './pre/Comment_pre.csv'
product_path = './pre/Product_pre.csv'
action_path = './pre/Action_pre.csv'

action_data = pd.read_pickle('./Action_pre.pkl')
print('Read Action')

#num = 10
#pre = 7
pre = 1

count = 0
for begin, middle, end in rand_day(pre,5):
	begin = begin.values[0]
	middle = middle.values[0]
	end = end.values[0]
	print(count)
	print(begin)
	print(middle)
	print(end)
	train_data = action_data.loc[(action_data['time']>=begin)&(action_data['time']<middle)]
	test_data = action_data.loc[(action_data['time']>=middle)&(action_data['time']<end)]
	test_data = test_data.loc[(test_data['type']=='T4'),["user_id", "sku_id"]]
	#print(test_data)
	test_data['Buy'] = 'True'
	train_data.to_csv('./cut_time/train_'+str(pre)+'_'+str(count)+'.csv', index=False)
	test_data.to_csv('./cut_time/test_'+str(pre)+'_'+str(count)+'.csv', index=False)
	print('./cut_time/test_'+str(pre)+'_'+str(count)+'.csv')
	#print(test_data)
	print(end)
	count+=1

middle = '2016-04-10'
end = '2016-04-15'
begin = (parseDateTime(middle,format="%Y-%m-%d")+dt.timedelta(days=(-1*pre))).date().isoformat()
train_data = action_data.loc[(action_data['time']>=begin)&(action_data['time']<middle)]
test_data = action_data.loc[(action_data['time']>=middle)&(action_data['time']<end)]
test_data = test_data.loc[(test_data['type']=='T4'),["user_id", "sku_id"]]
test_data['Buy'] = 'True'
train_data.to_csv('./cut_time/offline_train_'+str(pre)+'_1.csv', index=False)
test_data.to_csv('./cut_time/offline_test_'+str(pre)+'_1.csv', index=False)

middle = '2016-04-11'
end = '2016-04-16'
begin = (parseDateTime(middle,format="%Y-%m-%d")+dt.timedelta(days=(-1*pre))).date().isoformat()
train_data = action_data.loc[(action_data['time']>=begin)&(action_data['time']<middle)]
test_data = action_data.loc[(action_data['time']>=middle)&(action_data['time']<end)]
test_data = test_data.loc[(test_data['type']=='T4'),["user_id", "sku_id"]]
test_data['Buy'] = 'True'
train_data.to_csv('./cut_time/offline_train_'+str(pre)+'_2.csv', index=False)
test_data.to_csv('./cut_time/offline_test_'+str(pre)+'_2.csv', index=False)


train_data = action_data.loc[(action_data['time']>=begin)&(action_data['time']<middle)]
test_data = action_data.loc[(action_data['time']>=middle)&(action_data['time']<end)]
test_data = test_data.loc[(test_data['type']=='T4'),["user_id", "sku_id"]]

middle = '2016-04-16'
begin = (parseDateTime(middle,format="%Y-%m-%d")+dt.timedelta(days=(-1*pre))).date().isoformat()
train_data = action_data.loc[(action_data['time']>=begin)&(action_data['time']<middle)]
train_data.to_csv('./cut_time/final_'+str(pre)+'.csv', index=False)


cost_time = time.time()-now
print("end ......",'\n',"cost time:",cost_time,"(s)......")