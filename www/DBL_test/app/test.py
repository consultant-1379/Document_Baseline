import os

final_list = []

def delta_sort_ncpi(shipment1):
        file_name = "/var/www/hitme/app/NetAN_Features_Library_doc_details.txt";
        file_read = open(file_name, 'r')
        data_lines = file_read.readlines()
        file_read.close()

        for line in data_lines:
                data_list = line.split("::::")
                if data_list[0] == shipment1:
                        final_list.append(line)
		
	write_file = open('/var/www/hitme/app/test_result.txt', 'w+')
	write_file.writelines(final_list)

delta_sort_ncpi("20.4.9.EU2")
print final_list

