import re

def email_is_valid(email: str) -> str:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    is_valid = False
    
    if(re.fullmatch(regex, email)):
        is_valid = True
    return is_valid

def password_is_valid(password: str) -> tuple:
    special_symbols = {'$', '@', '#', '%'}
    password_blacklist = {'111111', '222222', '333333', '444444', '555555', '666666', '777777', '888888', '999999', '000000', '123456', '012345'}
    is_valid = True
    messages = None

    if not any(char.isdigit() for char in password):
        messages = 'Passwords should have atleast one numeral.'
        is_valid = False
        return (is_valid, messages)
    
    if not any(char.isupper() for char in password):
        messages = 'Passwords should have atleast one Upper Case Letter.'
        is_valid = False
        return (is_valid, messages)

    if not any(char.islower() for char in password):
        messages = 'Passwords should have atleast one Lower Case Letter.'
        is_valid = False
        return (is_valid, messages)


    if not any(char in special_symbols for char in password):      
        messages = 'Passwords should have atleast one of the following symbols $, @, #, %.'
        is_valid = False
        return (is_valid, messages)


    if any(True for _ in password_blacklist if password.startswith(_)):
        messages = 'Your password is too simple. Please create a strong password.'
        is_valid = False
        return (is_valid, messages)

            
    return (is_valid, messages)