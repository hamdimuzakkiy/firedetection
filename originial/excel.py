__author__ = 'hamdiahmadi'
import xlwt
import xlrd
from xlutils.copy import copy

def writeDataTraining(file,content,classes):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(0)
    wb2 = copy(wb)
    data2 = wb2.get_sheet(0)
    row = 0
    for x in content :
        for y in x:
            col = 0
            for z in y:
                data2.write(data.nrows+row,col,z)
                col+=1
            data2.write(data.nrows+row,col,classes)
            row+=1
    wb2.save(file)
    return

def readDataSet(file):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(0)
    res = []
    classes = []
    for x in range(1,data.nrows):
        content = data.row(x)
        tmp_res = []
        cnt = 0
        for idx,cell_obj in enumerate(content):
            if (cnt == 10):
                classes.append(str(cell_obj.value))
            else :
                tmp_res.append(float(cell_obj.value))
            cnt+=1
        res.extend([tmp_res])
    return res,classes

def writeAccuracy(file, content):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(0)
    wb2 = copy(wb)
    data2 = wb2.get_sheet(0)
    col = 0
    for x in content :
        data2.write(data.nrows,col,x)
        col+=1
    wb2.save(file)
    return