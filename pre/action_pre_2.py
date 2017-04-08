
import pandas as pd
action_path_out = './pre/Action_pre.csv'

data = pd.read_csv(action_path_out, index_col=None)
print('CSV')
print(data)
data.to_pickle('./Action_pre.pkl')
print('Done')
