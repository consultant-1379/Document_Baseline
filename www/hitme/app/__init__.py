from flask import Flask, render_template, redirect, url_for, request
import datetime
import json
import natsort
import xlsxwriter
import os
import paramiko
from scp import SCPClient


app = Flask(__name__)
app.secret_key = "abc"
dict={}


def file_to_list(filename):
        file = open(filename,'r')
        list =  file.readlines()
        list2=[]
        for elem in list:
                elem = elem.strip()
                list2.append(elem)
        file.close()
        return list2


def openfile(filename):
        file = open(filename,'a')
        return file


def copy_file(excel_file):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
	ssh.connect('seliius26954.seli.gic.ericsson.se',username='eniqdmt',password='EStAts(iDec$2()18',key_filename='/var/www/hitme/id_rsa.pub')
	scp = SCPClient(ssh.get_transport())
	scp.put('/var/www/hitme/app/excel_files/'+excel_file, '/proj/pduosslegacy/eniqdmt/dbl_files/'+excel_file)
	scp.close()


def create_excel(shipm, data_list, doc_type):
	excel_file = shipm+"_"+doc_type+"_Delta.xlsx"
	full_path = "/var/www/hitme/app/excel_files/"+excel_file
        heading_list = ["Sprint", "Document type", "Document Title", "Document Number", "Eridoc Link", "Revision", "Document Owner", "Technical Owner", "Date", "Comments"]
        
        workbook = xlsxwriter.Workbook(full_path)
        worksheet = workbook.add_worksheet()
	
	worksheet.set_column(0, 5, 12)
	worksheet.set_column(1, 4, 75)
	worksheet.set_column(3, 3, 25)
	worksheet.set_column(6, 9, 30)

	cell_format = workbook.add_format({'bold': True, 'bg_color': '#32CD32', 'border': True})
        row=0
        col=0
	
        for item in heading_list:
        	worksheet.write(row, col, item, cell_format)
        	col+=1
        row+=1

        for inlist in data_list:
        	col = 0
        	for item in inlist:
                	worksheet.write(row, col, item)
                	col+=1
        	row+=1
        workbook.close()

	copy_file(excel_file)


def search_delta_sort(shipm, doc_detail_file, doc_type):
        sorted_list = []
        final_list = []

        with open(doc_detail_file, 'r') as file_read:
                data_lines = file_read.readlines()

        for line in data_lines:
                data_list = [item.strip() for item in line.split('::::')]
                if data_list[0] == shipm:
                        sorted_list.append(data_list)
        sorted_list.sort(key=lambda x: x[2])

        for idx,item in enumerate(sorted_list):
                doc_list = []
                doc_list.append(item)
                doc_name = item[2].strip()
                doc_num = item[3].strip()

                for i in sorted_list[idx+1:]:
                    if i[2].strip() == doc_name:
                        doc_list.append(i)
                        sorted_list.pop(sorted_list.index(i))

                doc_list.sort(key=lambda x: x[5], reverse=True)
                final_list.append(doc_list[0])
        with open('/var/www/hitme/app/Delta_result.txt', 'w') as write_file:
                for line in final_list:
                        write_file.writelines(item + "::::" for item in line[:-1])
                        write_file.writelines(line[-1])
                        write_file.writelines("\n")
	
	create_excel(shipm, final_list, doc_type)

        with open('/var/www/hitme/app/Delta_result.txt', 'r') as final_file:
                delta_content = final_file.readlines()
        return delta_content


def search_sort_ncpi(shipment1):
        file = "/var/www/hitme/app/NetAN_Features_Library_doc_details.txt";
        fp = open(file, 'r')
        l = fp.readlines()
        fp.close()

        def my_ship(e):
                return(e.split("::::"))
        l.sort(key=my_ship)

        l.reverse()
        file2 = "/var/www/hitme/app/Sorted.txt";
        fp1 = open(file2,'w')
        fp1.writelines(l)
        fp1.close()

        fp3 = open(file2,"r")
        s = fp3.readlines()
        p = len(s)

        f1=0

        for i in range(p):
                l1 = list(s[i].split("::::"))
                if(l1[0] == shipment1):
                        f1 = 1
                        break;

        if (f1==1):
                l2 = []
                for j in range(i,p):
                        l2.append(s[j])
        else:
                l2 = []
                for j in range(p):
                        l2.append(s[j])

        q = len(l2)
        l6 = []
        for j in range(q):
                l6.append(list(l2[j].split("::::")))

        m=0
        l3 = []

        for j in range(q):
                val = l6[j][1]
                val1 = l6[j][2]
                val2 = l6[j][3]
		val3 = l6[j][5]
                val4 = l6[j][0]
                for k in range(j+1,q):
                        if((l6[k][1] == val and l6[k][2] == val1) or (l6[k][3] == val2)):
                                if(l6[k][5] > val3 and l6[k][0] >= val4):
                                        l3.append(l2[j])
                                        m = m +1
                                else:
                                        l3.append(l2[k])
                                        m = m + 1



        fp1 = open("/var/www/hitme/app/Search_result.txt",'w')
        fp1.close()

        for j in range(len(l2)):
                f=0
                for k in range(len(l3)):
                        if(l2[j] == l3[k]):
                                f=1;
                                break;

                if(f==0):
                        fp1 = open("/var/www/hitme/app/Search_result.txt",'a')
                        fp1.writelines(l2[j])
                        fp1.close()

        fp1 = open("/var/www/hitme/app/Search_result.txt",'r')
        list1 = fp1.readlines()
        fp1.close()
        return list1
		
def search_sort_other_docs(shipment1):
        file = "/var/www/hitme/app/Other_Documents_doc_details.txt";
        fp = open(file, 'r')
        l = fp.readlines()
        fp.close()

        def my_ship(e):
                return(e.split("::::"))
        l.sort(key=my_ship)

        l.reverse()
        file2 = "/var/www/hitme/app/Sorted.txt";
        fp1 = open(file2,'w')
        fp1.writelines(l)
        fp1.close()

        fp3 = open(file2,"r")
        s = fp3.readlines()
        p = len(s)

        f1=0

        for i in range(p):
                l1 = list(s[i].split("::::"))
                if(l1[0] == shipment1):
                        f1 = 1
                        break;

        if (f1==1):
                l2 = []
                for j in range(i,p):
                        l2.append(s[j])
        else:
                l2 = []
                for j in range(p):
                        l2.append(s[j])

        q = len(l2)
        l6 = []
        for j in range(q):
                l6.append(list(l2[j].split("::::")))

        m=0
        l3 = []

        for j in range(q):
                val = l6[j][1]
                val1 = l6[j][2]
                val2 = l6[j][3]
		val3 = l6[j][5]
                val4 = l6[j][0]
                for k in range(j+1,q):
                        if((l6[k][1] == val and l6[k][2] == val1) or (l6[k][3] == val2)):
                                if(l6[k][5] > val3 and l6[k][0] >= val4):
                                        l3.append(l2[j])
                                        m = m +1
                                else:
                                        l3.append(l2[k])
                                        m = m + 1


        fp1 = open("/var/www/hitme/app/Search_result.txt",'w')
        fp1.close()

        for j in range(len(l2)):
                f=0
                for k in range(len(l3)):
                        if(l2[j] == l3[k]):
                                f=1;
                                break;

                if(f==0):
                        fp1 = open("/var/www/hitme/app/Search_result.txt",'a')
                        fp1.writelines(l2[j])
                        fp1.close()

        fp1 = open("/var/www/hitme/app/Search_result.txt",'r')
        list1 = fp1.readlines()
        fp1.close()
        return list1

def search_sort_cpi(shipment1):
        file = "/var/www/hitme/app/CPI_doc_details.txt";
        fp = open(file, 'r')
        l = fp.readlines()
        fp.close()
        def my_ship(e):
                return(e.split("::::"))
        l.sort(key=my_ship)

        l.reverse()
        file2 = "/var/www/hitme/app/Sorted.txt";
        fp1 = open(file2,'w')
        fp1.writelines(l)
        fp1.close()

        fp3 = open(file2,"r")
        s = fp3.readlines()
        p = len(s)

        f1=0

        for i in range(p):
                l1 = list(s[i].split("::::"))
                if(l1[0] == shipment1):
                        f1 = 1
                        break;

        if (f1==1):
                l2 = []
                for j in range(i,p):
                        l2.append(s[j])
        else:
                l2 = []
                for j in range(p):
                        l2.append(s[j])

        q = len(l2)
        l6 = []
        for j in range(q):
                l6.append(list(l2[j].split("::::")))

        m=0
        l3 = []

        for j in range(q):
                val = l6[j][1]
                val1 = l6[j][2]
                val2 = l6[j][3]
		val3 = l6[j][5]
                val4 = l6[j][0]
                for k in range(j+1,q):
                        if((l6[k][1] == val and l6[k][2] == val1) or (l6[k][3] == val2)):
                                if(l6[k][5] > val3 and l6[k][0] >= val4):
                                        l3.append(l2[j])
                                        m = m +1
                                else:
                                        l3.append(l2[k])
                                        m = m + 1


        fp1 = open("/var/www/hitme/app/Search_result.txt",'w')
        fp1.close()

        for j in range(len(l2)):
                f=0
                for k in range(len(l3)):
                        if(l2[j] == l3[k]):
                                f=1;
                                break;

                if(f==0):
                        fp1 = open("/var/www/hitme/app/Search_result.txt",'a')
                        fp1.writelines(l2[j])
                        fp1.close()

        fp1 = open("/var/www/hitme/app/Search_result.txt",'r')
        list2 = fp1.readlines()
        fp1.close()
        return list2

def search_sort_cal(shipment1):
        file = "/var/www/hitme/app/CALSTORE_doc_details.txt";
        fp = open(file, 'r')
        l = fp.readlines()
        fp.close()
        def my_ship(e):
                return(e.split("::::"))
        l.sort(key=my_ship)

        l.reverse()
        file2 = "/var/www/hitme/app/Sorted.txt";
        fp1 = open(file2,'w')
        fp1.writelines(l)
        fp1.close()
        fp3 = open(file2,"r")
        s = fp3.readlines()
        p = len(s)
        f1=0
        for i in range(p):
                l1 = list(s[i].split("::::"))
                if(l1[0] == shipment1):
                        f1 = 1
                        break;
        if (f1==1):
                l2 = []
                for j in range(i,p):
                        l2.append(s[j])
        else:
                l2 = []
                for j in range(p):
                        l2.append(s[j])
        q = len(l2)
        l6 = []
        for j in range(q):
                l6.append(list(l2[j].split("::::")))
        m=0
        l3 = []
        for j in range(q):
                val = l6[j][1]
                val1 = l6[j][2]
                val2 = l6[j][3]
		val3 = l6[j][5]
		val4 = l6[j][0]
                for k in range(j+1,q):
        		if((l6[k][1] == val and l6[k][2] == val1) or (l6[k][3] == val2)):                                    
            			if(l6[k][5] > val3 and l6[k][0] >= val4):
                			l3.append(l2[j])
                			m = m +1
            			else:
                			l3.append(l2[k])
                			m = m + 1

        fp1 = open("/var/www/hitme/app/Search_result.txt",'w')
        fp1.close()
        for j in range(len(l2)):
                f=0
                for k in range(len(l3)):
                        if(l2[j] == l3[k]):
                                f=1;
                                break;
                if(f==0):
                        fp1 = open("/var/www/hitme/app/Search_result.txt",'a')
                        fp1.writelines(l2[j])
                        fp1.close()
        fp1 = open("/var/www/hitme/app/Search_result.txt",'r')
        list1 = fp1.readlines()
        fp1.close()
        return list1
@app.route("/document_baseline")
def home():
        return render_template("home.html")

@app.route("/document_baseline/upload", methods=['GET', 'POST'])
def upload():
        message=None
        doc_details = open('/var/www/hitme/app/doc_details.txt','a')
        doc_list_cpi = file_to_list("/var/www/hitme/app/CPI_Doc_Type.txt")
        doc_list_ncpi = file_to_list("/var/www/hitme/app/NetAn_CPI_Doc_Type.txt")
	doc_list_other_docs = file_to_list("/var/www/hitme/app/Other_Docs_Doc_Type.txt")
        doc_list_calstore = file_to_list("/var/www/hitme/app/CALSTORE_Doc_Type.txt")
	doc_details_list = file_to_list("/var/www/hitme/app/doc_details.txt")

        cpi_installation_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Installation_doc.txt")
        cpi_se_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Safety_and_Environment_doc.txt")
        cpi_lo_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Library_Overview_doc.txt")
        cpi_po_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Product_Overview_doc.txt")
        cpi_tu_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Technology_Package_Descriptions_and_Universe_References_doc.txt")
        cpi_ug_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_OM_User_Guides_doc.txt")
        cpi_sag_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_System_Administrator_Guides_doc.txt")
        cpi_bi_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Business_Intelligence_Reports_User_Guides.doc.txt")
        cpi_intf_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Interface_doc.txt")
        cpi_3pp_bo_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_3PP_BO_doc.txt")
        cpi_rhel_doc = file_to_list("/var/www/hitme/app/CPI_Docs/Third_Party_doc.txt")
        cpi_ad_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Additional_Documentation_doc.txt")
	cpi_osd_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Operating_Instruction_doc.txt")
        cal_se_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Safety_and_Environment_doc.txt")
        cal_lo_doc = file_to_list("/var/www/hitme/app/CPI_Docs/CPI_Library_Overview_doc.txt")
        cal_dimen_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Dimensioning_doc.txt")
        cal_ii_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Initial_Installation_doc.txt")
        cal_infra_mws_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Infra_MWS_doc.txt")
        cal_infra_nas_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Infra_NAS_doc.txt")
        cal_oss_monitr_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_OSS_Monitoring_doc.txt")
        cal_ug_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Upgrade_doc.txt")
        cal_fh_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Feature_Handling_doc.txt")
        cal_mig_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Migration_doc.txt")
        cal_exp_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Expansion_doc.txt")
        cal_int_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Integration_doc.txt")
        cal_rl_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Reporting_Layer_doc.txt")
        cal_nh_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Node_Hardening_doc.txt")
        cal_va_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_VA_doc.txt")
        cal_net_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_NetAn_Feature_Library.txt")
        cal_ad_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Additional_Documentation_doc.txt")
	cal_ep_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Emergency_procedure_doc.txt")
	cal_om_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Operation_Maintenance_doc.txt")
	cal_usr_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Guide_doc.txt")
	cal_integ_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Integration_doc.txt")
	cal_instructions_doc = file_to_list("/var/www/hitme/app/CALSTORE_Docs/CAL_Instructions_doc.txt")
        ncpi_dev_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/Development_Guide.txt")
        ncpi_app_coverage = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_App_Coverage.txt")
        ncpi_energy = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_Energy_Report.txt")
        ncpi_gsm = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_GSM_Opt_Report.txt")
        ncpi_ims = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_IMS_Capacity_Feature.txt")
        ncpi_3pp = file_to_list("/var/www/hitme/app/NetAn_Docs/3PP.txt")
        ncpi_nr_kpi = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_NR_KPI.txt")
        ncpi_pm_alarm = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_PM_Alarming.txt")
        ncpi_pm_exp = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_PM_Explorer.txt")
        ncpi_ran = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_RAN_Performance.txt")
        ncpi_ran_uplink = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_RAN_Uplink_Interface.txt")
        ncpi_volte = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_VoLTE_Feature.txt")
        ncpi_vowifi = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_VOWIFI.txt")
	ncpi_sag = file_to_list("/var/www/hitme/app/NetAn_Docs/System_Admin_Guide.txt")
        ncpi_video = file_to_list("/var/www/hitme/app/NetAn_Docs/Videos.txt")
	ncpi_trouble = file_to_list("/var/www/hitme/app/NetAn_Docs/Troubleshooting.txt")
	ncpi_pmax_kpi = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_PMAX_KPI.txt")
	ncpi_dcg = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_DCG_Guide.txt")
	ncpi_ta_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/Timing_Advance_Guide.txt")
	ncpi_mini_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_Minilink_Guide.txt")
	ncpi_fac_desc = file_to_list("/var/www/hitme/app/NetAn_Docs/Facility_Description.txt")
	ncpi_nrsa_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_NR_SA_Guide.txt")
	ncpi_voice_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_Voice_NR.txt")
	ncpi_wcdma_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_WCDMA_Guide.txt")
	ncpi_lte_kpi_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_LTE_KPI_Guide.txt")
	ncpi_om_nrup_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_NR_Uplink.txt")
	ncpi_om_cmcc_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_CMCC.txt")
	ncpi_om_rk6k_guide = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_Rt6k_Guide.txt")
	ncpi_om_rk6k_desc = file_to_list("/var/www/hitme/app/NetAn_Docs/OM_Rt6k_Description.txt")
	other_doc_rn = file_to_list("/var/www/hitme/app/Other_Docs/Release_Note_Docs.txt")
        dateofupload = datetime.datetime.now()
        flag=1
        if request.method == 'POST':
                shipment = request.form['shipment']
                category = request.form['category']
                doctype = request.form['doctype']
                doctype = doctype.strip()
                docnum = request.form['docnum']
                docname = request.form['docname']
                link = request.form['link']
                revision = request.form['revision']
                upby = request.form['upby']
                techOwn = request.form['techOwn']
		comments = request.form['comments']
                docnum = docnum.replace(" ", "")

                for line in doc_details_list:
                        if shipment in line and category in line and doctype in line and docnum in line and link in line and revision in line:
                                flag=0
                                message = "The "+docname+" is already uploaded with Revision "+revision+". Please check! "
                                break

                if shipment != "Select Shipment" and doctype != "Select Document Type" and shipment != "none" and doctype != "none" and docnum != "" and docname != "Select Document Title" and docname != "none" and link != "" and revision != "" and upby!= "" and techOwn!= "" and comments!= "" and flag == 1:
                        filename1 = "/var/www/hitme/app/"+category+"_doc_details.txt"
                        doc_details1 = open(filename1,'a')
                        doc_details1.write(shipment+"::::"+doctype+"::::"+docname+"::::"+docnum+"::::"+link+"::::"+revision+"::::"+upby+"::::"+techOwn+"::::"+str(dateofupload)+"::::"+comments+"\n")
                        doc_details.write(shipment+"::::"+doctype+"::::"+docname+"::::"+docnum+"::::"+link+"::::"+revision+"::::"+upby+"::::"+techOwn+"::::"+str(dateofupload)+"::::"+comments+"\n")
                        message = 'Document uploaded successfully!'
                        doc_details1.close()
                        doc_details.close()

                elif shipment == "Select Shipment" or category == "Select Document Category" or doctype == "Select Document type" or shipment == "none" or category == "none" or doctype == "none" or shipment == "" or category == "" or doctype == "" or docnum == "" or docname == "" or link == "" or revision == "" or upby== "":
                        message = 'Some values are empty. Please check!'

        ship_list = file_to_list("/var/www/hitme/app/Shipments.txt")
        return render_template("upload.html", message=message, ship_list=ship_list, doc_list_cpi=json.dumps(doc_list_cpi), doc_list_ncpi=json.dumps(doc_list_ncpi), doc_list_other_docs=json.dumps(doc_list_other_docs), doc_list_calstore=json.dumps(doc_list_calstore), cpi_installation_doc=json.dumps(cpi_installation_doc), cpi_se_doc=json.dumps(cpi_se_doc), cpi_lo_doc=json.dumps(cpi_lo_doc), cpi_po_doc=json.dumps(cpi_po_doc), cpi_tu_doc=json.dumps(cpi_tu_doc), cpi_ug_doc=json.dumps(cpi_ug_doc), cpi_sag_doc=json.dumps(cpi_sag_doc), cpi_bi_doc=json.dumps(cpi_bi_doc), cpi_intf_doc=json.dumps(cpi_intf_doc), cpi_3pp_bo_doc=json.dumps(cpi_3pp_bo_doc), cpi_rhel_doc=json.dumps(cpi_rhel_doc), cpi_ad_doc=json.dumps(cpi_ad_doc), cpi_osd_doc=json.dumps(cpi_osd_doc), cal_dimen_doc=json.dumps(cal_dimen_doc), cal_ii_doc=json.dumps(cal_ii_doc), cal_infra_mws_doc=json.dumps(cal_infra_mws_doc), cal_infra_nas_doc=json.dumps(cal_infra_nas_doc), cal_oss_monitr_doc=json.dumps(cal_oss_monitr_doc), cal_ug_doc=json.dumps(cal_ug_doc), cal_fh_doc=json.dumps(cal_fh_doc), cal_mig_doc=json.dumps(cal_mig_doc), cal_exp_doc=json.dumps(cal_exp_doc), cal_int_doc=json.dumps(cal_int_doc), cal_rl_doc=json.dumps(cal_rl_doc), cal_net_doc=json.dumps(cal_net_doc), cal_ad_doc=json.dumps(cal_ad_doc), cal_ep_doc=json.dumps(cal_ep_doc), cal_om_doc=json.dumps(cal_om_doc), cal_nh_doc=json.dumps(cal_nh_doc), cal_va_doc=json.dumps(cal_va_doc), cal_usr_doc=json.dumps(cal_usr_doc), cal_integ_doc=json.dumps(cal_integ_doc), cal_instructions_doc=json.dumps(cal_instructions_doc), ncpi_3pp=json.dumps(ncpi_3pp), ncpi_ims=json.dumps(ncpi_ims), ncpi_energy=json.dumps(ncpi_energy), ncpi_app_coverage=json.dumps(ncpi_app_coverage), ncpi_dev_guide=json.dumps(ncpi_dev_guide), ncpi_gsm=json.dumps(ncpi_gsm), ncpi_nr_kpi=json.dumps(ncpi_nr_kpi), ncpi_pm_alarm=json.dumps(ncpi_pm_alarm), ncpi_pm_exp=json.dumps(ncpi_pm_exp), ncpi_ran=json.dumps(ncpi_ran), ncpi_ran_uplink=json.dumps(ncpi_ran_uplink), ncpi_volte=json.dumps(ncpi_volte), ncpi_vowifi=json.dumps(ncpi_vowifi), ncpi_sag=json.dumps(ncpi_sag), ncpi_video=json.dumps(ncpi_video), ncpi_trouble=json.dumps(ncpi_trouble), ncpi_pmax_kpi=json.dumps(ncpi_pmax_kpi), ncpi_dcg=json.dumps(ncpi_dcg), ncpi_ta_guide=json.dumps(ncpi_ta_guide), ncpi_mini_guide=json.dumps(ncpi_mini_guide), ncpi_fac_desc=json.dumps(ncpi_fac_desc), ncpi_nrsa_guide=json.dumps(ncpi_nrsa_guide), ncpi_voice_guide=json.dumps(ncpi_voice_guide), ncpi_wcdma_guide=json.dumps(ncpi_wcdma_guide), ncpi_lte_kpi_guide=json.dumps(ncpi_lte_kpi_guide), ncpi_om_nrup_guide=json.dumps(ncpi_om_nrup_guide), ncpi_om_cmcc_guide=json.dumps(ncpi_om_cmcc_guide), ncpi_om_rk6k_guide=json.dumps(ncpi_om_rk6k_guide), ncpi_om_rk6k_desc=json.dumps(ncpi_om_rk6k_desc), other_doc_rn=json.dumps(other_doc_rn))


@app.route("/document_baseline/document_list_main_cpi", methods=['GET','POST'])
def document_list_main_cpi():
        shipm=""
	type=""
        dd=[]
	doc_details_list=[]
	doc_type = "CPI"
        ship_list = file_to_list("/var/www/hitme/app/Shipments.txt")
        doc_type_list_cpi = file_to_list("/var/www/hitme/app/CPI_Doc_Type.txt")
	doc_detail_file = "/var/www/hitme/app/CPI_doc_details.txt"

        if request.method == 'POST':
                shipm = request.form['ship']
		type = request.form['search_type']
                if type == "full":
                        doc_details_list = search_sort_cpi(shipm)
                elif type == "delta":
                        doc_details_list = search_delta_sort(shipm, doc_detail_file, doc_type)
                for doc_t in doc_details_list:
                        dets = doc_t.split("::::")
                        a = doc_t.find(dets[1])
                        doc_t = doc_t[a:]
                        b = doc_t.find('::::')
                        doc_t = doc_t[0:b]
                        dd.append(doc_t)
                dd = list(dict.fromkeys(dd))

        else:
                shipm="None"
                doc_details_list = search_sort_cpi("")

        return render_template("document_list_main_cpi.html", doc_type_list_cpi=doc_type_list_cpi, ship_list=ship_list,doc_details_list=doc_details_list, shipm=shipm, dd=dd, type=type)

@app.route("/document_baseline/document_list_main_calstore", methods=['GET','POST'])
def document_list_main_calstore():
        shipm=""
	type=""
        dd=[]
	doc_details_list=[]
	doc_type = "Calstore"
        ship_list = file_to_list("/var/www/hitme/app/Shipments.txt")
        doc_type_list_calstore = file_to_list("/var/www/hitme/app/CALSTORE_Doc_Type.txt")
	doc_detail_file = "/var/www/hitme/app/CALSTORE_doc_details.txt"

        if request.method == 'POST':
                shipm = request.form['ship']
		type = request.form['search_type']
                if type == "full":
                        doc_details_list = search_sort_cal(shipm)
                elif type == "delta":
                        doc_details_list = search_delta_sort(shipm, doc_detail_file, doc_type)
                for doc_t in doc_details_list:
                        dets = doc_t.split("::::")
                        a = doc_t.find(dets[1])
                        doc_t = doc_t[a:]
                        b = doc_t.find('::::')
                        doc_t = doc_t[0:b]
                        dd.append(doc_t)
                dd = list(dict.fromkeys(dd))

        else:
                shipm="None"
                doc_details_list = search_sort_cal("")

        return render_template("document_list_main_calstore.html", doc_type_list_calstore=doc_type_list_calstore, ship_list=ship_list,doc_details_list=doc_details_list, shipm=shipm, dd=dd, type=type)

@app.route("/document_baseline/document_list_main_ncpi", methods=['GET','POST'])
def document_list_main_ncpi():
        shipm=""
        type=""
	dd=[]
	doc_details_list=[]
	doc_type = "NetAn"
        ship_list = file_to_list("/var/www/hitme/app/Shipments.txt")
        doc_type_list_ncpi = file_to_list("/var/www/hitme/app/NetAn_CPI_Doc_Type.txt")
	doc_detail_file = "/var/www/hitme/app/NetAN_Features_Library_doc_details.txt"

        if request.method == 'POST':
                shipm = request.form['ship']
                type = request.form['search_type']
		if type == "full":
			doc_details_list = search_sort_ncpi(shipm)
		elif type == "delta":
			doc_details_list = search_delta_sort(shipm, doc_detail_file, doc_type)
                for doc_t in doc_details_list:
                        dets = doc_t.split("::::")
                        a = doc_t.find(dets[1])
                        doc_t = doc_t[a:]
                        b = doc_t.find('::::')
                        doc_t = doc_t[0:b]
                        dd.append(doc_t)
                dd = list(dict.fromkeys(dd))

        else:
                shipm="None"
                doc_details_list = search_sort_ncpi("")

        return render_template("document_list_main_ncpi.html", doc_type_list_ncpi=doc_type_list_ncpi, ship_list=ship_list,doc_details_list=doc_details_list, shipm=shipm, dd=dd, type=type)

@app.route("/document_baseline/document_list_main_other_docs", methods=['GET','POST'])
def document_list_main_other_docs():
        shipm=""
	type=""
        dd=[]
	doc_details_list=[]
	doc_type = "Other"
        ship_list = file_to_list("/var/www/hitme/app/Shipments.txt")
        doc_type_list_other_docs = file_to_list("/var/www/hitme/app/Other_Docs_Doc_Type.txt")
	doc_detail_file = "/var/www/hitme/app/Other_Documents_doc_details.txt"

        if request.method == 'POST':
                shipm = request.form['ship']
                type = request.form['search_type']
		if type == "full":
			doc_details_list = search_sort_other_docs(shipm)
		elif type == "delta":
			doc_details_list = search_delta_sort(shipm, doc_detail_file, doc_type)
                for doc_t in doc_details_list:
                        dets = doc_t.split("::::")
                        a = doc_t.find(dets[1])
                        doc_t = doc_t[a:]
                        b = doc_t.find('::::')
                        doc_t = doc_t[0:b]
                        dd.append(doc_t)
                dd = list(dict.fromkeys(dd))

        else:
                shipm="None"
                doc_details_list = search_sort_other_docs("")

        return render_template("document_list_main_other_docs.html", doc_type_list_other_docs=doc_type_list_other_docs, ship_list=ship_list,doc_details_list=doc_details_list, shipm=shipm, dd=dd, type=type)
