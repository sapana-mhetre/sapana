import os, time
from stat import *
import sys
import   xlrd
from datetime import date, datetime, timedelta
from xlrd import open_workbook, xldate_as_tuple, \
    XL_CELL_NUMBER, XL_CELL_DATE, XL_CELL_TEXT, cellname
from xlwt import easyxf, XFStyle, Workbook
from xlutils.copy import copy

"""
This test library provides some keywords to allow
opening, reading, writing, and saving Excel files
from Robot Framework
"""

class ExcelLibrary:

    VERSION = '0.0.1'

    def __init__(self, slash='/'):
        self.wb = None
        self.tb = None
        self.file_path = None
        self.file_path_counter = 0
        self.counter = 0
        self.slash = slash
        self.tmpDir = os.path.abspath(os.path.join( __file__, os.path.pardir))

    def open_excel(self, fname):
        """Open the Excel file indicated by fname"""
        # self.file_path_counter = self.file_path_counter+1
        # if self.file_path_counter == 1:
            # self.file_path = fname
        self.file_path = fname
        print 'Opening file at %s' % fname
        self.wb = open_workbook(os.path.join(self.slash, self.tmpDir, fname), formatting_info=False)#, on_demand=True)


    def read_cell(self, row, column, sheetname):
        """Return the value stored in the cell indicated by
        row and column.
        """
        sheet = self.wb.sheet_by_name(sheetname)
        cv = sheet.cell(int(row), int(column)).value
        print 'Cell %s!' % cv
        return cv

    def Get_Number_Of_Rows(file, name):
        wb = open_workbook(file)
        # sheet = wb.sheet_by_index(0)
        count = wb.sheet_by_name(name).nrows
        return count


    def put_number_to_cell(self, row, column, value, sheetname):
        """Sets the value of the indicated cell to be
        the number given in the parameter.
        """
        if self.wb:
            cell = self.wb.sheet_by_name(sheetname).cell(int(row), int(column))
            if cell.ctype == XL_CELL_NUMBER:
                self.wb.sheets()
                if not self.tb:
                    self.tb = copy(self.wb)
        if self.tb:
            plain = easyxf('')
            self.tb.sheet_by_name(sheetname).write(int(row),
                                       int(column),
                                       float(value),
                                       plain)


    def put_string_to_cell(self, row, column, value, sheetname):
        """Sets the value of the indicated cell to be
        the string given in the parameter.
        """
        # self.counter = self.counter+1
        # if self.counter == 1:
            # self.tb = copy(self.wb)
        print self.file_path
        # buffer_size = 8
        # locked = None
        # # file_object = open(os.path.join('/home/jenkins/workspace/DT2.0', self.file_path), 'a', buffer_size)
        # for x in range(0, 120):
            # file_object = open(os.path.join('/home/jenkins/workspace/DT2.0', self.file_path), 'a', buffer_size)
            # if file_object:
				# print file_object
				# locked = False
				# break
            # else:
				# locked = True
				# time.sleep(1)
        # wb = open_workbook(os.path.join('C:\\Users\\e001857\\Desktop\\DTNTS22', self.file_path), formatting_info=True)
        # for x in range(0, 120):
            # st = os.stat(os.path.join('/home/jenkins/workspace/DT2.0', self.file_path))
            # print st[ST_MODE]
            # if st[ST_MODE]!=33277:
                # time.sleep(1)
            # else:
                # break
        # print st[ST_MODE]
        wb = open_workbook(os.path.join('/home/jenkins/workspace/DT2.0', self.file_path), formatting_info=True)
        self.tb = copy(wb)
        plain = easyxf('')
        for index, sheet in enumerate(self.wb.sheet_names()):
            if sheet.upper() == sheetname.upper():
                print index
                sheet = self.tb.get_sheet(index)
                sheet.write(int(row), int(column), value, plain)
        # sheet = self.tb.get_sheet(self.wb.sheet_by_name(sheetname))
        # if self.wb:
            # cell = self.wb.get_sheet(0).cell(int(row), int(column))
            # if cell.ctype == XL_CELL_TEXT:
                # self.wb.sheets()
                # if not self.tb:
                    # self.tb = copy(self.wb)
        # if self.tb:
            # plain = easyxf('')
            # self.tb.get_sheet(0).write(int(row),
                                       # int(column),
                                       # value,
                                       # plain)
        # self.tb.save(os.path.join('C:\\Users\\e001857\\Desktop\\DTNTS22', self.file_path))
        self.tb.save(os.path.join('/home/jenkins/workspace/DT2.0', self.file_path))
        wb = None
        self.open_excel(self.file_path)
		
    def put_date_to_cell(self, row, column, value, dateFrm='d.M.yyyy'):
        """Sets the value of the indicated cell to be
        the date given in the parameter. The format of the resulting
        date may be given, too.
        """
        if self.wb:
            cell = self.wb.get_sheet(0).cell(int(row), int(column))
            if cell.ctype == XL_CELL_DATE:
                self.wb.sheets()
                if not self.tb:
                    self.tb = copy(self.wb)
        if self.tb:
            print(value)
            dt = value.split('.')
            dti = [int(dt[2]), int(dt[1]), int(dt[0])]
            print(dt, dti)
            ymd = datetime(*dti)
            plain = easyxf('', num_format_str=dateFrm)
            self.tb.get_sheet(0).write(int(row),
                                       int(column),
                                       ymd,
                                       plain)

    def modify_cell_with(self, row, column, op, val):
        """Modifies a number cell
        with the given operation and value.
        """
        cell = self.wb.get_sheet(0).cell(int(row), int(column))
        curval = cell.value
        if cell.ctype == XL_CELL_NUMBER:
            self.wb.sheets()
            if not self.tb:
                self.tb = copy(self.wb)
            plain = easyxf('')
            modexpr = str(curval)+op+val
            self.tb.get_sheet(0).write(int(row),
                                       int(column),
                                       eval(modexpr),
                                       plain)

    def add_to_date(self, row, column, numdays):
        """Adds a number of days to the
        date in the indicated cell.
        """
        cell = self.wb.get_sheet(0).cell(int(row), int(column))
        if cell.ctype == XL_CELL_DATE:
            self.wb.sheets()
            if not self.tb:
                self.tb = copy(self.wb)
            curval = datetime(*xldate_as_tuple(cell.value, self.wb.datemode))
            newval = curval+timedelta(int(numdays))
            plain = easyxf('', num_format_str='d.M.yy')
            self.tb.get_sheet(0).write(int(row),
                                       int(column),
                                       newval,
                                       plain)

    def subtract_from_date(self, row, column, numdays):
        """Subtracts a number of days from the
        date in the indicated cell.
        """
        cell = self.wb.get_sheet(0).cell(int(row), int(column))
        if cell.ctype == XL_CELL_DATE:
            self.wb.sheets()
            if not self.tb:
                self.tb = copy(self.wb)
            curval = datetime(*xldate_as_tuple(cell.value, self.wb.datemode))
            newval = curval-timedelta(int(numdays))
            plain = easyxf('', num_format_str='d.M.yy')
            self.tb.get_sheet(0).write(int(row),
                                       int(column),
                                       newval,
                                       plain)

    def save_excel(self, fname):
        """Saves the Excel file indicated by fname"""
        print '*DEBUG* Got fname %s' % fname
        self.tb.save(os.path.join(self.slash, self.tmpDir, fname))

    def create_excel(self):
        """Creates a new Excel workbook"""
        self.tb = Workbook()
        self.tb.add_sheet('Sheet 1')
        
    def row_count(self,  sheetname):
        RowCount =self.wb.sheet_by_name(sheetname).nrows
        return  RowCount
        
    def col_count(self, sheetname):
        ColCount =self.wb.sheet_by_name(sheetname).ncols
        return  ColCount 
    
    def Close_Excel(self):
        self.wb = None

    def get_row_count(self, sheetname):
        """
        Returns the specific number of rows of the sheet name specified.

        Arguments:
                |  Sheet Name (string)  | The selected sheet that the row count will be returned from. |
        Example:

        | *Keywords*          |  *Parameters*                                      |
        | Open Excel          |  C:\\Python27\\ExcelRobotTest\\ExcelRobotTest.xls  |
        | Get Row Count       |  TestSheet1                                        |

        """
        sheet = self.wb.sheet_by_name(sheetname)
        return sheet.nrows

    def read_cell_data_by_coordinates(self, sheetname, column, row):
        """
        Uses the column and row to return the data from that cell.

        Arguments:
                |  Sheet Name (string)  | The selected sheet that the cell value will be returned from.         |
                |  Column (int)         | The column integer value that the cell value will be returned from.   |
                |  Row (int)            | The row integer value that the cell value will be returned from.      |
        Example:

        | *Keywords*     |  *Parameters*                                              |
        | Open Excel     |  C:\\Python27\\ExcelRobotTest\\ExcelRobotTest.xls  |   |   |
        | Read Cell      |  TestSheet1                                        | 0 | 0 |

        """
        #my_sheet_index = self.sheetNames.index(sheetname)
        sheet = self.wb.sheet_by_name(sheetname)
        cellValue = sheet.cell(int(row), int(column)).value
        return cellValue

    def get_column_count(self, sheetname):
        """
        Returns the specific number of columns of the sheet name specified.

        Arguments:
                |  Sheet Name (string)  | The selected sheet that the column count will be returned from. |
        Example:

        | *Keywords*          |  *Parameters*                                      |
        | Open Excel          |  C:\\Python27\\ExcelRobotTest\\ExcelRobotTest.xls  |
        | Get Column Count    |  TestSheet1                                        |

        """
        sheet = self.wb.sheet_by_name(sheetname)
        return sheet.ncols
     
