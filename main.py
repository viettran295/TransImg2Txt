import easyocr 
import csv 
import re

def WriteCsv(filename: str, trans: list[str]):
    """
    Write list of string to csv file
    """
    trans.insert(0, ["Date", "State", "Symbol", "Amount", "Price value"])
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(trans)
    
def TransImg2Txt(imgPath: str) -> list[list[str]]:
    """
    Convert transaction image from Scalable trading platform to txt
    """
    reader = easyocr.Reader(['en'])
    res = reader.readtext(imgPath)
    txt = []
    tmp = []
    col_idx = 0
    for i in range(len(res)):
        char = res[i][1]
        char = re.sub(';+', '', char)
        tmp.append(char)
        col_idx += 1
        if col_idx == 5:
            txt.append(tmp.copy())
            tmp.clear()
            col_idx = 0
    return txt

if __name__ == "__main__":
    imgPath = './img/mstr2.png'
    trans = TransImg2Txt(imgPath)
    print(trans)
    WriteCsv('transaction.csv', trans)