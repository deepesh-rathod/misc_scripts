import re
def get_valid_phone(phone_number):
    digits = re.findall(r'\d', phone_number)[-10:]
    if len(digits):
        return ''.join(digits)
    else:
            return None
    
phn = get_valid_phone("(480) 444-6311")
print(0)