import re 

USER_INPUT = """
Hello, my name is aryan and my email is 
ARYAN@example.com. Please draft from my prespective
to my employer which is info@example.net asking for
7 days off.
"""

normalized_input = USER_INPUT.lower()

result = re.search(r"[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z]+",normalized_input)

matches = re.findall(r"[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z]+",normalized_input)

refinded_expression = re.findall(r"\w+@\w+\.\w+",normalized_input)

sanitized_input = re.sub(r"\w+@\w+\.\w+","USER_EMAIL",normalized_input)

WEBSERVER_INPUT = """
10.0.0.1 [01/01/2026 18:00:00] /app.html 200
"""

sanitized_input_1 = re.search(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",WEBSERVER_INPUT)

sanitized_input_2 = re.search(r"\d+\.\d+\.\d+\.\d+",WEBSERVER_INPUT)

sanitized_input_3 = re.sub(r"\d+\.\d+\.\d+\.\d+","IPV4_ADDRESS",WEBSERVER_INPUT)
print(sanitized_input_3)