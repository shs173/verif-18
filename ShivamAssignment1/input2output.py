import math
import os
import sys
n = 4

input_list = []
for line in open(sys.argv[1]):
	input_list = line.split()

n = int(math.sqrt(len(input_list)))
file = open("shidoku.props", "w")
list_basic = []
for i in range (1, n+1):
	for j in range (1, n+1):
		for val in range (1, n+1):
			
			list_basic.append(i*100 + j*10 + val)
			list = []	
			''' everything in the same row '''	
			for c in range (1, n+1):
				if c != j:
					list.append(i*100 + c*10 + val)

			''' everything in the same column '''	
			for r in range (1, n+1):
			 	if r != i:
			 		list.append(r*100 + j*10 + val)
			
			''' everything in the same box '''
			m = int(math.sqrt(n))	
			if (i <= m and j <= m):
				''' upper limit on row index'''
				ur = m   
				''' upper limit on col index'''
				lr = 1	 
				uc = m
				lc = 1
			elif (i <= m and j <= 2*m):
				ur = m
				lr = 1
				uc = 2*m
				lc = m+1
			elif (i <= m and j > 2*m):
				ur = m
				lr = 1
				uc = 3*m
				lc = 2*m + 1

			elif (i <= 2*m and j <= m):
				ur = 2*m
				lr = m + 1
				uc = m
				lc = 1
			elif (i <= 2*m and j <= 2*m):
				ur = 2*m
				lr = m + 1
				uc = 2*m
				lc = m + 1
			elif (i <= 2*m and j > 2*m):
				ur = 2*m
				lr = m + 1
				uc = 3*m 
				lc = 2*m + 1

			elif (i > 2*m and j <= m):
				ur = 3*m
				lr = 2*m + 1
				uc = m
				lc = 1
			elif (i > 2*m and j <= 2*m):
				ur = 3*m
				lr = 2*m + 1
				uc = 2*m
				lc = m + 1
			elif (i > 2*m and j > 2*m):
				ur = 3*m
				lr = 2*m + 1
				uc = 3*m 
				lc = 2*m + 1
			
			for r in range (lr, ur + 1):
				for c in range (lc, uc + 1):
					if (r !=i and c != j):
						list.append(r*100 + c*10 + val)
			
			''' write to file '''
			file.write("\nx%d%d%d implies not x%d " %(i,j,val,list[0]))
			list.remove(list[0])
			for item in list:
				file.write("and not x%d " %item)

index = 0
for i in range (1, n+1):
	for j in range (1, n+1):
		file.write("\n")
		for val in range (1, n+1):
			if (val != n):	
				file.write("x%d or " %(list_basic[index]))
			else:
		 		file.write("x%d" %(list_basic[index]))
		   	index = index + 1	

index = 0
for i in range (1, n+1):
	for j in range (1, n+1):		
		item = int(input_list[index])
		index = index + 1
		if (item != 0):
			file.write("\nx%d%d%d" %(i,j,item))
file.close()

os.system("python prop2cnf.py shidoku.props > shidoku.cnf")
os.system("./zchaff shidoku.cnf > cnfout.txt")

sol_str_list = []
start = 0
for line in open("cnfout.txt"):
	if (start == 1):
		sol_str_list = line.split(" ")	
		break
	test = []	
	test = line.split(" ")
	if (test[0] == 'Instance'):
		start = 1
		
sol_int_list = []
for item in sol_str_list:
	if (item == 'Random'):
		break
	elif (int(item) > 0):
		sol_int_list.append(int(item))

cnf2varDict = {}	
for line in open("shidoku.cnf"):
	test = []
	test = line.split(" ")
	if (len(test) > 2): 
		if (test[0] == 'c' and test[1] != 'original' and test[1] != 'parsetree:' and test[1] != 'clauses'):
			if (int(test[1]) > 0 and int(test[1]) < n*n*n):
				key = int(test[1])
				temp = test[3].split("\n")
				var = temp[0].split('x')
				cnf2varDict[key] = int(var[1])

pos2valDict = {}		
for item in sol_int_list:
	temp = cnf2varDict[item]
	val  = temp % 10
	key  = temp / 10
	pos2valDict[key] = val

pos2valList = sorted(pos2valDict)
for key in pos2valList:
	sys.stdout.write(str(pos2valDict[key])+' ')
print


















