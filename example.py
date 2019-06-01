import pandas as pd 
import re
import rainflowpy as rf 
import matplotlib.pyplot as plt 

def test():


	
	df = pd.read_csv('daily-minimum-temperatures-in-me1.csv')
	data = df['Daily minimum temperatures']
	
	rainflow_obj= rf.Rainflow(data)
	print(rainflow_obj.count_range(0)) #raw counts are calculated and save for further bin analysis.

	print(rainflow_obj.count_range(0,True,0,3))  #using precomputed raw counts.
	


test()
