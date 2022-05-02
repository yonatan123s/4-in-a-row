#import pyperclip as pc

# https://www.boi.org.il/he/ConsumerInformation/ToolsAndCalculators/Pages/Iban.aspx#

# iban_string = ""
iban_string = input("Enter IBAN: ")

iban_string = iban_string.replace(" ", "")


def remove_leading_zeros(string: str):
    while string[0] == "0":
        string = string[1:]
    return string


def get_from_iban_string(end_position: int):
    global iban_string

    # get the string and remove leading zeros
    return_string = iban_string[:end_position]
    return_string = remove_leading_zeros(return_string)

    # new start
    iban_string = iban_string[end_position:]

    return return_string


code_dict = {

    "country_code": get_from_iban_string(2),
    "bikoret_number": get_from_iban_string(2),
    "bank_code": get_from_iban_string(3),
    "sniff_code": get_from_iban_string(3),
    "account_number": remove_leading_zeros(iban_string),

}

# print(f"\n{code_dict}\n")

account_number = code_dict["account_number"]
print("Account Number:", account_number)
print(code_dict)
