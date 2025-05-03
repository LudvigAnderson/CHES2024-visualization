import pdfplumber
import json

start_page = 2

with pdfplumber.open("CHES_2024_Codebook.pdf") as pdf:
    page = pdf.pages[start_page-1]
    rows = page.extract_table()

# rows looks like:
# [['1', 'BE', 'Belgium', '22', 'EST', 'Estonia'], ['2', 'DK', 'Denmark', '23', 'HUN', 'Hungary'], ... ]

country_names = {row[i].lower() : row[i+1] for row in rows for i in [1, 4]}

priority = ["nor", "sv", "dk"] # Norway, Sweden, Denmark to be shown on top

top_countries = [(k, country_names[k]) for k in priority]

the_rest = [(k, v) for k, v in country_names.items() if k not in priority]
the_rest = sorted(the_rest, key=lambda x : x[1])

final_dict = dict(top_countries + the_rest)

with open("country_names.json", "w", encoding="utf-8") as json_file:
    json.dump(final_dict, json_file, indent=2, ensure_ascii=False)