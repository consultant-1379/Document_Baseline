dict = {}

def search_delta_sort(shipm, doc_detail_file):
        sorted_list = []
        final_list = []

        with open(doc_detail_file, 'r') as file_read:
                data_lines = file_read.readlines()

        for line in data_lines:
                data_list = [item.strip() for item in line.split('::::')]
                if data_list[0] == shipm:
                        sorted_list.append(data_list)
        sorted_list.sort(key=lambda x: x[2])

        index = 0
        for item in sorted_list:
                doc_list = []
                doc_list.append(item)
                doc_name = item[2].strip()
                doc_num = item[3].strip()
		print doc_name
		print doc_num
		
                index+=1
                for i in sorted_list[index:]:
                        if i[2].strip() == doc_name and i[3].strip() == doc_num:
				doc_list.append(i)
		    		sorted_list.pop(index)
                        else:
                                continue
                print doc_list
		print "\n\n"
                doc_list.sort(key=lambda x: x[5], reverse=True)
                final_list.append(doc_list[0])
        with open('/var/www/hitme/app/Delta_result.txt', 'w+') as write_file:
                for line in final_list:
                        write_file.writelines(item + "::::" for item in line[:-1])
                        write_file.writelines(line[-1])
                        write_file.writelines("\n")

        with open('/var/www/hitme/app/Delta_result.txt', 'r') as final_file:
                delta_content = final_file.readlines()
        return delta_content

def document_list_main_cpi():
		dd = []
		doc_detail_file = "/var/www/hitme/app/CPI_doc_details.txt"
		type = "Delta"
		shipm = "21.2.8.EU2"
		if type == "Full":
				doc_details_list = search_sort_cpi(shipm)
		elif type == "Delta":
				doc_details_list = search_delta_sort(shipm, doc_detail_file)
		for doc_t in doc_details_list:
				dets = doc_t.split("::::")
				a = doc_t.find(dets[1])
				doc_t = doc_t[a:]
				b = doc_t.find('::::')
				doc_t = doc_t[0:b]
				dd.append(doc_t)
		dd = list(dict.fromkeys(dd))
		print dd
		
document_list_main_cpi()
