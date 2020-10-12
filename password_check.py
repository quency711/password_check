import requests
import hashlib
import sys

def hash_transfer(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5_char, tail = sha1password[:5],sha1password[5:]
    return first_5_char, tail

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char[:5]
    res = requests.get(url)
    res_code = res.status_code
    res_txt = res.text
    if res_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res_txt

def get_password_leak_counts(password):
    hash_5, hash_to_check = hash_transfer(password)
    res_txt = request_api_data(hash_5)
    hash_res_stored = (line.split(":") for line in res_txt.splitlines())
    for h, count in hash_res_stored:
        if h == hash_to_check:
            return count
    return 0

def main(args):
    for password in args:
        ct = get_password_leak_counts(password)
        if ct:
            print(f'{password} was found {ct} times. You may want to change it!')
        else:
            print(f'{password} was NOT found! Carry On!')
    return "Done!"

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
