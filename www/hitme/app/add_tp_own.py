import os
import sys

file_name = sys.argv[1]
my_file = open(file_name, "r")
all_lines = my_file.readlines()
my_file.close()
file_len = len(all_lines)

data_file_name = "technical_owners.txt"
data_file = open(data_file_name, "r")
data_lines = data_file.readlines()
data_file.close()
data_len = len(data_lines)

flag = 0

for line in all_lines:
    data = line.split("::::")
    doc_name = data[2].strip()
    team_name = data[6].strip() 
    if "TP/KPI" in team_name or "TP\KPI" in team_name:
	data[7] = "Suvro Bakshi"
    else:
    	for i in data_lines:
        	doc_data = i.split("::")
        	if doc_data[0] == doc_name:
            		data[7] = doc_data[1].strip()
	    		break
		else:
	    		continue
    data_len = len(data)
    final_data= ""
    for i in range(data_len-1):
        final_data += data[i] + "::::"

    final_data = final_data + data[data_len-1].strip()
    print final_data

    if flag == 0:
        final_file = open(file_name+"_new",'w')
        final_file.writelines(final_data)
        final_file.writelines("\n")
        final_file.close()
    else:
        final_file = open(file_name+"_new",'a')
        final_file.writelines(final_data)
        final_file.writelines("\n")
        final_file.close()
    flag +=1

