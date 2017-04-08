import pandas as pd
import numpy as np

product_path = './JData_Product.csv'
product_path_out = './Product_pre.csv'

data = pd.read_csv(product_path, index_col='sku_id', encoding='gbk')
print(data)
'''
[24187 rows x 5 columns]
'''
print(set(data.a1))
'''
{1, 2, 3, -1}
'''
attr1_dict={1:'A', 2:'B', 3:'C', -1:np.nan}
for key,value in attr1_dict.items():
	#print(key) 
	data.a1[data.a1==key] = value
print(set(data.a2))
'''
{1, 2, -1}
'''
attr2_dict={1:'A', 2:'B', -1:np.nan}
for key,value in attr2_dict.items():
	#print(key) 
	data.a2[data.a2==key] = value
print(set(data.a3))
'''
{1, 2, -1}
'''
attr3_dict={1:'A', 2:'B', -1:np.nan}
for key,value in attr3_dict.items():
	#print(key) 
	data.a3[data.a3==key] = value
print(set(data['cate']))
'''
{8}
'''
cate_dict={8:'C8'}
for key,value in cate_dict.items():
	#print(key) 
	data['cate'][data['cate']==key] = value
print(set(data['brand']))
'''
{3, 515, 13, 14, 24, 25, 541, 30, 545, 554, 556, 48, 561, 562, 51, 49, 571, 574, 70, 76, 594, 83, 596, 599, 88, 90, 91, 605, 101, 622, 623, 116, 635, 124, 127, 655, 658, 665, 159, 673, 674, 677, 174, 180, 693, 197, 200, 717, 209, 211, 214, 225, 739, 227, 752, 244, 759, 249, 766, 772, 263, 790, 283, 285, 800, 801, 291, 804, 299, 812, 306, 318, 321, 324, 837, 328, 331, 336, 855, 857, 354, 355, 871, 875, 370, 885, 375, 383, 900, 905, 907, 403, 916, 404, 922, 427, 438, 453, 479, 484, 489, 499}
'''
print(len(set(data['brand'])))
'''
102
'''
data['brand']= data['brand'].map(lambda x : 'BD'+str(x))
data_1 = data.sort_index(axis=0,ascending=True)
print(data_1['brand'])

data_1.to_csv(product_path_out)

