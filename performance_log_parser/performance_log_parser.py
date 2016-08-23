import re
import ast
import csv
import xlwt

f = open("log-netflix_hevcm10pl51-6000fps-16000Kbps-3840x2160-1014520_5033638636-mtr_on-114929.txt", 'r')

performance_list = list()

'''
Read Log file and form dictionary
'''
for test_line in f:
    l = re.split(r'[:,\s]\s*', test_line)
    if l[0]=='VXG' and l[1]=='START':
        file_name = l[4]
    if l[0]=='@perf>>':
        p = [i for i in l if (i!='@perf>>' and i!='')]
        if p[0]=='pic_num':
            new_list = list()
        new_list = new_list + p
        #if p[0]=='module<end_of_pic>':
        if p[0]=='rbuf_hold':
            performance_list.append(dict(zip(*[iter(new_list)]*2)))
            


'''
Convert Performance Data from hex to deci, and calculate per MB number
'''
average_5_list_all  = list()
average_5_list_I    = list()
average_5_list_P    = list()
average_5_list_B    = list()
for per_entry in performance_list:
    mb_num = float(ast.literal_eval(per_entry['mbs']))
    for k,v in per_entry.iteritems():
        if(k!='type'):
            per_entry[k] = float(ast.literal_eval(v))
        if(k!='type' and k!='pic_num' and k!='show_flag' and k!='width' and k!='height' and k!='mbs' and k!='ints' and k!='rbuf_hold' and k!='rbuf_free' and k!='dbuf_hold' and k!='dbuf_free'):
            if(k=='wr_bd' or k=='rd_bd'):
                per_entry[k] = float(format(per_entry[k] * 16 / mb_num, '.04f'))
            else:
                per_entry[k] = float(format(per_entry[k] / mb_num, '.04f'))
    '''
    deal with all the data get what we need here
    '''
    per_entry['vpu_cycle'] = per_entry['hw_cycle'] + per_entry['sw_cycle']
    
    '''
    min, max, average
    '''
     
    '''
    average 5
    '''
    
        
        
#for i in performance_list:
#    print i
       
'''
get Min, Max, Average, Average5 value of (I, P, B, all)
    1. bit-rate 
    2. bandwidth
    3. hw_cycle, hw_cycle+sw_cycle
    4. time per frame
'''



'''
Write data into csv file

with open('performance.csv', 'w') as csvfile:
    fieldnames = ['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', 'bits', 'rd_bd', 'wr_bd',' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
    
    writer.writeheader()
    for i in performance_list:
        writer.writerow(i)
'''
            
'''
xls write
'''
import xlsxwriter

workbook = xlsxwriter.Workbook('performane_'+file_name+'.xlsx')

'''
Write Overview
'''
worksheet = workbook.add_worksheet('overview')

ordered_list=['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', 'bits', 'rd_bd', 'wr_bd',' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']

for header in ordered_list:
    col=ordered_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in performance_list:
    for _key,_value in per_entry.items():
        col = ordered_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row
    

'''
Write Bandwidth
'''

'''
Write Bit-rate
'''

'''
Write Performance
'''
    
workbook.close()
    














