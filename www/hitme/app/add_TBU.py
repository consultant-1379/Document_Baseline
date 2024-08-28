import os
import sys

file_name = sys.argv[1]
my_file = open(file_name, "r")
all_lines = my_file.readlines()
my_file.close()

file_len = len(all_lines)

flag = 0

for line in range(file_len):
    data = all_lines[line].split("::::")

    data.insert(7, "TBU")

    data_len = len(data)
    final_data= ""
    for i in range(data_len-1):
        final_data += data[i] + "::::"

    final_data = final_data + data[data_len-1].strip()
    print final_data

    if flag == 0:
	final_file = open(file_name,'w')
	final_file.writelines(final_data)
        final_file.writelines("\n")
	final_file.close()
    else:
	final_file = open(file_name,'a')
        final_file.writelines(final_data)
        final_file.writelines("\n")
        final_file.close()
    flag +=1
