import random
import pandas as pd
import datetime as dt
import time

def rand_day(train_length, test_length, num=None):
	day_list = pd.read_csv('./day_list.csv')
	#print(day_list)
	day_length = len(day_list)
	#k = (day_length-train_length-test_length)//num
	k=1
	for begin in range(0, day_length-1-train_length-test_length, k):
		#begin = random.randint(0,day_length-1-train_length-test_length)
		middle = begin+train_length
		end = middle+test_length
		#print(begin)
		#print(day_list.iloc[begin])
		#print(middle)
		#print(day_list.iloc[middle])
		#print(end)
		#print(day_list.iloc[end])
		yield day_list.iloc[begin], day_list.iloc[middle], day_list.iloc[end]

def build_time_list():
	#adata = pd.read_csv('./Action_pre.csv')
	adata = pd.read_pickle('./Action_pre.pkl')
	aday = (adata['time']).drop_duplicates()
	del adata 
	print(aday)
	aday = aday.map(extract_date)
	aday = aday.drop_duplicates()
	aday.to_csv('./day_list.csv', index=False)

def DateTime2String(dati):
	return dati.isoformat()

#def parseDateTime(input, format="%Y-%m-%d"):
def parseDateTime(input, format="%Y-%m-%d %H:%M:%S"):
	return dt.datetime.fromtimestamp(time.mktime(time.strptime(input,format)))

def extract_date(input):
	return DateTime2String(parseDateTime(input, format="%Y-%m-%d %H:%M:%S").date())
if __name__== "__main__":
	
	#str_1 = "2016-02-29"
	#str_2="2016-02-29 23:59:01"
	#str_3="2016-04-29 23:59:01"
	#dt_1 = parseDateTime(str_1,format="%Y-%m-%d")
	#dt_3 = parseDateTime(str_3,format="%Y-%m-%d %H:%M:%S")
	#print((dt_3-dt_1).days)
	#print(extract_date(str_3))
	#print(dt_1+dt.timedelta(days=1)) 
	#print(dt_1.date())
	#print([i for i in range(0, 10, 1)])
	
	#build_time_list()
	#rand_day(10,5)
	pass