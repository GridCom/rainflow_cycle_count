import numpy as np
from collections import defaultdict

class Rainflow:
	def __init__(self,data):
		self.data = data 
		self.raw_cycles = None

	


	def get_raw_cycles(self):
		def get_reversals(data):
			curr = 1
			last = 1 
			while curr<len(data)-1:
				if(data[curr]==data[curr+1]):
					curr = curr + 1
					continue
					
				if((data[last]>data[last-1])==(data[curr]>data[curr+1])):
					yield data[curr]
					curr = curr +1
					last = curr  
				else:
					
					curr  = curr + 1
		
		if  self.raw_cycles!=None:
			return self.raw_cycles


		reversals = [x for x in get_reversals(self.data)]
		

		n = len(reversals)


		curr = -1 #current index

		bow = []
		elems_left = n
		elems_del = 0
		goto2 = False

		while len(reversals)>curr:
			
			if goto2==False:

				curr +=1
				if len(reversals)<=curr:
					break

			if curr<2:
				goto2 = False
				continue


			if abs(reversals[curr]-reversals[curr-1]) >= abs(reversals[curr-2]-reversals[curr-1]):
				goto2 = True
				if(curr<=2):

					bow.append((abs(reversals[0]-reversals[1]),abs(reversals[0]+reversals[1])/2,0.5))
					curr = curr - 1
					elems_left -=1
					elems_del +=1
					reversals = np.delete(reversals,[0])

				else:
					bow.append((abs(reversals[curr-1]-reversals[curr-2]), abs(reversals[curr-1]+reversals[curr-2])/2, 1))
					reversals = np.delete(reversals,[curr-2])
					reversals = np.delete(reversals,[curr-2])
					curr = curr-2 
					elems_del +=2
					elems_left -=2
			else:
				goto2 = False
				
			
		for i in range(len(reversals)-1):
			bow.append((abs(reversals[i]-reversals[i+1]),abs(reversals[i]+reversals[i+1])/2,0.5))

		self.raw_cycles = bow
		def sortf(x):
			return x[0]
		return sorted(bow,key=sortf)


	

	def count_range_mean(self,ndigits=None,use_bins=False,refs=None,widths=None):
		def get_bracket(val,ndigits=None,ref=None,width=None,use_bins=False):
			if use_bins:
				print('here')
				to_ret =  ref + width*np.floor((val-ref)/width) + width/2
				if isinstance(ndigits,type(None)):

					
					return to_ret
				else:
					return round(to_ret,ndigits)
					
			else:
				if isinstance(ndigits,type(None)):
					return val
				else:
					return round(val,ndigits)

		if not self.raw_cycles:
			bow = self.get_raw_cycles()
			self.raw_cycles = bow

		bow = self.raw_cycles
		if use_bins:
			if len(refs)>1:
				r1,r2 = refs[:2]
			else:
				r1 = refs[0]
				r2 = refs[0]
			if len(widths)>1:
				w1,w2 = widths[:2]
			else:
				w1 = widths[0]
				w2 = widths[0]
		else:
			r1,r2 = None,None
			w1,w2 = None,None


		final_bow = defaultdict(float)
		print(ndigits)

		for elem in bow:
			elem = (get_bracket(elem[0],ndigits,r1,w1,use_bins), get_bracket(elem[1],ndigits,r2,w2,use_bins), elem[2])
			final_bow[(elem[0],elem[1])] +=elem[2]

		def sortf(x):
			return x[0][0]
		return sorted(final_bow.items(),key=sortf)

	def count_range(self,ndigits=None,use_bins=False,ref=None,width=None):
		def get_bracket(val,ndigits=None,ref=None,width=None,use_bins=False):
			if use_bins:
				to_ret =  ref + width*np.floor((val-ref)/width) + width/2
				if isinstance(ndigits,type(None)):

					
					return to_ret
				else:
					return round(to_ret,ndigits)
					
			else:
				if isinstance(ndigits,type(None)):
					return val
				else:
					return round(val,ndigits)


		if  self.raw_cycles==None:
			bow = self.get_raw_cycles()
			self.raw_cycles = bow
		bow = self.raw_cycles

		r1 = ref
		
		w1 = width
		
		final_bow = defaultdict(float)


		for elem in bow:
			range_,c  = (get_bracket(elem[0],ndigits,r1,w1,use_bins) ,elem[2])
			final_bow[range_] +=c

		def sortf(x):
			return x[0]
		return sorted(final_bow.items(),key=sortf)



    
	
