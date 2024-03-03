import easyocr 
import csv 
import os 
import re

def WriteCsv(filename: str, trans: list[str]):
    """
    Write list of string to csv file
    """
    col_name = ["Date", "State", "Symbol", "Amount", "Price value"]
    if not os.path.isfile(filename):
        trans.insert(0, col_name) 

    with open(filename, 'a') as file:
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
    imgPaths = ['./img/amd.png', './img/amzn.png', './img/coinb1.png', './img/coinb2.png', './img/meta1.png',
                './img/meta2.png', './img/mstr1.png', './img/mstr2.png', './img/nvda.png',]
    for img in imgPaths:
        trans = TransImg2Txt(img)
        WriteCsv('transaction.csv', trans)