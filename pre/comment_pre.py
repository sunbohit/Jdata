import pandas as pd

comment_path = './JData_Comment.csv'
comment_path_out = './Comment_pre.csv'

data = pd.read_csv(comment_path, index_col=None, encoding='gbk')
print(data)
'''
[558552 rows x 5 columns]
'''
print(len(set(data['sku_id'])))
'''
46546
'''

print(data['dt'].min())
'''
20160201
'''
print(data['dt'].max())
'''
20160415
'''

data_1 = data.sort_index(by='dt',ascending=True)
print(data_1)

data_1.to_csv(comment_path_out, index=False)