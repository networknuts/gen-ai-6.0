import re 

email_data = """
john <john@networknuts.net>
jane <jane@networknuts.net>
arthur <arthur@networknuts.net>
thomas <thomas@networknuts.net>
chris <chris@networknuts.net>
bobbi <bobbi@networknuts.net>
"""

# SIMPLE STRING SEARCHING
result_1 = re.search(r"[b,r]obb[i,y]",email_data)

# MULTIPLE MISSING LETTERS IN STRING - VARIANT 1
result_2 = re.search(r"chr[a-z][a-z]",email_data)

# MULTIPLE MISSING LETTERS IN STRING - VARIANT 2
result_3 = re.search(r"art[a-z]{3}",email_data)

# MULTIPLE MISSING LETTERS IN STRING - VARIANT 3 
result_4 = re.search(r"j[a-z]+",email_data)