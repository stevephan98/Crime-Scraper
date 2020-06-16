import re
import json
import requests
from bs4 import BeautifulSoup

url = 'https://ofsistorage.blob.core.windows.net/publishlive/ConList.html'
soup = BeautifulSoup(requests.get(url).content, 'html.parser')

persons = []
for li in soup.select('li:has(b:contains("Name 6:"))'):
    name = [name.find_next_sibling(text=True).strip() for name in li.select('b')[:6]]
    name = [n for n in name if '/' not in n]
    if len(name) > 1:
        last, *_, first = name
    else:
        last, first = '-', name[0]

    dob = li.select_one('b:contains("DOB:")')
    dob = dob.find_next_sibling(text=True).strip().replace('\xa0', '') if dob else '-'

    pob = li.select_one('b:contains("POB:")')
    pob = pob.find_next_sibling(text=True).strip().replace('\xa0', '') if pob else '-'

    nationality = li.select_one('b:contains("Nationality:")')
    nationality =  nationality.find_next_sibling(text=True).strip().replace('\xa0', '') if nationality else '-'

    gender = re.findall(r'((?:fe)?male)', li.get_text(strip=True, separator=' '), flags=re.I)
    gender = gender[0] if gender else '-'

    other = li.select_one('b:contains("Other Information:")')
    other =  other.find_next_sibling(text=True).strip().replace('\xa0', '') if other else '-'

    persons.append(
        {
        'firstname': first,
        'lastname': last,
        'about': {
            'date_of_birth': dob,
            'place_of_birth': pob,
            'nationality': nationality,
            'gender': gender
        },
        'other': other
    })
    
with open('data.json', 'w') as f:
    json.dump(persons, f)