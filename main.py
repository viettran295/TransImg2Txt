import easyocr 

def TransImg2Txt(imgPath: str) -> str:
    """
    Convert transaction image from Scalable trading platform to txt
    """
    reader = easyocr.Reader(['en'])
    res = reader.readtext(imgPath)
    txt = ""
    for i in range(len(res)):
        char = res[i][1]
        txt += char + ', '
        if '€' in char:
            txt += "\n"
    return txt

if __name__ == "__main__":
    imgPath = './img/transactions.png'
    print(TransImg2Txt(imgPath))