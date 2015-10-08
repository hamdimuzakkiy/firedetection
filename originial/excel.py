__author__ = 'hamdiahmadi'
import xlwt


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

