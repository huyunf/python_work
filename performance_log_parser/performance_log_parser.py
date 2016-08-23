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

'''
bit rate:
    frm_size, br_30, br_60,
bandwidth:
    rd_bd, wr_bd, all_bd
performance (600M, 700M, 800M):
    hw_cycle, sw_cycle, vpu_cycle, fr_600, fr_700, fr_800
'''
min_list_all        = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
max_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
avg_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }

min_list_I          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
max_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
avg_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }

min_list_P          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
max_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
avg_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }

min_list_B          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
max_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
avg_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }

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
    per_entry['vpu_cycle']  = per_entry['hw_cycle'] + per_entry['sw_cycle']
    per_entry['frm_size']   = float(format((per_entry['bits'] * mb_num) / (1024*1024), '.04f'))
    per_entry['br_30']      = per_entry['frm_size'] * 30
    per_entry['br_60']      = per_entry['frm_size'] * 60
    per_entry['all_bd']     = per_entry['wr_bd'] + per_entry['rd_bd']
    
    per_entry['hw_600']     = (per_entry['hw_cycle']*mb_num) / 600000.0
    per_entry['hw_700']     = (per_entry['hw_cycle']*mb_num) / 700000.0
    per_entry['hw_800']     = (per_entry['hw_cycle']*mb_num) / 800000.0
    
    per_entry['t_600']      = (per_entry['vpu_cycle']*mb_num) / 600000.0
    per_entry['t_700']      = (per_entry['vpu_cycle']*mb_num) / 700000.0
    per_entry['t_800']      = (per_entry['vpu_cycle']*mb_num) / 800000.0
    
    '''
    min, max, average
    '''
    min_list_all['count'] += 1
    if(per_entry['frm_size'] < min_list_all['frm_size']):   min_list_all['frm_size'] = per_entry['frm_size']
    if(per_entry['br_30'] < min_list_all['br_30']):         min_list_all['br_30'] = per_entry['br_30']
    if(per_entry['br_60'] < min_list_all['br_60']):         min_list_all['br_60'] = per_entry['br_60']       
    if(per_entry['rd_bd'] < min_list_all['rd_bd']):         min_list_all['rd_bd'] = per_entry['rd_bd']     
    if(per_entry['wr_bd'] < min_list_all['wr_bd']):         min_list_all['wr_bd'] = per_entry['wr_bd']
    if(per_entry['all_bd'] < min_list_all['all_bd']):       min_list_all['all_bd'] = per_entry['all_bd']
        
    if(per_entry['hw_cycle'] < min_list_all['hw_cycle']):   min_list_all['hw_cycle'] = per_entry['hw_cycle']
    if(per_entry['sw_cycle'] < min_list_all['sw_cycle']):   min_list_all['sw_cycle'] = per_entry['sw_cycle']
    if(per_entry['vpu_cycle'] < min_list_all['vpu_cycle']): min_list_all['vpu_cycle'] = per_entry['vpu_cycle']   
    
    if(per_entry['t_600'] < min_list_all['t_600']):         min_list_all['t_600'] = per_entry['t_600']     
    if(per_entry['t_700'] < min_list_all['t_700']):         min_list_all['t_700'] = per_entry['t_700']
    if(per_entry['t_800'] < min_list_all['t_800']):         min_list_all['t_800'] = per_entry['t_800']     

    if(per_entry['hw_600'] < min_list_all['hw_600']):       min_list_all['hw_600'] = per_entry['hw_600']     
    if(per_entry['hw_700'] < min_list_all['hw_700']):       min_list_all['hw_700'] = per_entry['hw_700']
    if(per_entry['hw_800'] < min_list_all['hw_800']):       min_list_all['hw_800'] = per_entry['hw_800']   
    
    max_list_all['count'] += 1
    if(per_entry['frm_size'] > max_list_all['frm_size']):   max_list_all['frm_size'] = per_entry['frm_size']
    if(per_entry['br_30'] > max_list_all['br_30']):         max_list_all['br_30'] = per_entry['br_30']
    if(per_entry['br_60'] > max_list_all['br_60']):         max_list_all['br_60'] = per_entry['br_60']       
    if(per_entry['rd_bd'] > max_list_all['rd_bd']):         max_list_all['rd_bd'] = per_entry['rd_bd']     
    if(per_entry['wr_bd'] > max_list_all['wr_bd']):         max_list_all['wr_bd'] = per_entry['wr_bd']
    if(per_entry['all_bd'] > max_list_all['all_bd']):       max_list_all['all_bd'] = per_entry['all_bd']
        
    if(per_entry['hw_cycle'] > max_list_all['hw_cycle']):   max_list_all['hw_cycle'] = per_entry['hw_cycle']
    if(per_entry['sw_cycle'] > max_list_all['sw_cycle']):   max_list_all['sw_cycle'] = per_entry['sw_cycle']
    if(per_entry['vpu_cycle'] > max_list_all['vpu_cycle']): max_list_all['vpu_cycle'] = per_entry['vpu_cycle']   
    
    if(per_entry['t_600'] > max_list_all['t_600']):         max_list_all['t_600'] = per_entry['t_600']     
    if(per_entry['t_700'] > max_list_all['t_700']):         max_list_all['t_700'] = per_entry['t_700']
    if(per_entry['t_800'] > max_list_all['t_800']):         max_list_all['t_800'] = per_entry['t_800']     

    if(per_entry['hw_600'] > max_list_all['hw_600']):       max_list_all['hw_600'] = per_entry['hw_600']     
    if(per_entry['hw_700'] > max_list_all['hw_700']):       max_list_all['hw_700'] = per_entry['hw_700']
    if(per_entry['hw_800'] > max_list_all['hw_800']):       max_list_all['hw_800'] = per_entry['hw_800'] 
    
    
    avg_list_all['count'] += 1
    avg_list_all['frm_size'] += per_entry['frm_size']
    avg_list_all['br_30'] += per_entry['br_30']
    avg_list_all['br_60'] += per_entry['br_60']       
    avg_list_all['rd_bd'] += per_entry['rd_bd']     
    avg_list_all['wr_bd'] += per_entry['wr_bd']
    avg_list_all['all_bd'] += per_entry['all_bd']
    avg_list_all['hw_cycle'] += per_entry['hw_cycle']
    avg_list_all['sw_cycle'] += per_entry['sw_cycle']
    avg_list_all['vpu_cycle'] += per_entry['vpu_cycle']   
    avg_list_all['t_600'] += per_entry['t_600']     
    avg_list_all['t_700'] += per_entry['t_700']
    avg_list_all['t_800'] += per_entry['t_800']     
    avg_list_all['hw_600'] += per_entry['hw_600']     
    avg_list_all['hw_700'] += per_entry['hw_700']
    avg_list_all['hw_800'] += per_entry['hw_800']
    
    '''
    average 5
    '''

avg_list_all['frm_size']    /= avg_list_all['count']
avg_list_all['br_30']       /= avg_list_all['count']
avg_list_all['br_60']       /= avg_list_all['count']
avg_list_all['rd_bd']       /= avg_list_all['count']
avg_list_all['wr_bd']       /= avg_list_all['count']
avg_list_all['all_bd']      /= avg_list_all['count']
avg_list_all['hw_cycle']    /= avg_list_all['count']
avg_list_all['sw_cycle']    /= avg_list_all['count']
avg_list_all['vpu_cycle']   /= avg_list_all['count']
avg_list_all['t_600']       /= avg_list_all['count']
avg_list_all['t_700']       /= avg_list_all['count']
avg_list_all['t_800']       /= avg_list_all['count']
avg_list_all['hw_600']      /= avg_list_all['count'] 
avg_list_all['hw_700']      /= avg_list_all['count']
avg_list_all['hw_800']      /= avg_list_all['count']
        
        
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
    fieldnames = ['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', 'bits', ' ', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']
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

overview_list=['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'hw_600', 'hw_700', 'hw_800', 't_600', 't_700', 't_800', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']

for header in overview_list:
    col=overview_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in performance_list:
    for _key,_value in per_entry.items():
        col = overview_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row

'''
Write Summary
'''
worksheet = workbook.add_worksheet('summary')

summay_list = [' ', ' ', 'count', ' ', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'sw_cycle', 'vpu_cycle', ' ', 'hw_600', 'hw_700', 'hw_800', ' ', 't_600', 't_700', 't_800']

for header in summay_list:
    col=summay_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.
    
row = 3
worksheet.write_string(row, 1, 'all_min')
for _key, _value in min_list_all.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

worksheet.write_string(row, 1, 'all_max')
for _key, _value in max_list_all.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1
    
worksheet.write_string(row, 1, 'all_avg')
for _key, _value in avg_list_all.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=2

worksheet.write_string(row, 1, 'I_min')
for _key, _value in min_list_I.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

worksheet.write_string(row, 1, 'I_max')
for _key, _value in max_list_I.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1
    
worksheet.write_string(row, 1, 'I_avg')
for _key, _value in avg_list_I.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=2

worksheet.write_string(row, 1, 'P_min')
for _key, _value in min_list_P.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

worksheet.write_string(row, 1, 'P_max')
for _key, _value in max_list_P.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1
    
worksheet.write_string(row, 1, 'P_avg')
for _key, _value in avg_list_P.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=2

worksheet.write_string(row, 1, 'B_min')
for _key, _value in min_list_B.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

worksheet.write_string(row, 1, 'B_max')
for _key, _value in max_list_B.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1
    
worksheet.write_string(row, 1, 'B_avg')
for _key, _value in avg_list_B.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

workbook.close()
    














