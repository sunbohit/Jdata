import xgboost as xgb
import pandas as pd
import time 
import numpy as np
import os

now = time.time()
'''
./merge3/xxgboost/try_xgboost_2_1_merge.csv
'''
train_root = './xxgboost/'
first_flag = True
dataset = None
for parent,dirnames,filenames in os.walk(train_root):
	for filename in filenames:
		print(filename)
		if first_flag :
			dataset = pd.read_csv(os.path.join(parent,filename), index_col=None)
			first_flag = False
		else:
			dataset = pd.concat([dataset, pd.read_csv(os.path.join(parent,filename), index_col=None)])
len_data = len(dataset)
print('Read Train Set')

#dataset['Iris-setosa'] = dataset['Iris-setosa'].map(char2int)

preset = pd.read_csv('./final_xgboost_1_merge.csv', index_col=None)
print('Read Predict Set')

len_pre =len(preset)
insert_buy = pd.Series([True]*len_pre)
preset.insert(0,'Buy', insert_buy)
#print(preset)
#print(len(preset))
concatset = pd.concat([dataset,preset])
del dataset
del preset
print('Finished concat')

concatset.model_id = 'MD-1'
#concatset.brand = 'BD-1'
concatset.user_reg_tm = '2016-01-01'
def precess_Buy(x):
	if x == 'True' or x == True:
		return True
	else:
		return False
concatset.Buy = concatset.Buy.map(precess_Buy)

concatset = pd.get_dummies(concatset)
print('Onehot')
print(concatset.columns)

cols = list(concatset.columns)
cols.insert(0, cols.pop(cols.index('Buy')))
b = concatset['Buy']
concatset.drop(labels=['Buy'], axis=1,inplace = True)
concatset.insert(0, 'Buy', b)

cols = list(concatset.columns)
cols.insert(1, cols.pop(cols.index('user_id')))
b = concatset['user_id']
concatset.drop(labels=['user_id'], axis=1,inplace = True)
concatset.insert(1, 'user_id', b)

cols = list(concatset.columns)
cols.insert(2, cols.pop(cols.index('sku_id')))
b = concatset['sku_id']
concatset.drop(labels=['sku_id'], axis=1,inplace = True)
concatset.insert(2, 'sku_id', b)

print(concatset.columns)

preset = concatset.iloc[len_data:,:]
dataset = concatset.iloc[:len_data,:]
del concatset
#print('Preset')
#print(preset)
#print('Preset_Len')
#print(len(preset))

'''
dataset = dataset.sample(frac=1)
dataset_2 = dataset.iloc[:len_data//4,:]
dataset = dataset.iloc[len_data//4:,:]
'''

#dataset = dataset.fillna(dataset.mean())
#print(dataset)
count = dataset['Buy'].value_counts()
print(count)
neg_data = dataset.loc[(dataset['Buy']==False)].sample(n=7000000, replace=True)
pos_data = dataset.loc[(dataset['Buy']==True)].sample(n=3000000, replace=True)
dataset = pd.concat([neg_data,pos_data])
dataset = dataset.sample(frac=1)
count = dataset['Buy'].value_counts()
print(count)

train_features = dataset.iloc[:,3:].values
train_labels = dataset.iloc[:,0].values
del dataset

'''
test_features = dataset_2.iloc[:,3:].values
test_labels = dataset_2.iloc[:,0].values
del dataset_2
'''
test_features = preset.iloc[:,3:].values

print(train_features)
print(train_labels)
print(len(train_features))
print(len(train_labels))

#tests = pd.read_csv("../input/test.csv") # 注意自己数据路径
#test_id = range(len(tests))
#test = tests.iloc[:,:].values

params_1={
'booster':'gbtree',
# 这里手写数字是0-9，是一个多类的问题，因此采用了multisoft多分类器，
'objective': 'binary:logitraw', 
#'objective': 'binary:logistic',
#'objective': 'multi:softmax',
#'num_class':3, # 类数，与 multisoftmax 并用
'gamma':0.05,  # 在树的叶子节点下一个分区的最小损失，越大算法模型越保守 。[0:]
'max_depth':12, # 构建树的深度 [1:]
#'lambda':450,  # L2 正则项权重
'subsample':0.4, # 采样训练数据，设置为0.5，随机选择一般的数据实例 (0:1]
'colsample_bytree':0.7, # 构建树树时的采样比率 (0:1]
#'min_child_weight':12, # 节点的最少特征数
'silent':1 ,
'eta': 0.005, # 如同学习率
'seed':710,
'nthread':12,# cpu 线程数,根据自己U的个数适当调整
}
params_2={
'booster':'gbtree',
	    'objective': 'rank:pairwise',
	    'eval_metric':'auc',
	    'gamma':0.1,
	    'min_child_weight':1.1,
	    'max_depth':5,
	    'lambda':10,
	    'subsample':0.7,
	    'colsample_bytree':0.7,
	    'colsample_bylevel':0.7,
	    'eta': 0.01,
	    'tree_method':'exact',
	    'seed':0,
	    'nthread':12
}
params_3={
'booster':'gblinear',
'alpha':0,
'silent':0 , 
'nthread':12,# cpu 线程数,根据自己U的个数适当调整
'objective': 'binary:logitraw', 
#'objective': 'binary:logistic',
#'objective': 'multi:softmax',
#'num_class':3, # 类数，与 multisoftmax 并用

#'lambda':450,  # L2 正则项权重

'seed':710,

}

plst = list(params_1.items())

#Using 10000 rows for early stopping. 

print("Check 1")
num_rounds = 10000 # 迭代你次数
#xgtest = xgb.DMatrix(train)
xgtest = xgb.DMatrix(test_features)
print("Check 2")
# 划分训练集与验证集 
off = 7000000
xgtrain = xgb.DMatrix(train_features[:off], label=train_labels[:off])
xgval = xgb.DMatrix(train_features[off:], label=train_labels[off:])
print(train_labels)
del train_features
#del train_labels

# return 训练和验证的错误率
watchlist = [(xgtrain, 'train'),(xgval, 'val')]

print("Check 3")
# training model 
# early_stopping_rounds 当设置的迭代次数较大时，early_stopping_rounds 可在一定的迭代次数内准确率没有提升就停止训练
model = xgb.train(plst, xgtrain, num_rounds, watchlist,early_stopping_rounds=100)

print("Check 4")
#model = xgb.train(plst, xgtrain, num_rounds, watchlist,early_stopping_rounds=100)
#model.save_model('./1_xgb.model') # 用于存储训练出的模型
#preds = model.predict(xgtest,ntree_limit=model.best_iteration)
preds = model.predict(xgtest)
model.save_model('./3_xgb.model')
preset['Buy'] = pd.Series(preds)
print(preset)
preset.loc[:,['user_id','sku_id','Buy']].to_csv('predict_3.csv',index=None)
'''
print(preds>0.5)
print(sum(preds>0.5))
test_length = len((preds>0.5)==test_labels)
test_right = sum((preds>0.5)==test_labels)
print(test_right/test_length)
'''
cost_time = time.time()-now
print("end ......",'\n',"cost time:",cost_time,"(s)......")
