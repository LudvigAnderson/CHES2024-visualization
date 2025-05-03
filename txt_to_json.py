import re
import json


# note that I needed to make some manual edit in codebook.txt as explained in pdf_to_txt.py
with open("codebook.txt", "r", encoding="utf-8") as file:
    text = file.read()

# the question pattern gets:
#   "judicial_independence",
#
#   "Position on JUDICIAL INDEPENDENCE  ",
#
#   "0 = the judiciary should be independent 
#   . 
#   10 = the government should have influence over the judiciary "
question_pattern = r"(\w+):\s((?:.|\n)+?)((?:\d+\s*=\s*.+\s(?:\.\s*)*)+)"

# the values pattern gets:
#   "0",
#   "the judiciary should be independent"
values_pattern = r"(\d+)\s*=\s*(.+)"


question_matches = re.findall(question_pattern, text)
data = {}

for match in question_matches:
    question_code = match[0].strip()
    question_description = match[1].replace("\n", "").strip()
    values_text = match[2]

    values_matches = re.findall(values_pattern, values_text)

    values = []
    value_descriptions = []
    for value_match in values_matches:
        values.append(int(value_match[0]))
        value_descriptions.append(value_match[1].strip())
    
    value_description_pairs = dict(zip(values, value_descriptions))
    

    data[question_code] = {                     # "corrupt_salience" (key)
        "description" : question_description,   # "How salient has REDUCING POLITICAL CORRUPTION been to each party in 2024?"
        "values" : value_description_pairs,     # {"0" : "not important at all", "10" : "extremely important"}
        "range" : [min(values), max(values)]    # [0, 10]
    }

with open("codebook.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=2, ensure_ascii=False)