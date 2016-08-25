import re
import ast
import csv
import xlwt
import os
import sys
import xlsxwriter


performance_entry = {'stream name':'', 'width':0, 'height':0, 'mbs':0, 'rd_bd':0, 'wr_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'total':0}
performance_worksheet_h  = [' ', ' ', 'stream name', 'width', 'height', 'mbs', 'rd_bd', 'wr_bd', 'hw_cycle', 'sw_cycle', 'total']

def func(worksheet, curf, row):
    
    performance_list = list()
    
    for test_line in curf:
        l = re.split(r'[:,\s]\s*', test_line)
        if l[0]=='VXG' and l[1]=='START':
            file_name = l[4]
        if l[0]=='@perf>>':
            p = [i for i in l if (i!='@perf>>' and i!='')]
            if p[0]=='pic_num':
                new_list = list()
            new_list = new_list + p
            if p[0]=='rbuf_hold':
                performance_list.append(dict(zip(*[iter(new_list)]*2)))
    
    count = 0
    sheet_entry = performance_entry
    sheet_entry['stream name'] = file_name

    for per_entry in performance_list:
        mb_num = float(ast.literal_eval(per_entry['mbs']))
        for k,v in per_entry.iteritems():
            if(k!='type'):
                per_entry[k] = float(ast.literal_eval(v))
            if(k!='type' and k!='pic_num' and k!='show_flag' and k!='width' and k!='height' and k!='mbs' and k!='ints' and k!='rbuf_hold' and k!='rbuf_free' and k!='dbuf_hold' and k!='dbuf_free'):
                if(k=='wr_bd' or k=='rd_bd'):
                    #per_entry[k] = float(format(per_entry[k] * 16 / mb_num, '.04f'))
                    per_entry[k] = int(per_entry[k] * 16)
                else:
                    #per_entry[k] = float(format(per_entry[k] / mb_num, '.04f'))
                    per_entry[k] = int(per_entry[k])
                    
            if sheet_entry.has_key(k):
                if k=='width' or k=='height' or k=='mbs':
                    sheet_entry[k] = per_entry[k]
                else:
                    sheet_entry[k] += per_entry[k]
        count += 1
    
    for k,v in sheet_entry.iteritems():
        if k != 'stream name' and k!='width' and k!='height' and k!='mbs':
            sheet_entry[k] /= count 
    
    for _key,_value in sheet_entry.items():
        col = performance_worksheet_h.index(_key)
        if _key=='stream name':
            worksheet.write_string(row, col, _value)
        else:
            worksheet.write_number(row, col, float(_value))
                    
    
    
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Command Line Wrong!\n"
        print "Command Line Usage: performance_log_group [dir]"
        exit(0)
    '''
    prepare worksheet
    '''
    workbook = xlsxwriter.Workbook('performane.xlsx')
    worksheet = workbook.add_worksheet('overview')
    
    '''
    Write header
    '''
    row = 2
    for header in performance_worksheet_h:
        col=performance_worksheet_h.index(header)  # we are keeping order.
        worksheet.write(row, col, header) # we have written first row which is the header of worksheet also.
    row += 1
    '''
    walk every file to collect data and write int worksheet
    '''
    rootDir = sys.argv[1]
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\tProcessing %s' % dirName+'\\'+fname)
            fn = open(dirName+'\\'+fname, 'r')
            func(worksheet, fn, row)
            row += 1
            #fn.close()
           
    #fn = open('a\log-uhd_vod_count_down_girl_girl_girl_2nd_02-mtr_on-173354.txt', 'r')
    #func(worksheet, fn, row)    
        
    workbook.close()