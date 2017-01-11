import re
import ast
import csv
import xlwt
import os
import sys


if len(sys.argv) != 3:
    print "performance_log_parser.py log_file mode(0:host, 1:m3)"
    exit() 
    
print sys.argv[0]
f = open(sys.argv[1], 'r')
mode = sys.argv[2]

#f = open("log-netflix_hevcm10pl51-6000fps-16000Kbps-3840x2160-1014520_5033638636-mtr_on-114929.txt", 'r')
#f = open("log-Nepal_Adventures_of_Teamsupertramp-mtr_on-142209.txt", 'r')
#f = open("log-street1_1_4096x2176_fr60_bd10-mtr_on-183028.txt", 'r')
#f = open("log-street1_1_4096x2176_fr60_bd8-mtr_on-182757.txt", 'r')
#f = open("log-uhd_vod_count_down_girl_girl_girl_2nd_02-mtr_on-173354.txt", 'r')
#f = open("log-transformers_4_2014_4k_official_trailer-mtr_on-175016.txt", 'r')
#f = open("log-grass_1_4096X2176_fr60_bd8_sub8X8_l51-mtr_off-182513.txt", 'r')

original_list = list()
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
        if p[0]=='module<end_of_pic>':
        #if p[0]=='rbuf_hold':
            performance_list.append(dict(zip(*[iter(new_list)]*2)))
            original_list.append(dict(zip(*[iter(new_list)]*2)))

'''
Convert Performance Data from hex to deci, and calculate per MB number
'''
x_value = 6
average_x_list_all  = list()

'''
bit rate:
    frm_size, br_30, br_60,
bandwidth:
    rd_bd, wr_bd, all_bd
performance (600M, 700M, 800M):
    hw_cycle, sw_cycle, vpu_cycle, fr_600, fr_700, fr_800
'''

if mode == '0':
    min_list_all        = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    cur_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    min_list_avgx       = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_I          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_P          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_B          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'sw_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'sw_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }

elif mode == '1':
    min_list_all        = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'host_cycle':18300, 'm3_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_all        = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    cur_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    min_list_avgx       = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'host_cycle':18300, 'm3_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_avgx       = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_I          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'host_cycle':18300, 'm3_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_I          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_P          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'host_cycle':18300, 'm3_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_P          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    
    min_list_B          = {'count':0, 'frm_size':12, 'br_30':160, 'br_60':320, 'rd_bd':8192, 'wr_bd':8192, 'all_bd':16384, 'hw_cycle':18300, 'host_cycle':18300, 'm3_cycle':18300, 'vpu_cycle':36600, 'hw_600':240, 'hw_700':240, 'hw_800':240, 't_600':240, 't_700':240, 't_800':240 }
    max_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }
    avg_list_B          = {'count':0, 'frm_size':0, 'br_30':0, 'br_60':0, 'rd_bd':0, 'wr_bd':0, 'all_bd':0, 'hw_cycle':0, 'host_cycle':0, 'm3_cycle':0, 'vpu_cycle':0, 'hw_600':0, 'hw_700':0, 'hw_800':0, 't_600':0, 't_700':0, 't_800':0 }


'''
data for plot
'''
t_600_list = list() # time
t_700_list = list() # time
t_800_list = list() # time

rd_bd_list = list() # read bandwidth

frm_size_list = list()  # frame size


'''
Process Data
'''
# Original
for per_entry in original_list:
    for k,v in per_entry.iteritems():
        if(k!='type'):
            per_entry[k] = int(ast.literal_eval(v))
            
# Real Performance Data
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
    insert value for average x
    '''
    if len(average_x_list_all) == x_value:
        average_x_list_all.pop(0)
    average_x_list_all.append(per_entry)
    
    '''
    deal with all the data get what we need here
        1. add new 
    '''
    if mode == '0':
        per_entry['vpu_cycle']  = per_entry['hw_cycle'] + per_entry['sw_cycle']
    elif mode == '1':
        per_entry['vpu_cycle']  = per_entry['hw_cycle'] + per_entry['host_cycle']
        
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
    
    t_600_list.append(per_entry['t_600'])
    t_700_list.append(per_entry['t_700'])
    t_800_list.append(per_entry['t_800'])
    rd_bd_list.append(per_entry['rd_bd'])
    frm_size_list.append(per_entry['frm_size'])
    
    '''
    deal with average x
    '''
    if len(average_x_list_all) == x_value:
        ''' initial current'''
        for k,v in cur_list_avgx.iteritems():
            cur_list_avgx[k] = 0
        ''' sum x_value '''     
        for i in range(x_value):
            cur_entry = average_x_list_all[i]
            for k,v in cur_list_avgx.iteritems():
                if k!= 'count':
                    cur_list_avgx[k] += cur_entry[k]
        ''' calc average '''
        for k,v in cur_list_avgx.iteritems():
            if k!= 'count':
                cur_list_avgx[k] /= x_value
        
        min_list_avgx['count'] += 1
        max_list_avgx['count'] += 1
        avg_list_avgx['count'] += 1
        for k,v in cur_list_avgx.iteritems():
            if k != 'count':
                if(v < min_list_avgx[k]):   min_list_avgx[k] = v
                if(v > max_list_avgx[k]):   max_list_avgx[k] = v
                avg_list_avgx[k] += v
                    
    '''
    min, max, average
    '''
    min_list_all['count'] += 1
    max_list_all['count'] += 1
    avg_list_all['count'] += 1
    if per_entry['type'] == 'I':
        min_list_I['count'] += 1
        max_list_I['count'] += 1
        avg_list_I['count'] += 1
    if per_entry['type'] == 'P' and per_entry['show_flag']==1:
        min_list_P['count'] += 1
        max_list_P['count'] += 1
        avg_list_P['count'] += 1
    if per_entry['type'] == 'B' or (per_entry['type'] == 'P' and per_entry['show_flag']==0):
        min_list_B['count'] += 1
        max_list_B['count'] += 1
        avg_list_B['count'] += 1  
         
    for k,v in per_entry.iteritems():
        if k != 'count' and avg_list_all.has_key(k):
            if(v < min_list_all[k]):   min_list_all[k] = v
            if(v > max_list_all[k]):   max_list_all[k] = v
            avg_list_all[k] += v                

            if per_entry['type'] == 'I':
                if(v < min_list_I[k]):   min_list_I[k] = v
                if(v > max_list_I[k]):   max_list_I[k] = v
                avg_list_I[k] += v              
        
            if per_entry['type'] == 'P' and per_entry['show_flag']==1:
                if(v < min_list_P[k]):   min_list_P[k] = v
                if(v > max_list_P[k]):   max_list_P[k] = v
                avg_list_P[k] += v  
        
            if per_entry['type'] == 'B' or (per_entry['type'] == 'P' and per_entry['show_flag']==0):
                if(v < min_list_B[k]):   min_list_B[k] = v
                if(v > max_list_B[k]):   max_list_B[k] = v
                avg_list_B[k] += v  
        
'''
calculate average value
'''
if avg_list_all['count'] > 0:
    for k,v in avg_list_all.iteritems():
        if k!='count':
            avg_list_all[k] /= avg_list_all['count']

if avg_list_I['count'] > 0:
    for k,v in avg_list_I.iteritems():
        if k!='count':
            avg_list_I[k] /= avg_list_I['count']

if avg_list_P['count'] > 0:
    for k,v in avg_list_P.iteritems():
        if k!='count':
            avg_list_P[k] /= avg_list_P['count']

if avg_list_B['count'] > 0:
    for k,v in avg_list_B.iteritems():
        if k!='count':
            avg_list_B[k] /= avg_list_B['count']

if avg_list_avgx['count'] > 0:
    for k,v in avg_list_avgx.iteritems():
        if k!='count':
            avg_list_avgx[k] /= avg_list_avgx['count']
    
#for i in performance_list:
#    print i
       
'''
t_600_list = list() # time
t_700_list = list() # time
t_800_list = list() # time
rd_bd_list = list() # read bandwidth
frm_size_list = list()  # frame size       
'''  
    
import numpy as np
from scipy.optimize import curve_fit
import pylab as pl

def func(x, k, l):
    '''
    function (x) = k*x + l            :    return k*x+l
    '''
    return k*x+l

def residuals(p, y, x):
    '''
    residual function
    '''
    return y - func(x, p)

def func2(x, a, b, c):
    '''
    function (x) = a*x^2 + b*x + c    :    return k*x*x + m*x +l
    '''
    return a*x*x + b*x +c

def residuals2(p, y, x):
    
    return y - func2(x, p) 

'''
Get Fit Function
'''
x = np.array(frm_size_list)
y = np.array(t_800_list)
#popt, pcov = curve_fit(func, x, y)
popt, pcov = curve_fit(func2, x, y)
print popt
print pcov
#pl.plot(x, func(x, popt[0], popt[1]), 'r', label='Fit Func: y = %f*x + %f' % (popt[0], popt[1]))
pl.plot(x, func2(x, popt[0], popt[1], popt[2]), '.', label='Fit Func: y = %f*x^2 + %f*x + %f' % (popt[0], popt[1], popt[2]))
'''
plot original 
'''
pl.plot(frm_size_list, t_800_list, '.', label='original values')
'''
plot
'''
pl.xlabel('frame size (Mbits)')
pl.ylabel('decoding time (ms)')
pl.title('frame size - decoding time')
pl.legend()
pl.savefig(file_name+".png")
#pl.show()

 
'''
xls write
'''
import xlsxwriter

workbook = xlsxwriter.Workbook('performance_'+file_name+'.xlsx')

'''
Write Original Data
'''
worksheet = workbook.add_worksheet('original')

if mode == '0':
    orig_list = ['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'rd_bd', 'wr_bd', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free', ' ', 'slcs', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'scu', 'spu1', 'spu2', 'spu3', 'qtu1', 'vcu1', 'vcu2', 'ppu1', 'pfu1', 'fcu1']
elif mode == '1':
    orig_list = ['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'rd_bd', 'wr_bd', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'host_cycle', 'm3_cycle', 'int_lat', 'total', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free', ' ', 'slcs', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'scu', 'spu1', 'spu2', 'spu3', 'qtu1', 'vcu1', 'vcu2', 'ppu1', 'pfu1', 'fcu1']

for header in orig_list:
    col=orig_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.

row=4
for per_entry in original_list:
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
worksheet = workbook.add_worksheet('overview')

if mode == '0':
    overview_list=['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'sw_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'hw_600', 'hw_700', 'hw_800', 't_600', 't_700', 't_800', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']
elif mode == '1':
    overview_list=['pic_num', 'show_flag', 'type', 'width', 'height', 'mbs', 'ints', ' ', 'bits', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'module<so_pic_cfg>', 'module<end_of_pic>', 'host_cycle', 'm3_cycle', 'vpu_cycle', 'int_lat', 'total', ' ', 'hw_600', 'hw_700', 'hw_800', 't_600', 't_700', 't_800', ' ', 'rbuf_hold', 'rbuf_free', 'dbuf_hold', 'dbuf_free',' ', 'spu', 'qtu', 'mvu', 'vcu', 'ppu', 'fcu', 'pfu', 'slcs', 'vcu2', 'vcu1', 'scu', 'spu2', 'spu3', 'pfu1', 'spu1', 'ppu1', 'qtu1', 'fcu1']
    
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

if mode == '0':
    summay_list = [' ', ' ', 'count', ' ', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'sw_cycle', 'vpu_cycle', ' ', 'hw_600', 'hw_700', 'hw_800', ' ', 't_600', 't_700', 't_800']
elif mode == '1':
    summay_list = [' ', ' ', 'count', ' ', 'frm_size', 'br_30', 'br_60', ' ', 'rd_bd', 'wr_bd', 'all_bd', ' ', 'hw_cycle', 'host_cycle', 'm3_cycle', 'vpu_cycle', ' ', 'hw_600', 'hw_700', 'hw_800', ' ', 't_600', 't_700', 't_800']
    
for header in summay_list:
    col=summay_list.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.
    
row = 2
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
row +=1

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
row +=1

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
row +=1

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

worksheet.write_string(row, 1, str(x_value)+('_avg_min'))
for _key, _value in min_list_avgx.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

worksheet.write_string(row, 1, str(x_value)+('_avg_max'))
for _key, _value in max_list_avgx.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1
    
worksheet.write_string(row, 1, str(x_value)+('_avg_avg'))
for _key, _value in avg_list_avgx.items():
    col = summay_list.index(_key)
    worksheet.write_number(row, col, float(_value))
row +=1

'''
Write Fit Image
'''
worksheet = workbook.add_worksheet('Fit Function(frm_size-time)')

worksheet.write_string(0, 1, 'a')
worksheet.write_number(1, 1, popt[0])
worksheet.write_string(0, 2, 'b')
worksheet.write_number(1, 2, popt[1])
worksheet.write_string(0, 3, 'c')
worksheet.write_number(1, 3, popt[2])

row = 3
worksheet.write_string(row, 0, 'covariance')
for i in pcov:
    col = 1
    for j in i:
        worksheet.write_number(row, col, j)
        col +=1
    row += 1
    
worksheet.insert_image('F7', file_name+".png")


'''
Write Simulation
'''
'''
Freq            = 600000000.0
Buf_Num         = 16
Frm_R_Target    = 60
Dis_Interval    = 1.0 / Frm_R_Target
worksheet = workbook.add_worksheet('Sim-F(%dMHz)-B(%d)-T(%d)' % (Freq, Buf_Num, Frm_R_Target))

Sim_header = ['', 'Time', ' ', 'V4G_Out', 'Dis_Free', ' ', 'Buf_Num', 'V4G_Buf', 'Sys_Buf', 'Valid_DBuf']

Simulation = {'Time':0.0, 'V4G_Out':0, 'Display':0, 'Buf_Num':Buf_Num, 'V4G_Buf':0, 'Sys_Buf':0, 'Valid_DBuf':0}


for header in Sim_header:
    col=Sim_header.index(header)  # we are keeping order.
    worksheet.write(0, col, header) # we have written first row which is the header of worksheet also.
'''    
'''
    Simulation Start --->
'''    
'''
print "freqency: %f, total buffer number:%d, target frame rate: %d, display interval: %f" % (Freq, Buf_Num, Frm_R_Target, Dis_Interval)

Sim_List = list()

prev_sim = Simulation
next_disp_time = Dis_Interval
step = 0    # 0: wait for buffer full 1: real start
for per_entry in original_list:
    cur_sim = Simulation
    if mode == '0':
        cur_time_consume = float((per_entry['hw_cycle'] + per_entry['sw_cycle'])/Freq)
    elif mode == '1':
        cur_time_consume = float(per_entry['host_cycle']/Freq)
        
    cur_sim['Time'] = prev_sim['Time'] + cur_time_consume;

    if step==0:
        cur_sim['V4G_Out'] = per_entry['dbuf_free']
        cur_sim['V4G_Buf'] = per_entry['rbuf_hold']
        cur_sim['Valid_DBuf'] = prev_sim['Valid_DBuf'] + per_entry['dbuf_free']
        cur_sim['Sys_Buf'] = Buf_Num - cur_sim['V4G_Buf'] - cur_sim['Valid_DBuf']
        
        if cur_sim['Sys_Buf'] == 1: 
            step = 1
            next_disp_time += cur_sim['Time']
            #print next_disp_time
    else:
        pass
    
    #print cur_sim
    
    Sim_List.append(cur_sim)
    prev_sim = cur_sim

'''
'''
    Simulation End --->
''' 


'''
Clean
'''
workbook.close()
os.remove(file_name+".png")
pl.close()
f.close()











