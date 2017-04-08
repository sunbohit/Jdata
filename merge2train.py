import pandas as pd
import numpy as np
import time 
import os
import os.path

now = time.time()

def merge3table(inter_path, isfinal=False):
	if os.path.exists('./merge3'+(inter_path.strip('.csv')+'_merge.csv')):
		return
	inter_data = pd.read_csv(inter_path,index_col=None)
	user_data = pd.read_csv('./user_basic_feature.csv',index_col=None)
	inter_data = pd.merge(inter_data,user_data,on=['user_id'],how='left')
	del user_data
	
	sku_data = pd.read_csv('./sku_basic_feature.csv',index_col=None)
	inter_data = pd.merge(inter_data,sku_data,on=['sku_id'],how='left')
	del sku_data
	
	#print(inter_data)
	#print(inter_data.columns)
	#'''
	if isfinal:
		inter_data.to_csv('./merge3/'+(inter_path.strip('.csv').strip('/xxgboost')+'_merge.csv'), index=False)
		return
	cols = list(inter_data.columns)
	cols.insert(0, cols.pop(cols.index('Buy')))
	buy = inter_data['Buy']
	inter_data.drop(labels=['Buy'], axis=1,inplace = True)
	#print(type(buy))
	inter_data.insert(0, 'Buy', buy)
	print(inter_data)
	print(inter_data.columns)
	#'''
	inter_data.to_csv('./merge3'+(inter_path.strip('.csv')+'_merge.csv'), index=False)
	
#merge3table('./try_xgboost_2_3.csv')
#merge3table('./xxgboost/final_xgboost_2.csv')
feature_dir = './xxgboost/'
for parent,dirnames,filenames in os.walk(feature_dir):
		for filename in filenames:
			print(filename)
			if filename[:5] == 'final':
				continue
			merge3table(os.path.join(parent,filename))

final_file = './xxgboost/final_xgboost_1.csv'
merge3table(final_file,isfinal=True)

cost_time = time.time()-now
print("end ......",'\n',"cost time:",cost_time,"(s)......")
