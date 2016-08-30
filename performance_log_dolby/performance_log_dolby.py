import re
import ast
import csv
import xlwt
import os
import sys


if len(sys.argv) != 2:
    print "performance_log_dolby.py log_file"
    exit() 
    
print sys.argv[0]
f = open(sys.argv[1], 'r')

original_BL_list = list()
original_EL_list = list()
performance_BL_list = list()
performance_EL_list = list()

BL_width = '0'
EL_width = '0'

file_name = "current_stream"

'''
Read Log file and form dictionary
'''
for test_line in f:
    l = re.split(r'[:,\s]\s*', test_line)
    if l[0]=='@perf>>':
        p = [i for i in l if (i!='@perf>>' and i!='')]
        if p[0]=='pic_num':
            new_list = list()
        new_list = new_list + p
        if p[0]=='module<end_of_pic>':
            cur = dict(zip(*[iter(new_list)]*2))
            if BL_width=='0' or BL_width==cur['width']:
                BL_width = cur['width']
                performance_BL_list.append(dict(zip(*[iter(new_list)]*2)))
                original_BL_list.append(dict(zip(*[iter(new_list)]*2)))
            elif EL_width=='0' or EL_width==cur['width']:
                EL_width = cur['width']
                performance_EL_list.append(dict(zip(*[iter(new_list)]*2)))
                original_EL_list.append(dict(zip(*[iter(new_list)]*2)))

'''
Process Data
'''
# Original Base layer
for per_entry in original_BL_list:
    for k,v in per_entry.iteritems():
        if(k!='type'):
            per_entry[k] = int(ast.literal_eval(v))
            
# Real Performance Data Base layer
for per_entry in performance_BL_list:
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
    per_entry['frm_size']   = float(format((per_entry['bits'] * mb_num) / (1024*1024), '.04f'))     # Mbits
    per_entry['br_30']      = float(format(per_entry['frm_size'] * 30, '.04f'))                     # Mbps
    per_entry['br_60']      = float(format(per_entry['frm_size'] * 60, '.04f'))                     # Mbps
    per_entry['all_bd']     = float(format(per_entry['wr_bd'] + per_entry['rd_bd'], '.04f'))
    
    per_entry['hw_600']     = float(format((per_entry['hw_cycle']*mb_num) / 600000.0, '.04f'))      # ms
    per_entry['hw_700']     = float(format((per_entry['hw_cycle']*mb_num) / 700000.0, '.04f'))      # ms
    per_entry['hw_800']     = float(format((per_entry['hw_cycle']*mb_num) / 800000.0, '.04f'))      # ms
    
    per_entry['t_600']      = float(format((per_entry['vpu_cycle']*mb_num) / 600000.0, '.04f'))     # ms
    per_entry['t_700']      = float(format((per_entry['vpu_cycle']*mb_num) / 700000.0, '.04f'))     # ms
    per_entry['t_800']      = float(format((per_entry['vpu_cycle']*mb_num) / 800000.0, '.04f'))     # ms


# Original Enhance layer
for per_entry in original_EL_list:
    for k,v in per_entry.iteritems():
        if(k!='type'):
            per_entry[k] = int(ast.literal_eval(v))
            
# Real Performance Data Enhance layer
for per_entry in performance_EL_list:
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
    per_entry['frm_size']   = float(format((per_entry['bits'] * mb_num) / (1024*1024), '.04f'))     # Mbits
    per_entry['br_30']      = float(format(per_entry['frm_size'] * 30, '.04f'))                     # Mbps
    per_entry['br_60']      = float(format(per_entry['frm_size'] * 60, '.04f'))                     # Mbps
    per_entry['all_bd']     = float(format(per_entry['wr_bd'] + per_entry['rd_bd'], '.04f'))
    
    per_entry['hw_600']     = float(format((per_entry['hw_cycle']*mb_num) / 600000.0, '.04f'))      # ms
    per_entry['hw_700']     = float(format((per_entry['hw_cycle']*mb_num) / 700000.0, '.04f'))      # ms
    per_entry['hw_800']     = float(format((per_entry['hw_cycle']*mb_num) / 800000.0, '.04f'))      # ms
    
    per_entry['t_600']      = float(format((per_entry['vpu_cycle']*mb_num) / 600000.0, '.04f'))     # ms
    per_entry['t_700']      = float(format((per_entry['vpu_cycle']*mb_num) / 700000.0, '.04f'))     # ms
    per_entry['t_800']      = float(format((per_entry['vpu_cycle']*mb_num) / 800000.0, '.04f'))     # ms
       
'''
xls write
'''
import xlsxwriter

workbook = xlsxwriter.Workbook('performance_'+file_name+'.xlsx')

'''
Write Original Data
'''
orig_list = ['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'rd_bd', 'wr_bd', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free', ' ', 'slcs', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'scu', 'spu1', 'spu2', 'spu3', 'qtu1', 'vcu1', 'vcu2', 'ppu1', 'pfu1', 'fcu1']

worksheet = workbook.add_worksheet('original_BL')

for header in orig_list:
    col=orig_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in original_BL_list:
    for _key,_value in per_entry.items():
        col = orig_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row


worksheet = workbook.add_worksheet('original_EL')

for header in orig_list:
    col=orig_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in original_EL_list:
    for _key,_value in per_entry.items():
        col = orig_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row
    
'''
Write Overview
'''
overview_list=['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'hw_600', 'hw_700', 'hw_800', 't_600', 't_700', 't_800', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']

worksheet = workbook.add_worksheet('overview_BL')

for header in overview_list:
    col=overview_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in performance_BL_list:
    for _key,_value in per_entry.items():
        col = overview_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row


worksheet = workbook.add_worksheet('overview_EL')

for header in overview_list:
    col=overview_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in performance_EL_list:
    for _key,_value in per_entry.items():
        col = overview_list.index(_key)
        if _key=='type':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
    row+=1 #enter the next row

'''
Clean
'''
workbook.close()
f.close()











