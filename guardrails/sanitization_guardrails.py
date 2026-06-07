from guardrails.hub import DetectPII
from guardrails import Guard

guard = Guard().use(
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="fix")
)

USER_INPUT = """
Hello, my name is aryan. please write an email draft with the following info:
subject: request for 7 PTO
my email: aryan@networknuts.net
my phone number: 9326532664
receiver email: info@networknuts.net
"""

try:
    result = guard.validate(USER_INPUT)
    print(result)
except Exception as e:
    print(f"Error: {e}")