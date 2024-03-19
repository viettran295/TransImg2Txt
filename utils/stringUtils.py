import re 

def exclude_number(s: str) -> str:
    """
    Exclude numbers in string
    """
    numbers = re.findall(r'\d+', s)
    for num in numbers:
        s = s.replace(num, '')
    return s 

def extract_name(s: str) -> str:
    """
    Extract file name from path (e.g ./img/name1.png)
    """
    name_wExt = s.split('/')[-1].split('.')[0]
    return exclude_number(name_wExt)
