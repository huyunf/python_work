import re
import ast
import csv
import xlwt

f = open("log-netflix_hevcm10pl51-6000fps-16000Kbps-3840x2160-1014520_5033638636-mtr_on-114929.txt", 'r')
#f = open("log-Nepal_Adventures_of_Teamsupertramp-mtr_on-142209.txt", 'r')

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
x_value = 5
average_x_list_all  = list()

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
        if(cur_list_avgx['frm_size'] < min_list_avgx['frm_size']):   min_list_avgx['frm_size'] = cur_list_avgx['frm_size']
        if(cur_list_avgx['br_30'] < min_list_avgx['br_30']):         min_list_avgx['br_30'] = cur_list_avgx['br_30']
        if(cur_list_avgx['br_60'] < min_list_avgx['br_60']):         min_list_avgx['br_60'] = cur_list_avgx['br_60']       
        if(cur_list_avgx['rd_bd'] < min_list_avgx['rd_bd']):         min_list_avgx['rd_bd'] = cur_list_avgx['rd_bd']     
        if(cur_list_avgx['wr_bd'] < min_list_avgx['wr_bd']):         min_list_avgx['wr_bd'] = cur_list_avgx['wr_bd']
        if(cur_list_avgx['all_bd'] < min_list_avgx['all_bd']):       min_list_avgx['all_bd'] = cur_list_avgx['all_bd']
            
        if(cur_list_avgx['hw_cycle'] < min_list_avgx['hw_cycle']):   min_list_avgx['hw_cycle'] = cur_list_avgx['hw_cycle']
        if(cur_list_avgx['sw_cycle'] < min_list_avgx['sw_cycle']):   min_list_avgx['sw_cycle'] = cur_list_avgx['sw_cycle']
        if(cur_list_avgx['vpu_cycle'] < min_list_avgx['vpu_cycle']): min_list_avgx['vpu_cycle'] = cur_list_avgx['vpu_cycle']   
        
        if(cur_list_avgx['t_600'] < min_list_avgx['t_600']):         min_list_avgx['t_600'] = cur_list_avgx['t_600']     
        if(cur_list_avgx['t_700'] < min_list_avgx['t_700']):         min_list_avgx['t_700'] = cur_list_avgx['t_700']
        if(cur_list_avgx['t_800'] < min_list_avgx['t_800']):         min_list_avgx['t_800'] = cur_list_avgx['t_800']     
    
        if(cur_list_avgx['hw_600'] < min_list_avgx['hw_600']):       min_list_avgx['hw_600'] = cur_list_avgx['hw_600']     
        if(cur_list_avgx['hw_700'] < min_list_avgx['hw_700']):       min_list_avgx['hw_700'] = cur_list_avgx['hw_700']
        if(cur_list_avgx['hw_800'] < min_list_avgx['hw_800']):       min_list_avgx['hw_800'] = cur_list_avgx['hw_800']   
        
        max_list_avgx['count'] += 1
        if(cur_list_avgx['frm_size'] > max_list_avgx['frm_size']):   max_list_avgx['frm_size'] = cur_list_avgx['frm_size']
        if(cur_list_avgx['br_30'] > max_list_avgx['br_30']):         max_list_avgx['br_30'] = cur_list_avgx['br_30']
        if(cur_list_avgx['br_60'] > max_list_avgx['br_60']):         max_list_avgx['br_60'] = cur_list_avgx['br_60']       
        if(cur_list_avgx['rd_bd'] > max_list_avgx['rd_bd']):         max_list_avgx['rd_bd'] = cur_list_avgx['rd_bd']     
        if(cur_list_avgx['wr_bd'] > max_list_avgx['wr_bd']):         max_list_avgx['wr_bd'] = cur_list_avgx['wr_bd']
        if(cur_list_avgx['all_bd'] > max_list_avgx['all_bd']):       max_list_avgx['all_bd'] = cur_list_avgx['all_bd']
            
        if(cur_list_avgx['hw_cycle'] > max_list_avgx['hw_cycle']):   max_list_avgx['hw_cycle'] = cur_list_avgx['hw_cycle']
        if(cur_list_avgx['sw_cycle'] > max_list_avgx['sw_cycle']):   max_list_avgx['sw_cycle'] = cur_list_avgx['sw_cycle']
        if(cur_list_avgx['vpu_cycle'] > max_list_avgx['vpu_cycle']): max_list_avgx['vpu_cycle'] = cur_list_avgx['vpu_cycle']   
        
        if(cur_list_avgx['t_600'] > max_list_avgx['t_600']):         max_list_avgx['t_600'] = cur_list_avgx['t_600']     
        if(cur_list_avgx['t_700'] > max_list_avgx['t_700']):         max_list_avgx['t_700'] = cur_list_avgx['t_700']
        if(cur_list_avgx['t_800'] > max_list_avgx['t_800']):         max_list_avgx['t_800'] = cur_list_avgx['t_800']     
    
        if(cur_list_avgx['hw_600'] > max_list_avgx['hw_600']):       max_list_avgx['hw_600'] = cur_list_avgx['hw_600']     
        if(cur_list_avgx['hw_700'] > max_list_avgx['hw_700']):       max_list_avgx['hw_700'] = cur_list_avgx['hw_700']
        if(cur_list_avgx['hw_800'] > max_list_avgx['hw_800']):       max_list_avgx['hw_800'] = cur_list_avgx['hw_800'] 
        
        
        avg_list_avgx['count'] += 1
        avg_list_avgx['frm_size'] += cur_list_avgx['frm_size']
        avg_list_avgx['br_30'] += cur_list_avgx['br_30']
        avg_list_avgx['br_60'] += cur_list_avgx['br_60']       
        avg_list_avgx['rd_bd'] += cur_list_avgx['rd_bd']     
        avg_list_avgx['wr_bd'] += cur_list_avgx['wr_bd']
        avg_list_avgx['all_bd'] += cur_list_avgx['all_bd']
        avg_list_avgx['hw_cycle'] += cur_list_avgx['hw_cycle']
        avg_list_avgx['sw_cycle'] += cur_list_avgx['sw_cycle']
        avg_list_avgx['vpu_cycle'] += cur_list_avgx['vpu_cycle']   
        avg_list_avgx['t_600'] += cur_list_avgx['t_600']     
        avg_list_avgx['t_700'] += cur_list_avgx['t_700']
        avg_list_avgx['t_800'] += cur_list_avgx['t_800']     
        avg_list_avgx['hw_600'] += cur_list_avgx['hw_600']     
        avg_list_avgx['hw_700'] += cur_list_avgx['hw_700']
        avg_list_avgx['hw_800'] += cur_list_avgx['hw_800']
        
                    
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
    
    if per_entry['type'] == 'I':
        min_list_I['count'] += 1
        if(per_entry['frm_size'] < min_list_I['frm_size']):   min_list_I['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] < min_list_I['br_30']):         min_list_I['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] < min_list_I['br_60']):         min_list_I['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] < min_list_I['rd_bd']):         min_list_I['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] < min_list_I['wr_bd']):         min_list_I['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] < min_list_I['all_bd']):       min_list_I['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] < min_list_I['hw_cycle']):   min_list_I['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] < min_list_I['sw_cycle']):   min_list_I['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] < min_list_I['vpu_cycle']): min_list_I['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] < min_list_I['t_600']):         min_list_I['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] < min_list_I['t_700']):         min_list_I['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] < min_list_I['t_800']):         min_list_I['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] < min_list_I['hw_600']):       min_list_I['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] < min_list_I['hw_700']):       min_list_I['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] < min_list_I['hw_800']):       min_list_I['hw_800'] = per_entry['hw_800']   
        
        max_list_I['count'] += 1
        if(per_entry['frm_size'] > max_list_I['frm_size']):   max_list_I['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] > max_list_I['br_30']):         max_list_I['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] > max_list_I['br_60']):         max_list_I['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] > max_list_I['rd_bd']):         max_list_I['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] > max_list_I['wr_bd']):         max_list_I['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] > max_list_I['all_bd']):       max_list_I['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] > max_list_I['hw_cycle']):   max_list_I['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] > max_list_I['sw_cycle']):   max_list_I['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] > max_list_I['vpu_cycle']): max_list_I['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] > max_list_I['t_600']):         max_list_I['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] > max_list_I['t_700']):         max_list_I['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] > max_list_I['t_800']):         max_list_I['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] > max_list_I['hw_600']):       max_list_I['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] > max_list_I['hw_700']):       max_list_I['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] > max_list_I['hw_800']):       max_list_I['hw_800'] = per_entry['hw_800'] 
        
        
        avg_list_I['count'] += 1
        avg_list_I['frm_size'] += per_entry['frm_size']
        avg_list_I['br_30'] += per_entry['br_30']
        avg_list_I['br_60'] += per_entry['br_60']       
        avg_list_I['rd_bd'] += per_entry['rd_bd']     
        avg_list_I['wr_bd'] += per_entry['wr_bd']
        avg_list_I['all_bd'] += per_entry['all_bd']
        avg_list_I['hw_cycle'] += per_entry['hw_cycle']
        avg_list_I['sw_cycle'] += per_entry['sw_cycle']
        avg_list_I['vpu_cycle'] += per_entry['vpu_cycle']   
        avg_list_I['t_600'] += per_entry['t_600']     
        avg_list_I['t_700'] += per_entry['t_700']
        avg_list_I['t_800'] += per_entry['t_800']     
        avg_list_I['hw_600'] += per_entry['hw_600']     
        avg_list_I['hw_700'] += per_entry['hw_700']
        avg_list_I['hw_800'] += per_entry['hw_800'] 
    
    if per_entry['type'] == 'P' and per_entry['show_flag']==1:
        min_list_P['count'] += 1
        if(per_entry['frm_size'] < min_list_P['frm_size']):   min_list_P['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] < min_list_P['br_30']):         min_list_P['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] < min_list_P['br_60']):         min_list_P['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] < min_list_P['rd_bd']):         min_list_P['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] < min_list_P['wr_bd']):         min_list_P['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] < min_list_P['all_bd']):       min_list_P['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] < min_list_P['hw_cycle']):   min_list_P['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] < min_list_P['sw_cycle']):   min_list_P['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] < min_list_P['vpu_cycle']): min_list_P['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] < min_list_P['t_600']):         min_list_P['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] < min_list_P['t_700']):         min_list_P['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] < min_list_P['t_800']):         min_list_P['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] < min_list_P['hw_600']):       min_list_P['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] < min_list_P['hw_700']):       min_list_P['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] < min_list_P['hw_800']):       min_list_P['hw_800'] = per_entry['hw_800']   
        
        max_list_P['count'] += 1
        if(per_entry['frm_size'] > max_list_P['frm_size']):   max_list_P['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] > max_list_P['br_30']):         max_list_P['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] > max_list_P['br_60']):         max_list_P['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] > max_list_P['rd_bd']):         max_list_P['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] > max_list_P['wr_bd']):         max_list_P['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] > max_list_P['all_bd']):       max_list_P['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] > max_list_P['hw_cycle']):   max_list_P['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] > max_list_P['sw_cycle']):   max_list_P['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] > max_list_P['vpu_cycle']): max_list_P['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] > max_list_P['t_600']):         max_list_P['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] > max_list_P['t_700']):         max_list_P['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] > max_list_P['t_800']):         max_list_P['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] > max_list_P['hw_600']):       max_list_P['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] > max_list_P['hw_700']):       max_list_P['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] > max_list_P['hw_800']):       max_list_P['hw_800'] = per_entry['hw_800'] 
        
        
        avg_list_P['count'] += 1
        avg_list_P['frm_size'] += per_entry['frm_size']
        avg_list_P['br_30'] += per_entry['br_30']
        avg_list_P['br_60'] += per_entry['br_60']       
        avg_list_P['rd_bd'] += per_entry['rd_bd']     
        avg_list_P['wr_bd'] += per_entry['wr_bd']
        avg_list_P['all_bd'] += per_entry['all_bd']
        avg_list_P['hw_cycle'] += per_entry['hw_cycle']
        avg_list_P['sw_cycle'] += per_entry['sw_cycle']
        avg_list_P['vpu_cycle'] += per_entry['vpu_cycle']   
        avg_list_P['t_600'] += per_entry['t_600']     
        avg_list_P['t_700'] += per_entry['t_700']
        avg_list_P['t_800'] += per_entry['t_800']     
        avg_list_P['hw_600'] += per_entry['hw_600']     
        avg_list_P['hw_700'] += per_entry['hw_700']
        avg_list_P['hw_800'] += per_entry['hw_800'] 
        
    if per_entry['type'] == 'B' or (per_entry['type'] == 'P' and per_entry['show_flag']==0):
        min_list_B['count'] += 1
        if(per_entry['frm_size'] < min_list_B['frm_size']):   min_list_B['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] < min_list_B['br_30']):         min_list_B['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] < min_list_B['br_60']):         min_list_B['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] < min_list_B['rd_bd']):         min_list_B['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] < min_list_B['wr_bd']):         min_list_B['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] < min_list_B['all_bd']):       min_list_B['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] < min_list_B['hw_cycle']):   min_list_B['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] < min_list_B['sw_cycle']):   min_list_B['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] < min_list_B['vpu_cycle']): min_list_B['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] < min_list_B['t_600']):         min_list_B['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] < min_list_B['t_700']):         min_list_B['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] < min_list_B['t_800']):         min_list_B['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] < min_list_B['hw_600']):       min_list_B['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] < min_list_B['hw_700']):       min_list_B['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] < min_list_B['hw_800']):       min_list_B['hw_800'] = per_entry['hw_800']   
        
        max_list_B['count'] += 1
        if(per_entry['frm_size'] > max_list_B['frm_size']):   max_list_B['frm_size'] = per_entry['frm_size']
        if(per_entry['br_30'] > max_list_B['br_30']):         max_list_B['br_30'] = per_entry['br_30']
        if(per_entry['br_60'] > max_list_B['br_60']):         max_list_B['br_60'] = per_entry['br_60']       
        if(per_entry['rd_bd'] > max_list_B['rd_bd']):         max_list_B['rd_bd'] = per_entry['rd_bd']     
        if(per_entry['wr_bd'] > max_list_B['wr_bd']):         max_list_B['wr_bd'] = per_entry['wr_bd']
        if(per_entry['all_bd'] > max_list_B['all_bd']):       max_list_B['all_bd'] = per_entry['all_bd']
            
        if(per_entry['hw_cycle'] > max_list_B['hw_cycle']):   max_list_B['hw_cycle'] = per_entry['hw_cycle']
        if(per_entry['sw_cycle'] > max_list_B['sw_cycle']):   max_list_B['sw_cycle'] = per_entry['sw_cycle']
        if(per_entry['vpu_cycle'] > max_list_B['vpu_cycle']): max_list_B['vpu_cycle'] = per_entry['vpu_cycle']   
        
        if(per_entry['t_600'] > max_list_B['t_600']):         max_list_B['t_600'] = per_entry['t_600']     
        if(per_entry['t_700'] > max_list_B['t_700']):         max_list_B['t_700'] = per_entry['t_700']
        if(per_entry['t_800'] > max_list_B['t_800']):         max_list_B['t_800'] = per_entry['t_800']     
    
        if(per_entry['hw_600'] > max_list_B['hw_600']):       max_list_B['hw_600'] = per_entry['hw_600']     
        if(per_entry['hw_700'] > max_list_B['hw_700']):       max_list_B['hw_700'] = per_entry['hw_700']
        if(per_entry['hw_800'] > max_list_B['hw_800']):       max_list_B['hw_800'] = per_entry['hw_800'] 
        
        
        avg_list_B['count'] += 1
        avg_list_B['frm_size'] += per_entry['frm_size']
        avg_list_B['br_30'] += per_entry['br_30']
        avg_list_B['br_60'] += per_entry['br_60']       
        avg_list_B['rd_bd'] += per_entry['rd_bd']     
        avg_list_B['wr_bd'] += per_entry['wr_bd']
        avg_list_B['all_bd'] += per_entry['all_bd']
        avg_list_B['hw_cycle'] += per_entry['hw_cycle']
        avg_list_B['sw_cycle'] += per_entry['sw_cycle']
        avg_list_B['vpu_cycle'] += per_entry['vpu_cycle']   
        avg_list_B['t_600'] += per_entry['t_600']     
        avg_list_B['t_700'] += per_entry['t_700']
        avg_list_B['t_800'] += per_entry['t_800']     
        avg_list_B['hw_600'] += per_entry['hw_600']     
        avg_list_B['hw_700'] += per_entry['hw_700']
        avg_list_B['hw_800'] += per_entry['hw_800']         
        
    '''
    average 5
    '''
if avg_list_all['count'] > 0:
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

if avg_list_I['count'] > 0:
    avg_list_I['frm_size']    /= avg_list_I['count']
    avg_list_I['br_30']       /= avg_list_I['count']
    avg_list_I['br_60']       /= avg_list_I['count']
    avg_list_I['rd_bd']       /= avg_list_I['count']
    avg_list_I['wr_bd']       /= avg_list_I['count']
    avg_list_I['all_bd']      /= avg_list_I['count']
    avg_list_I['hw_cycle']    /= avg_list_I['count']
    avg_list_I['sw_cycle']    /= avg_list_I['count']
    avg_list_I['vpu_cycle']   /= avg_list_I['count']
    avg_list_I['t_600']       /= avg_list_I['count']
    avg_list_I['t_700']       /= avg_list_I['count']
    avg_list_I['t_800']       /= avg_list_I['count']
    avg_list_I['hw_600']      /= avg_list_I['count'] 
    avg_list_I['hw_700']      /= avg_list_I['count']
    avg_list_I['hw_800']      /= avg_list_I['count']

if avg_list_P['count'] > 0:
    avg_list_P['frm_size']    /= avg_list_P['count']
    avg_list_P['br_30']       /= avg_list_P['count']
    avg_list_P['br_60']       /= avg_list_P['count']
    avg_list_P['rd_bd']       /= avg_list_P['count']
    avg_list_P['wr_bd']       /= avg_list_P['count']
    avg_list_P['all_bd']      /= avg_list_P['count']
    avg_list_P['hw_cycle']    /= avg_list_P['count']
    avg_list_P['sw_cycle']    /= avg_list_P['count']
    avg_list_P['vpu_cycle']   /= avg_list_P['count']
    avg_list_P['t_600']       /= avg_list_P['count']
    avg_list_P['t_700']       /= avg_list_P['count']
    avg_list_P['t_800']       /= avg_list_P['count']
    avg_list_P['hw_600']      /= avg_list_P['count'] 
    avg_list_P['hw_700']      /= avg_list_P['count']
    avg_list_P['hw_800']      /= avg_list_P['count']

if avg_list_B['count'] > 0:
    avg_list_B['frm_size']    /= avg_list_B['count']
    avg_list_B['br_30']       /= avg_list_B['count']
    avg_list_B['br_60']       /= avg_list_B['count']
    avg_list_B['rd_bd']       /= avg_list_B['count']
    avg_list_B['wr_bd']       /= avg_list_B['count']
    avg_list_B['all_bd']      /= avg_list_B['count']
    avg_list_B['hw_cycle']    /= avg_list_B['count']
    avg_list_B['sw_cycle']    /= avg_list_B['count']
    avg_list_B['vpu_cycle']   /= avg_list_B['count']
    avg_list_B['t_600']       /= avg_list_B['count']
    avg_list_B['t_700']       /= avg_list_B['count']
    avg_list_B['t_800']       /= avg_list_B['count']
    avg_list_B['hw_600']      /= avg_list_B['count'] 
    avg_list_B['hw_700']      /= avg_list_B['count']
    avg_list_B['hw_800']      /= avg_list_B['count'] 

if avg_list_avgx['count'] > 0:
    avg_list_avgx['frm_size']    /= avg_list_avgx['count']
    avg_list_avgx['br_30']       /= avg_list_avgx['count']
    avg_list_avgx['br_60']       /= avg_list_avgx['count']
    avg_list_avgx['rd_bd']       /= avg_list_avgx['count']
    avg_list_avgx['wr_bd']       /= avg_list_avgx['count']
    avg_list_avgx['all_bd']      /= avg_list_avgx['count']
    avg_list_avgx['hw_cycle']    /= avg_list_avgx['count']
    avg_list_avgx['sw_cycle']    /= avg_list_avgx['count']
    avg_list_avgx['vpu_cycle']   /= avg_list_avgx['count']
    avg_list_avgx['t_600']       /= avg_list_avgx['count']
    avg_list_avgx['t_700']       /= avg_list_avgx['count']
    avg_list_avgx['t_800']       /= avg_list_avgx['count']
    avg_list_avgx['hw_600']      /= avg_list_avgx['count'] 
    avg_list_avgx['hw_700']      /= avg_list_avgx['count']
    avg_list_avgx['hw_800']      /= avg_list_avgx['count'] 
    
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
row +=2

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
row +=2
workbook.close()
    














