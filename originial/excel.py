__author__ = 'hamdiahmadi'
import xlwt
import xlrd
from xlutils.copy import copy

def save(data):
    book = xlwt.Workbook()
    sheets = book.add_sheet("TA")
    B = "B"
    R = "R"
    G = "G"
    variabel = [B,R,G]

    sheets.write(0,0,B)
    sheets.write(0,1,G)
    sheets.write(0,2,R)
    count = 1
    for x in data:
        sheets.write(count,0,int(x[0]))
        sheets.write(count,1,int(x[1]))
        sheets.write(count,2,int(x[2]))
        count+=1
    book.save("TA.xls")

def saveDataSet(file,content,classes):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(2)
    wb2 = copy(wb)
    data2 = wb2.get_sheet(2)
    col = 0
    for x in content :
        data2.write(data.nrows,col,x)
        col+=1
    data2.write(data.nrows,col,classes)
    wb2.save(file)

def retriveListDataset(file):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(1)
    res = []
    for x in range(1,data.nrows):
        content = data.row(x)
        tmp_res = []
        for idx,cell_obj in enumerate(content):
            tmp_res.append(str(cell_obj.value))
        res.extend([tmp_res])
    return res


def readDataSet(file):
    wb = xlrd.open_workbook(filename=file)
    data = wb.sheet_by_index(2)
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