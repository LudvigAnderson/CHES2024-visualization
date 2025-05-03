import pdfplumber

start_page = 16

with pdfplumber.open("CHES_2024_Codebook.pdf") as pdf:
    text = ""
    for page in pdf.pages[(start_page-1):]:
        text += page.extract_text_simple()
    
    with open("codebook.txt", "w", encoding="utf-8") as file:
        file.write(text)

# NOTE: The authors of the PDF have made a mistake in the naming of a question.
# I therefore fix this manually on line 182: spendvstax --> spendvtax.
#
# There are also two places in the result that makes the regex more complicated,
# so I make a manual edit in the resulting .txt file.
# The edit is to remove the newline on line 323, then on line 321, and finally on line 159.
