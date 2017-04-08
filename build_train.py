import pandas as pd
import numpy as np
import time 
from util import rand_day

now = time.time()

user_path = './User_pre.csv'
comment_path = './Comment_pre.csv'
product_path = './Product_pre.csv'
action_path = './Action_pre.csv'

#action_data = pd.read_pickle('./Action_pre.pkl')
#print('Read Action')


#print(basic_data)
num = 10
#pre = 7
pre=2
def extract_feature(isfinal=False, num=None ,pre=None):
	if isfinal == False:
		count=0
		for begin, middle, end in rand_day(pre,5):
			print('Count:'+str(count))
			if count%10 != 4:
				count+=1
				continue
			begin = begin.values[0]
			middle = middle.values[0]
			end = end.values[0]
			train_data = pd.read_csv('./cut_time_2/train_'+str(pre)+'_'+str(count)+'.csv', index_col=None)
			test_data = pd.read_csv('./cut_time_2/test_'+str(pre)+'_'+str(count)+'.csv', index_col=None)
			count+=1
			basic_data = pd.read_pickle('./basic_data.pkl')
			#print(basic_data)
			#print('basic')
			for idx, series in basic_data.iterrows():
				if idx%1000==0 :
					print('IDX:'+str(idx))
					#print(basic_data) 
				uid = series['user_id']
				pid = series['sku_id']
				train_select = train_data.loc[(train_data['user_id']==uid)&(train_data['sku_id']==pid)]
				#print(idx)
				if not train_select.empty:
					type_count = train_select['type'].value_counts()
					#print(count)
					t1 = type_count.get('T1',0) #浏览
					t2 = type_count.get('T2',0) #加入
					t3 = type_count.get('T3',0) #删除
					t4 = type_count.get('T4',0) #下单
					t5 = type_count.get('T5',0) #关注
					t6 = type_count.get('T6',0) #点击
				else:
					t1 = 0 #浏览
					t2 = 0 #加入
					t3 = 0 #删除
					t4 = 0 #下单
					t5 = 0 #关注
					t6 = 0 #点击
				total_t = t1+t2+t3+t4+t5+t6
				basic_data.at[idx,str(pre)+'_total_t']=total_t
				basic_data.at[idx,str(pre)+'_t1']=t1
				basic_data.at[idx,str(pre)+'_t2']=t2
				basic_data.at[idx,str(pre)+'_t3']=t3
				basic_data.at[idx,str(pre)+'_t4']=t4
				basic_data.at[idx,str(pre)+'_t5']=t5
				basic_data.at[idx,str(pre)+'_t6']=t6
				basic_data.at[idx,str(pre)+'_t2jt3']=t2-t3
				basic_data.at[idx,str(pre)+'_total_tbpre']=total_t/pre
				basic_data.at[idx,str(pre)+'_t1bpre']=t1/pre
				basic_data.at[idx,str(pre)+'_t2bpre']=t2/pre
				basic_data.at[idx,str(pre)+'_t3bpre']=t3/pre
				basic_data.at[idx,str(pre)+'_t4bpre']=t4/pre
				basic_data.at[idx,str(pre)+'_t5bpre']=t5/pre
				basic_data.at[idx,str(pre)+'_t6bpre']=t6/pre
			print(basic_data)
			test_data = pd.merge(basic_data,test_data,on=['user_id','sku_id'],how='left')
			del basic_data
			test_data['Buy']= test_data['Buy'].fillna('False')
			test_data.to_csv('./xxgboost/try_xgboost_'+str(pre)+'_'+str(count)+'.csv', index=False)
	else:
		print('Final:')
		#end = 20160421
		#middle = 20160416
		#begin = 20160416-pre
		train_data = pd.read_csv('./cut_time_2/final_'+str(pre)+'.csv', index_col=None)
		basic_data = pd.read_pickle('./basic_data.pkl')
		for idx, series in basic_data.iterrows():
			if idx%1000==0 :
				print('IDX:'+str(idx))
				#print(basic_data) 
			uid = series['user_id']
			pid = series['sku_id']
			train_select = train_data.loc[(train_data['user_id']==uid)&(train_data['sku_id']==pid)]
			#print(idx)
			if not train_select.empty:
				type_count = train_select['type'].value_counts()
				#print(count)
				t1 = type_count.get('T1',0) #浏览
				t2 = type_count.get('T2',0) #加入
				t3 = type_count.get('T3',0) #删除
				t4 = type_count.get('T4',0) #下单
				t5 = type_count.get('T5',0) #关注
				t6 = type_count.get('T6',0) #点击
			else:
				t1 = 0 #浏览
				t2 = 0 #加入
				t3 = 0 #删除
				t4 = 0 #下单
				t5 = 0 #关注
				t6 = 0 #点击
			total_t = t1+t2+t3+t4+t5+t6
			basic_data.at[idx,str(pre)+'_total_t']=total_t
			basic_data.at[idx,str(pre)+'_t1']=t1
			basic_data.at[idx,str(pre)+'_t2']=t2
			basic_data.at[idx,str(pre)+'_t3']=t3
			basic_data.at[idx,str(pre)+'_t4']=t4
			basic_data.at[idx,str(pre)+'_t5']=t5
			basic_data.at[idx,str(pre)+'_t6']=t6
			basic_data.at[idx,str(pre)+'_t2jt3']=t2-t3
			basic_data.at[idx,str(pre)+'_total_tbpre']=total_t/pre
			basic_data.at[idx,str(pre)+'_t1bpre']=t1/pre
			basic_data.at[idx,str(pre)+'_t2bpre']=t2/pre
			basic_data.at[idx,str(pre)+'_t3bpre']=t3/pre
			basic_data.at[idx,str(pre)+'_t4bpre']=t4/pre
			basic_data.at[idx,str(pre)+'_t5bpre']=t5/pre
			basic_data.at[idx,str(pre)+'_t6bpre']=t6/pre
		print(basic_data)
		basic_data.to_csv('./xxgboost/final_xgboost_'+str(pre)+'.csv', index=False)

#extract_feature(isfinal=True, num=None ,pre=pre)
extract_feature(isfinal=False, num=num ,pre=pre)


cost_time = time.time()-now
print("end ......",'\n',"cost time:",cost_time,"(s)......")
