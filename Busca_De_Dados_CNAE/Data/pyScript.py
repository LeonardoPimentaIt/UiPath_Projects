from unicodedata import normalize
import re as re

def removeAccents(strToChange):

	return normalize('NFKD', strToChange.lower()).encode('ASCII', 'ignore').decode('ASCII')

def keepOnlyNumbers(strToChange):
    num = re.findall(r'[0-9]+',strToChange)
    return "".join(num)