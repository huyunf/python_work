import re
import ast
import os
import sys
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from collections import namedtuple

RET_OK      = 0
RET_FAIL    =-1

def command_line(argv):
    if len(argv) != 3:
        print "performance_log_parser.py log_file mode(0:host, 1:m3, 2:amp)"
        return RET_FAIL
    else:
        return RET_OK

class original_log:
    
    F = 0               # original file descriptor
    m = 0               # mode: 0:host, 1:m3, 2:amp
    sstring = ''
    original_list = list()
    
    def __init__(self, name, mode):
        self.F = open(name, 'r')
        if self.F == 0:
            print "[Error]: Could not open log file: %s\n" % name
        else:
            print "Open input log file: %s" % name
        self.m = int(mode)
        
        if self.m == 0 or self.m  == 1:
            self.sstring = 'pic_num'
        elif self.m == 2:    
            self.sstring = 'Ins_num'
            
    def __del__(self):
        if self.F != 0:
            self.F.close()
            
    def set_log(self, name):
        if self.F != 0:
            close(self.F)
        self.F = open(name, 'r')
        if self.F==0:
            print "[Error]: Could not open log file: %s\n" % name
        else:
            print "Open input log file: %s" % name
            
    @staticmethod
    def entry_filter_item(d, index):
        # transfer key
        trans_d = {
             'hw_cycle':'hw', 
             'fw_cycle':'sw',
             'sw_cycle':'sw',
             'module<end_of_pic>':'eop',
             'module<so_pic_cfg>':'sop',
             'rd_bd':'r_bw',
             'wr_bd':'w_bw',
            }
        for _k,_v in d.items():
            if trans_d.has_key(_k):
                d.pop(_k, None)
                d[trans_d[_k]] = _v
                
        # add must-have key
        if not d.has_key('show'):
            d['show'] = '1'
        if not d.has_key('pic_num'):
            d['pic_num'] = str(index)
            
    @staticmethod
    def hex2oct_filter_key(k):
        l = ['type']
        if k in l:
            return True
        else:
            return False
        
    def add_entry_2_orig_list(self, entry, index):
        d = dict(zip(*[iter(entry)]*2))                                 # generate dict for each item   
        self.entry_filter_item(d, index)                                # filter item for table title
        for k,v in d.iteritems():
            if self.hex2oct_filter_key(k) == False:                     # trans str for 'number' value
                d[k] = int(ast.literal_eval(v))   
        self.original_list.append(d)
            
    def get_orig_data(self):
        index = 0
        new_entry = list()
        for test_line in self.F:
            l = re.split(r'[:,\s]\s*', test_line)
            if '@perf>>' in l:
                # get value from log
                p = [i for i in l if (i!='' and l.index(i)>l.index('@perf>>'))]   
                # encounter the start of next entry, put current into original list
                if len(new_entry)>0 and p[0]==self.sstring:                 
                    self.add_entry_2_orig_list(new_entry, index)
                    index = index + 1                                   # update index
                    new_entry[:] = []                                   # empty new_entry for next
                new_entry = new_entry + p
        # deal with the last one
        self.add_entry_2_orig_list(new_entry, index)
        index = index + 1
        
        #print self.original_list
        print 'total entry: %d' % index        

class xls_wrokbook:
    
    workbook            = 0
    
    wb_fmt              = dict()
    
    sheet_entry         = namedtuple('sheet_entry',         'fmtIdx    col         formula     dst_b     pa_size     b0     b1     b2     b3     b4     const')
    sheet_statistic_row = namedtuple('sheet_statistic_row', 'row       label       formula     row_beg   row_end')
    sheet_name          = namedtuple('sheet_name',          'fmtIdx    name      label_c     label       cell      formula   cell_v')
    
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    def open(self):
        self.workbook   = xlsxwriter.Workbook('performance_'+'.xlsx')
        
        self.wb_fmt['f1'] = self.workbook.add_format()
        self.wb_fmt['f1'].set_num_format('0.0')
        self.wb_fmt['f2'] = self.workbook.add_format()
        self.wb_fmt['f2'].set_num_format('0.00')
        self.wb_fmt['f3'] = self.workbook.add_format()
        self.wb_fmt['f3'].set_num_format('0.000')
        self.wb_fmt['F2'] = self.workbook.add_format({'color':'blue', 'underline':1})
        self.wb_fmt['F2'].set_num_format('0.00')
        self.wb_fmt['d'] = self.workbook.add_format()
        self.wb_fmt['d'].set_num_format('0')
        self.wb_fmt['D'] = self.workbook.add_format({'color':'blue', 'underline':1})
        self.wb_fmt['D'].set_num_format('0')
        self.wb_fmt['L'] = self.workbook.add_format({'bold':1, 'bg_color':'#8FCDCC'})
        self.wb_fmt['Ls'] = self.workbook.add_format({'bold':1, 'color':'red'})
        self.wb_fmt['l'] = self.workbook.add_format({'bold':1})
        self.wb_fmt['b'] = self.workbook.add_format({'bg_color':'#FE9F9F'})
    
    def close(self):
        self.workbook.close()
        
    def write_sheet_with_data(self, sheet, entry_list, data_list):
        for entry in entry_list:
            col = entry_list.index(entry)  
            sheet.write(0, col, entry)
        sheet.freeze_panes(1, 2)            # freeze the first line
        row=1
        for per_entry in data_list:
            for _key,_value in per_entry.items():
                if _key in entry_list:
                    col = entry_list.index(_key)
                    if type(_value)==int:
                        sheet.write_number(row, col, int(_value), self.wb_fmt['d'])
                    else:
                        sheet.write(row, col, _value)
            row+=1 #enter the next row   
    
    def write_sheet_with_entry(self, sheet, entry, num):
        for idx in range(num):
            di = entry.dst_b + idx
            b0 = entry.b0 + idx
            b1 = entry.b1 + idx
            b2 = entry.b2 + idx
            b3 = entry.b3 + idx
            b4 = entry.b4 + idx
            if int(entry.pa_size)==0:
                if entry.formula=='':
                    sheet.write_blank(entry.col % (di), None, self.wb_fmt[entry.fmtIdx])
                else:
                    sheet.write_formula(entry.col % (di), entry.formula % (entry.const), self.wb_fmt[entry.fmtIdx])
            if int(entry.pa_size)==1:
                sheet.write_formula(entry.col % (di), entry.formula % (b0), self.wb_fmt[entry.fmtIdx])
            if int(entry.pa_size)==2:
                sheet.write_formula(entry.col % (di), entry.formula % (b0, b1), self.wb_fmt[entry.fmtIdx])
            if int(entry.pa_size)==3:
                sheet.write_formula(entry.col % (di), entry.formula % (b0, b1, b2), self.wb_fmt[entry.fmtIdx])
            if int(entry.pa_size)==4:
                sheet.write_formula(entry.col % (di), entry.formula % (b0, b1, b2, b3), self.wb_fmt[entry.fmtIdx]) 
            if int(entry.pa_size)==5:
                sheet.write_formula(entry.col % (di), entry.formula % (b0, b1, b2, b3, b4), self.wb_fmt[entry.fmtIdx])
                
    def write_sheet_with_name(self, sheet, entry):
        # label
        sheet.write_string(entry.label_c, entry.label)
        # value
        sheet.write(entry.cell, entry.formula, self.wb_fmt[entry.fmtIdx])
        self.workbook.define_name(entry.name, entry.cell_v)
                
    def write_raw(self, orig_log):
        worksheet = self.workbook.add_worksheet('raw')
        entry_list = ['pic_num', 'type', 'width', 'height', 'mbs', 'show', 'ints', 'slcs', 'bits', 'r_bw', 'w_bw', 'hw', 'sw', 'total', 'sop', 'eop', 'int_lat', 'm3', 
                      'scu', 'spu', 'mvu', 'qtu', 'vcu', 'ppu', 'fcu', 'pfu', 'spu1', 'spu2', 'spu3', 'qtu1', 'vcu1', 'vcu2', 'ppu1', 'fcu1', 'pfu1', ' ',
                      'mb_bits', 'mb_rbw', 'mb_wbw', 'mb_hw', 'mb_sw', 'mb_total', 'mb_intlat', 'mb_m3', ' ',
                      'br', 'gr_bw', 'gw_bw']
        
        self.write_sheet_with_data(worksheet, entry_list, orig_log.original_list)
        
        row_num     = len(orig_log.original_list)
        col_num     = len(entry_list)
        
        # AK ... AR, AT, AU, AV
        sheet_entries = [
            #                fmtIdx    col        formula                                           d        psz     b0      b1     b2       b3      b4       const
            self.sheet_entry('b',     'AJ%d',     '',                                              2,       0,      0,      0,      0,      0,      0,        0),
            self.sheet_entry('f3',    'AK%d',     '=I%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AL%d',     '=J%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AM%d',     '=K%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AN%d',     '=L%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AO%d',     '=M%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AP%d',     '=N%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AQ%d',     '=Q%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AR%d',     '=R%d/$E%d',                                     2,       2,      2,      2,      0,      0,      0,        0),

            self.sheet_entry('f2',    'AT%d',     '=I%d*60/1000000',                               2,       1,      2,      0,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AU%d',     '=J%d*128*60/1000000000',                        2,       1,      2,      0,      0,      0,      0,        0),
            self.sheet_entry('f2',    'AV%d',     '=K%d*128*60/1000000000',                        2,       1,      2,      0,      0,      0,      0,        0),
        ]
        
        for entry in sheet_entries:
            self.write_sheet_with_entry(worksheet, entry, row_num)
        
    def write_perf_data(self, orig_log):
        worksheet = self.workbook.add_worksheet('perf_data')
        entry_list = ['','','pic_num', 'type', 'disp', 'disc', 't_hw', 't_fw', 't_sw', 't_hw_f', 't_fw_f', 't_sw_f', 't+h', 't+hf', 't+hfs', 'r', 'w', 'r+w', 'r_h', 'w_h', 'r+w_h']
        self.write_sheet_with_data(worksheet, entry_list, [])
        
        row_num     = len(orig_log.original_list)
        col_num     = len(entry_list)

        '''
        write special row
        '''
        sheet_rows = [
            self.sheet_statistic_row(2,     'min',      'MIN',      9,      9+row_num-1),
            self.sheet_statistic_row(3,     'avg',      'AVERAGE',  9,      9+row_num-1),
            self.sheet_statistic_row(4,     'max',      'MAX',      9,      9+row_num-1),
            self.sheet_statistic_row(5,     'min',      '',         9,      9+row_num-1),
            self.sheet_statistic_row(6,     'avg',      '',         9,      9+row_num-1),
            self.sheet_statistic_row(7,     'max',      '',         9,      9+row_num-1),
        ]
        
        for entry in sheet_rows:
            worksheet.write_string(entry.row, 0, entry.label)
            for col in range(col_num):
                if col > 1:
                    cur = xl_rowcol_to_cell(entry.row, col)
                    beg = xl_rowcol_to_cell(entry.row_beg, col)
                    end = xl_rowcol_to_cell(entry.row_end, col)
                    formula = entry.formula
                    if formula !='':
                        formula = formula+'('+beg+':'+end+')'
                    worksheet.write_formula(cur, formula, self.wb_fmt['f2'])

        '''
        write entry
        '''
        sheet_entries = [
			#				fmtIdx	col		formula												d		psz 	b0  	b1		b2		b3		b4		const
            self.sheet_entry('d',	'A%d',     '%d',                               				10, 	1,  	0,  	0,  	0,  	0,  	0,		0),
            self.sheet_entry('d',	'B%d',     '=IF(MOD(A%d,1)=0,1,0)',            				10, 	1,  	10, 	0,  	0,  	0,  	0,		0),
            self.sheet_entry('d',	'C%d',     '=IF($B%d=0,"",raw!A%d)',           				10, 	2,  	10,  	2,  	0,  	0,  	0,		0),
            self.sheet_entry('d',	'D%d',     '=IF($B%d=1,raw!B%d,"")',           				10, 	2,  	10,  	2,  	0,  	0,  	0,		0),
            self.sheet_entry('d',	'E%d',     '=raw!F%d',                         				10, 	1,  	2,  	0,  	0,  	0,  	0,		0),
            self.sheet_entry('d',	'F%d',     '1-E%d',                            				10, 	1,  	10, 	0,  	0,  	0,  	0,		0),
            self.sheet_entry('f2',	'G%d',     '=IF($B%d=0,"",raw!L%d/600/1000)',  				10, 	2,  	10,  	2,  	0,  	0,  	0,		0),
            self.sheet_entry('f2',	'H%d',     '=IF($B%d=0,"",raw!M%d/600/1000)',  				10, 	2,  	10,  	2,  	0,  	0,  	0,		0),
            self.sheet_entry('f2',	'I%d',     '=IF($B%d=0,"",raw!N%d/600/1000)-G%d-H%d',		10,     4,      10,     2,     10,     10,      0,		0),
            self.sheet_entry('f2',	'J%d',     '=IF($B%d=0,"",IF(G%d>J$8,J$7,G%d))',			10,     3,      10,    10,     10,      0,      0,		0),
            self.sheet_entry('f2',	'K%d',     '=IF($B%d=0,"",IF(H%d>K$8,K$7,H%d))',			10,     3,      10,    10,     10,      0,      0,		0),
            self.sheet_entry('f2',	'L%d',     '=IF($B%d=0,"",IF(I%d>L$8,L$7,I%d))', 			10,     3,      10,    10,     10,      0,      0,		0),
            self.sheet_entry('f2',	'M%d',     '=IF($B%d=0,"",J%d)',                 			10,     2,      10,    10,      0,      0,      0,		0),
            self.sheet_entry('f2',	'N%d',     '=IF($B%d=0,"",J%d+K%d)',             			10,     3,      10,    10,     10,      0,      0,		0),
            self.sheet_entry('f2',	'O%d',     '=IF($B%d=0,"",J%d+K%d+L%d)',         			10,     4,      10,    10,     10,     10,      0,		0),
            self.sheet_entry('d',	'P%d',     '=IF($B%d=0,"",raw!J%d)',             			10,     2,      10,     2,      0,      0,      0,		0),
            self.sheet_entry('d',	'Q%d',     '=IF($B%d=0,"",raw!K%d)',             			10,     2,      10,     2,      0,      0,      0,		0),
            self.sheet_entry('d',	'R%d',     '=IF($B%d=0,"",P%d+Q%d)',             			10,     3,      10,    10,     10,      0,      0,		0),
            self.sheet_entry('f2',  'S%d',     '=IF($B%d=0,"",P%d*128/M%d/1000000)',            10,     3,      10,    10,     10,      0,      0,      0),
            self.sheet_entry('f2',  'T%d',     '=IF($B%d=0,"",Q%d*128/M%d/1000000)',            10,     3,      10,    10,     10,      0,      0,      0),
            self.sheet_entry('f2',  'U%d',     '=IF($B%d=0,"",R%d*128/M%d/1000000)',            10,     3,      10,    10,     10,      0,      0,      0),
        ]
        
        for entry in sheet_entries:
            self.write_sheet_with_entry(worksheet, entry, row_num)
        
        sheet_statistic_entries = [
            self.sheet_entry('d',   'G%d',     '=1000/G%d',                                     6,      1,       3,     0,      0,      0,      0,		0),
            self.sheet_entry('d',   'M%d',     '=1000/M%d',                                     6,      1,       3,     0,      0,      0,      0,		0),
            self.sheet_entry('d',   'N%d',     '=1000/N%d',                                     6,      1,       3,     0,      0,      0,      0,		0),
            self.sheet_entry('d',   'O%d',     '=1000/O%d',                                     6,      1,       3,     0,      0,      0,      0,		0),
        ]

        for entry in sheet_statistic_entries:
            self.write_sheet_with_entry(worksheet, entry, 3)

        '''
        write special value
        '''
        worksheet.write_number('J7', 40,    self.wb_fmt['F2'])
        worksheet.write_number('J8', 100,   self.wb_fmt['F2'])
        worksheet.write_number('K7', 5,     self.wb_fmt['F2'])
        worksheet.write_number('K8', 10,    self.wb_fmt['F2'])
        worksheet.write_number('L7', 200,   self.wb_fmt['F2'])
        worksheet.write_number('L8', 1000,  self.wb_fmt['F2'])
		
    def write_simdat(self, orig_log):
        worksheet = self.workbook.add_worksheet('simdat')
        entry_list = ['#', 'pic_type', 'time(ms)', 'display(a)', 'discard(a)', '', 'win_avg', 'violation', 'fps']
        self.write_sheet_with_data(worksheet, entry_list, [])
        
        row_num     = len(orig_log.original_list)
        col_num     = len(entry_list)
        
        '''
        define name
        '''
        worksheet.merge_range('L10:M10',    'Raw data properties(Global):',     self.wb_fmt['L'])
        worksheet.merge_range('L17:M17',    'UserParameters(Local):',           self.wb_fmt['L'])
        worksheet.merge_range('L22:M22',    'Derived parameters(Local):',       self.wb_fmt['L'])
        worksheet.merge_range('L26:M26',    'Sim result:',                      self.wb_fmt['L'])
        
        sheet_names = [
            self.sheet_name('d',	'mbs',      		    'L11',      'mbs',      			'M11',      '=32640',                           					'=simdat!$M$11'),
            self.sheet_name('d',	'fcnt',     		    'L12',      'fcnt',     			'M12',      '=COUNT(C:C)',                      					'=simdat!$M$12'),
            self.sheet_name('d',	'bot_idx',  		    'L14',      'bot_idx',  			'M14',      '=MATCH(MAX(C:C)+1,C:C,1)',         					'=simdat!$M$14'),
            self.sheet_name('d',	'top_idx',  		    'L13',      'top_idx',  			'M13',      '=bot_idx-fcnt+1',                  					'=simdat!$M$13'),
            self.sheet_name('d',	'simdat!idly',  		'L15',      'idly',     			'M15',      '=MATCH(TRUE,D:D-1>=0,0)-top_idx',  					'=simdat!$M$15'),
														
            self.sheet_name('f1',	'simdat!freq',     		'L18',      'freq',     			'M18',      '=600',                             					'=simdat!$M$18'),
            self.sheet_name('f1',	'simdat!fps',      		'L19',      'fps',      			'M19',      '=60',                              					'=simdat!$M$19'),
            self.sheet_name('f1',	'simdat!avg_win',  		'L20',      'avg_win',  			'M20',      '=8',                               					'=simdat!$M$20'),
														
            self.sheet_name('f1',	'simdat!dt',       		'L23',      'dt(ms)',   			'M23',      '=1000/fps',                        					'=simdat!$M$23'),
				
            self.sheet_name('f1',	'simdat!max_wavg_t',	'L27',      'max_win_avg(ms)',   	'M27',      '=MAX(OFFSET(G$1,top_idx+avg_win-1,0,fcnt-avg_win-1))',	'=simdat!$M$27'),
			self.sheet_name('f1',	'simdat!max_wavg_h',	'L28',      'max_win_avg(MHz)',   	'M28',      '=M27*fps*freq/1000',									'=simdat!$M$28'),
			self.sheet_name('f1',	'simdat!min_wavg_f',	'L29',      'min_win_avg(fps)',   	'M29',      '=1000/M27',											'=simdat!$M$29'),
            self.sheet_name('f1',	'simdat!violations',	'L30',      'violations',   		'M30',      '=COUNTIF(H:H,">0")',									'=simdat!$M$30'),
				
			self.sheet_name('f1',	'simdat!avg_ms',		'L32',      'average(msg)',   		'M32',      '=AVERAGE(C:C)',										'=simdat!$M$32'),
			self.sheet_name('f1',	'simdat!avg_fps',		'L33',      'average fps',   		'M33',      '=1000/M32',											'=simdat!$M$33'),
        ]
        
        for entry in sheet_names:
            self.write_sheet_with_name(worksheet, entry)
            
        '''
        write entry
        '''
        sheet_entries = [
            #                fmtIdx    col        formula                                        d      psz     b0      b1      b2      b3      b4       const
            self.sheet_entry('d',    'A%d',     '%d',                                           10,     1,      0,      0,      0,      0,      0,        0),
            self.sheet_entry('d',    'B%d',     '=perf_data!D%d',                               10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('f1',   'C%d',     '=perf_data!N%d',                               10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('d',    'D%d',     '=perf_data!E%d',                               10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('d',    'E%d',     '=perf_data!F%d',                               10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('f1',   'G%d',     '=AVERAGE(OFFSET(C%d,1-avg_win,0,avg_win,1))',  10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('f1',   'H%d',     '=MAX(0,G%d-dt)',                               10,     1,      10,     0,      0,      0,      0,        0),
            self.sheet_entry('f1',   'I%d',     '=1000/G%d',                                    10,     1,      10,     0,      0,      0,      0,        0),
        ]
        
        for entry in sheet_entries:
            self.write_sheet_with_entry(worksheet, entry, row_num)
            

    def write_sim0(self, orig_log):
        worksheet = self.workbook.add_worksheet('sim0')
        entry_list = ['#', 't', 'n', 'Q\'', 'x', 'Q\'\'', 'Q\'\'\'', 's', 'Q', 'r\'', 'r', 'w']
        self.write_sheet_with_data(worksheet, entry_list, [])
        
        row_num     = len(orig_log.original_list)
        col_num     = len(entry_list)
        
        '''
        define name
        '''
        worksheet.merge_range('N10:O10',    'UserParameters(Local):',           self.wb_fmt['L'])
        worksheet.merge_range('N14:O14',    'Derived parameters(Local):',       self.wb_fmt['L'])
        worksheet.merge_range('N18:O18',    'Sim result:',                      self.wb_fmt['L'])
        worksheet.merge_range('N31:O31',    'Sim model 0',                      self.wb_fmt['L'])
        
        worksheet.write_string('N33',       't(i)=r(i-1)+d(i)')
        worksheet.write_string('N34',       'n(i)=t(i)/dt')
        worksheet.write_string('N35',       'Q\'(i)=Q(i-1)-n(i)')
        worksheet.write_string('N36',       'x(i)=-min(0,Q\'(i))')
        worksheet.write_string('N37',       'Q\'\'(i)=Q\'(i)+x(i)')
        worksheet.write_string('N38',       'Q\'\'\'(i)=Q\'\'(i)+a(i)')
        worksheet.write_string('N39',       's(i)=max(0,Q\'\'\'(i)-bufs)')
        worksheet.write_string('N40',       'Q(i)=Q\'(i)-s(i)')
        worksheet.write_string('N41',       'r\'(i)=t(i)-n(i)*dt')
        worksheet.write_string('N42',       'r(i)=s(i)?0:t(i)-n(i)*dt')
        worksheet.write_string('N43',       'w(i)=max(0,s(i)*dt-r\'(i))')
		
        sheet_names = [
            self.sheet_name('f1',    'sim0!fps',              'N11',      'fps',                  'O11',      '=80',                                               '=sim0!$O$11'),
            self.sheet_name('d',     'sim0!bufs',             'N12',      'bufs',                 'O12',      '=10',                                               '=sim0!$O$12'),
            
            self.sheet_name('f2',    'sim0!dt',               'N15',      'dt',                   'O15',      '=1000/fps',                                         '=sim0!$O$15'),
            self.sheet_name('d',     'sim0!qdly',             'N16',      'qdly',                 'O16',      '=bufs',                                             '=sim0!$O$16'),
            
            self.sheet_name('d',     'sim0!min_bufs',         'N19',      'min_bufs',             'O19',      '=MAX(I10:I44)-MIN(I10:I44)+1',                      '=sim0!$O$19'),
            self.sheet_name('d',     'sim0!q_inc',            'N20',      'q_inc',                'O20',      '=OFFSET(I1,bot_idx-1,0)-OFFSET(I1,top_idx-2,0)',    '=sim0!$O$20'),
            self.sheet_name('f2',    'sim0!sum_d',            'N21',      'sum_d',                'O21',      '=SUM(simdat!C:C)',                                  '=sim0!$O$21'),
            
            self.sheet_name('f2',    'sim0!sum_b',            'N22',      'sum_b',                'O22',      '=SUM(simdat!E:E)',                                  '=sim0!$O$22'),
            self.sheet_name('f2',    'sim0!sum_n',            'N23',      'sum_n',                'O23',      '=SUM(C:C)',                                         '=sim0!$O$23'),
            self.sheet_name('f2',    'sim0!sum_s',            'N24',      'sum_s',                'O24',      '=SUM(H:H)',                                         '=sim0!$O$24'),
            self.sheet_name('f2',    'sim0!sum_w',            'N25',      'sum_w',                'O25',      '=SUM(L:L)',                                         '=sim0!$O$25'),
            self.sheet_name('f2',    'sim0!sum_x',            'N26',      'sum_x',                'O26',      '=SUM(E:E)',                                         '=sim0!$O$26'),
            self.sheet_name('d',     'sim0!check_fcnt',       'N27',      'check_fcnt',           'O27',      '=sum_n+sum_s-sum_x+q_inc+sum_b',                    '=sim0!$O$27'),
            
            self.sheet_name('Ls',    'sim0!conclusion',       'N29',      'conclusion',           'O29',      '=fps&"/"&bufs&": "&IF(P29=0,"PASS","FAIL")',        '=sim0!$O$29'),
        ]
        
        for entry in sheet_names:
            self.write_sheet_with_name(worksheet, entry)     
               
        '''
        write special value
        '''
        worksheet.write('K9',   0,                      self.wb_fmt['F2'])
        worksheet.write('I9',   '=qdly',                self.wb_fmt['D'])
        worksheet.write('P26',  '=IF(sum_x=0,0,-1)')
        worksheet.write('P26',  '=IF(sum_x=0,0,-1)')
        worksheet.write('P27',  '=IF(O27=fcnt,0,-1)')
        worksheet.write('P29',  '=IF(SUM(P26:P27)=0,0,-1)')
        
        '''
        write entry
        '''
        sheet_entries = [
            #                fmtIdx    col        formula                                        d      psz     b0      b1      b2      b3      b4       const
            self.sheet_entry('d',    'A%d',     '%d',                                           10,     1,      0,      0,      0,      0,      0,        0),
            self.sheet_entry('f1',   'B%d',     '=K%d+simdat!C%d',                              10,     2,      9,     10,      0,      0,      0,        0),
            self.sheet_entry('d',    'C%d',     '=INT(B%d/dt)',                                 10,     1,     10,      0,      0,      0,      0,        0),
            self.sheet_entry('d',    'D%d',     '=I%d-C%d',                                     10,     2,      9,     10,      0,      0,      0,        0),
            self.sheet_entry('d',    'E%d',     '=-MIN(0,D%d)',                                 10,     1,     10,      0,      0,      0,      0,        0),
            self.sheet_entry('d',    'F%d',     '=D%d+E%d',                                     10,     2,     10,     10,      0,      0,      0,        0),
            self.sheet_entry('d',    'G%d',     '=F%d+simdat!D%d',                              10,     2,     10,     10,      0,      0,      0,        0),
            self.sheet_entry('d',    'H%d',     '=MAX(0,G%d-bufs)',                             10,     1,     10,      0,      0,      0,      0,        0),
            self.sheet_entry('d',    'I%d',     '=G%d-H%d',                                     10,     2,     10,     10,      0,      0,      0,        0),
            self.sheet_entry('f1',   'J%d',     '=B%d-C%d*dt',                                  10,     2,     10,     10,      0,      0,      0,        0),
            self.sheet_entry('f1',   'K%d',     '=IF(H%d>0,0,J%d)',                             10,     2,     10,     10,      0,      0,      0,        0),
            self.sheet_entry('f1',   'L%d',     '=MAX(0,H%d*dt-J%d)',                           10,     2,     10,     10,      0,      0,      0,        0),
        ]
        
        for entry in sheet_entries:
            self.write_sheet_with_entry(worksheet, entry, row_num)
        
if __name__=="__main__":
    
    if command_line(sys.argv) < 0:
        exit(0)
    
    orig_log = original_log(sys.argv[1], sys.argv[2])
    orig_log.get_orig_data()
    
    #for i in orig_l.original_list:
    #    print i

    xls_book = xls_wrokbook()
    xls_book.open()
    xls_book.write_raw(orig_log)
    xls_book.write_perf_data(orig_log)
    xls_book.write_simdat(orig_log)
    xls_book.write_sim0(orig_log)
    xls_book.close()
    
    