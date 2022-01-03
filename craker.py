import pyzipper
import py7zr
import rarfile
import itertools
import time


A_Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
a_z = "abcdefghijklmnopqrstuvwxyz"
symbols = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
nums = "0123456789"
master = nums + a_z + A_Z + symbols

global file_type #0-zip, 1-7z, 2-rar

while(True):
    path = input("Type in the complete path of archive file\n")
    if path.endswith('.zip'):
        file_type = 0
        break
    elif path.endswith('.7z'):
        file_type = 1
        break
    elif path.endswith('.rar'):
        file_type = 2
        break
    else:
        print("\nGiven file type is not supported. Only zip, 7z, and rar are supported")

print("\nDefault path of extraction is the directory of this program")
custom = int(input("Type 1 or 2 according to your choice\n1. Give custom extraction path\n2. Keep default extraction path\n"))

if custom == 1:
    ex_path = input("\nType in your custom extraction path\n")
elif custom == 2:
    ex_path = None
else:
    ex_path = None



def convertf(fractional_second):

    '''Function to convert fractional seconds to hours, minutes and seconds'''
    
    hour = 0
    minute = 0
    second = 0
    
    if fractional_second < 60:
        second = int(fractional_second)
    elif fractional_second < 3600:
        minute = int(fractional_second) // 60
        second = int(fractional_second) % 60
    else:
        hour = int(fractional_second) // 3600
        minute = int(fractional_second) % 3600
        second = minute % 60
        minute = minute // 60
        
    return(hour, minute, second)


def zip_extractor(password, start, count, ex_path):
    
    '''Function to extract zip file encrypted with AES'''
    
    flag = False
    try:
        with pyzipper.AESZipFile(path, 'r') as zf:
            try:
                zf.extractall(path = ex_path, pwd = bytes(password.encode('utf8')))
                print("\n\nPassword found = {}".format(password), end = '')
                flag = True
                return flag
            except:
                t = time.monotonic() - start
                t = convertf(t)
                print("\rElapsed time = {}:{}:{} Attempt = {} Password failed = {}                    "
                .format(t[0], t[1], t[2], count, password), end = '', flush = True)
            
    except(FileNotFoundError):
        print("\nNo such file or directory found")
        return True
    except:
        print("\nOops! some error occured")
        return True
    
    
def sevenz_extractor(password, start, count, ex_path):

    '''Function to extract 7z file'''
    
    flag = False
    try:
        with py7zr.SevenZipFile(path, mode = 'r', password = password) as szf:
            try:
                szf.extractall(path = ex_path)
                print("\n\npassword found = {}".format(password))
                flag = True
                return flag
            except:
                t = time.monotonic() - start
                t = convertf(t)
                print("\rElapsed time = {}:{}:{} Attempt = {} Password failed = {}                     "
                .format(t[0], t[1], t[2], count, password), end = '', flush = True)
                
    except(FileNotFoundError):
        print("\nNo such file or directory found")
        return True
    


def rar_extractor(password, start, count, ex_path):
    
    '''Function to extract rar file'''
    
    flag = False
    try:
        with rarfile.RarFile(path) as rf:
            try:
                rf.extractall(path = ex_path, pwd = bytes(password.encode('utf8')))
                print("\n\nPassword found = {}".format(password))
                flag = True
                return flag
            except:
                t = time.monotonic() - start
                t = convertf(t)
                print("\rElapsed time = {}:{}:{} Attempt = {} Password failed = {}                     "
                .format(t[0], t[1], t[2], count, password), end = '', flush = True)
                
    except(FileNotFoundError):
        print("\nNo such file or directory found")
        return True
    


def brute_force(extractor, characters, min_len, max_len, prefix, suffix):
    
    '''Function which will do iteration of all possible password combinations in characters 
    also known as brute force attack'''
    
    print("Press any button on keyboard to stop and exit the program (For Windows users only)\nUsers of other platforms should force stop the program to stop and exit it while it is in operation")
    start = time.monotonic()
    count = 1
    flag = False
    for L in range(min_len, max_len + 1):
        if flag == True:
            break
        for x in itertools.product(characters, repeat = L):
            password = prefix + ''.join(x) + suffix
            flag = extractor(password, start, count, ex_path)
            
            if flag == True:
                break
            
            count += 1


def dictionary_attack(extractor, dict_path, prefix, suffix):
    
    '''Function to do dictionary attack
    It will try each word separated by new line in given dictionary'''
    
    print("Press any button on keyboard to stop and exit the program (For Windows users only)\nUsers of other platforms should force stop the program to stop and exit it while it is in operation") 
    flag1 = False
    count = 1
    start = time.monotonic()
    with open(dict_path, 'r') as text:
        while flag1 == False:
            for word in text.readlines():
                password = prefix + word.strip() + suffix
                flag1 = extractor(password, start, count, ex_path)
                
                if flag1 == True:
                    break
                    
                count += 1


global flag2
flag2 = False
global flag3
flag3 = True

while flag3 == True:
    method = int(input("\nChoose the type of attack. Type 1, 2 or 3 according to your choice\n1. Dictionary attack\n2. Brute force attack\n3. Exit\n"))

    if method == 1:
        dict_path = input("\nType in the path of dictionary\n")
        dict_path = dict_path.replace("\\", "/")
        dict_path = Path(dict_path)
       
    elif method == 2:
        min_len = int(input("\nType in minimum lenght of password\n"))
        max_len = int(input("\nType in maximum length of password\n"))
        method_2 = int(input("\nChoose the character set. Type 1, 2, 3, 4, 5 or 6 according to your choice.\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n6. Want to give your own charcater set\n".format(nums, a_z, A_Z, symbols, master)))
    
        if method_2 == 1:
            char_set = nums
        elif method_2 == 2:
            char_set = a_z
        elif method_2 == 3:
            char_set = A_Z
        elif method_2 == 4:
            char_set = symbols
        elif method_2 == 5:
            char_set = master
        elif method_2 == 6:
            char_set = input("Type in your own characters\n")
        else:
            print("\nType 1, 2, 3, 4, 5 or 6 as choice")
            continue
    elif method == 3:
        break
    else:
        print("\nType 1, 2 or 3 as choice")
        continue
    
    while True:
        method_1 = int(input("\nType 1, 2, 3, 4 or 5 according to your choice\n1. Give prefix\n2. Give suffix\n3. Give both prefix & suffix\n4. Neither prefix nor suffix\n5. Back\n"))
    
        if method_1 == 1:
            prefix = input("\nType the prefix\n")
            suffix = ""
        elif method_1 == 2:
            suffix = input("\nType the suffix\n")
            prefix = ""
        elif method_1 == 3:
            prefix = input("\nType the prefix\n")
            suffix = input("\nType the suffix\n")
        elif method_1 == 4:
            prefix = ""
            suffix = ""
        elif method_1 == 5:
            flag2 = True
            break
        else:
            print("\nType 1, 2, 3, 4 or 5 as choice")
            continue
        
        if method == 1:
            if file_type == 0:
                dictionary_attack(zip_extractor, dict_path, prefix, suffix)
                flag3 = False
                break
            elif file_type == 1:
                dictionary_attack(sevenz_extractor, dict_path, prefix, suffix)
                flag3 = False
                break
            elif file_type == 2:
                dictionary_attack(rar_extractor, dict_path, prefix, suffix)
                flag3 = False
                break
        elif method == 2:
            if file_type == 0:
                brute_force(zip_extractor, char_set, min_len, max_len, prefix, suffix)
                flag3 = False
                break
            elif file_type == 1:
                brute_force(sevenz_extractor, char_set, min_len, max_len, prefix, suffix)
                flag3 = False
                break
            elif file_type == 2:
                brute_force(rar_extractor, char_set, min_len, max_len, prefix, suffix)
                flag3 = False
                break
            
    if flag2 == True:
        continue
    
print("\nProcess completed\n")
input()



    
