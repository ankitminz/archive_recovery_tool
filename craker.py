import pyzipper
import py7zr
import rarfile
import itertools
import time
import os
from PyPDF2 import PdfFileReader, PdfFileWriter


A_Z = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
a_z = "abcdefghijklmnopqrstuvwxyz"
symbols = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
nums = "0123456789"
master = nums + a_z + A_Z + symbols

global file_type #0-zip, 1-7z, 2-rar, 3-pdf

while(True):
    path = input("Type in the complete path of file\n")
    if path.endswith('.zip'):
        file_type = 0
        break
    elif path.endswith('.7z'):
        file_type = 1
        break
    elif path.endswith('.rar'):
        file_type = 2
        break
    elif path.endswith('.pdf'):
        file_type = 3
        break
    else:
        print("\nGiven file type is not supported. Only zip, 7z, rar and pdf are supported")

print("\nBy default a new directory having same name as that of archive will be made in this parent directory and all contents of archive will be extracted in it. Pdf file is extracted in same directory as that of original file by default and '_decrypted' is appended to its name.")


while(True):
    try:
        custom = int(input("1. Give custom extraction path\n2. Keep default extraction path\n"))
        if custom == 1:
            ex_path = input("\nType in your custom extraction path\n")
            break
        elif custom == 2:
            i = 0
            if(file_type == 3):
                directoryPath = "".join([path[:-4], "_decrypted.pdf"])
                ex_path = directoryPath
                while(os.path.isfile(ex_path)):
                    i += 1
                    ex_path = directoryPath[:-4] + str(i) + ".pdf"
                break
            index1 = path.rfind("\\")
            index2 = path.rfind(".")
            directoryName = path[index1 + 1 : index2]
            parentDirectory = path[:index1 + 1]
            directoryPath = parentDirectory + directoryName
            ex_path = directoryPath
            while(True):
                try:
                    os.mkdir(ex_path)
                    break
                except(FileExistsError):
                    i += 1
                    ex_path = directoryPath + str(i)
                    
            break
        else:
            print("\nEnter 1 or 2")
    except(ValueError):
        print("\nEnter 1 or 2")



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
                print("\n\nFile decrypted successfully\nPassword found = {}".format(password), end = '')
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
    except Exception as e:
        print("\n{}".format(e))
        return True
    
    
def sevenz_extractor(password, start, count, ex_path):

    '''Function to extract 7z file'''
    
    flag = False
    try:
        with py7zr.SevenZipFile(path, mode = 'r', password = password) as szf:
            try:
                szf.extractall(path = ex_path)
                print("\n\nFile decrypted successfully\nPassword found = {}".format(password))
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
    except Exception as e:
        print("\n{}".format(e))
        return True
    


def rar_extractor(password, start, count, ex_path):
    
    '''Function to extract rar file'''
    
    flag = False
    try:
        with rarfile.RarFile(path) as rf:
            try:
                rf.extractall(path = ex_path, pwd = bytes(password.encode('utf8')))
                print("\n\nFile decrypted successfully\nPassword found = {}".format(password))
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
    except Exception as e:
        print("\n{}".format(e))
        return True
    


def pdf_extractor(password, start, count, ex_path):
    
    '''Function to extract encrypted pdf file'''
    
    flag = False
    myFile = PdfFileReader(path)
    if myFile.isEncrypted == True:
        try:
            myFile.decrypt(password)
            out = PdfFileWriter()
            for idx in range(myFile.numPages):
                page = myFile.getPage(idx)
                out.addPage(page)

            with open(ex_path, "wb") as f:
                out.write(f)
                print("\n\nFile decrypted Successfully.")
   
            print("Password found = {}".format(password), end = '')
            flag = True
            return flag
        except(NotImplementedError):
            print("NotImplementedError: Only 40 and 128 bit RC4 algorithm is suported")
            return True
        except:
            t = time.monotonic() - start
            t = convertf(t)
            print("\rElapsed time = {}:{}:{} Attempt = {} Password failed = {}                    "
            .format(t[0], t[1], t[2], count, password), end = '', flush = True)

    else:
        print("\nFile already decrypted.")
        return True



def brute_force(extractor, characters, min_len, max_len, prefix, suffix):
    
    '''Function to iterate all permutation with repetition'''
    
    print("\nIn progress")
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
    
    print("\nIn progress") 
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


method1 = 0
dict_path = ""
min_len = 0
max_len = 0
char_set = ""
prefix = ""
suffix = ""

print()
while(True):
    try:
        method1 = int(input("Choose the type of attack.\n1. Dictionary attack\n2. Brute force attack\n"))

        if method1 == 1:
            dict_path = input("\nEnter path of dictionary\n")
            break
            
        elif method1 == 2:
            print()
            while(True):
                try:
                    min_len = int(input("Enter minimum lenght of password\n"))
                    if(min_len > 0):
                        break
                    else:
                        print("\nEnter a positive integer greater than 0")
                except(ValueError):
                    print("\nEnter a positive integer greater than 0")
            print()
            
            while(True):
                try:
                    max_len = int(input("Enter maximum length of password\n"))
                    if(max_len >= min_len):
                        break
                    else:
                        print("\nEnter a positive integer greater than or equal to {}".format(min_len))
                except(ValueError):
                    print("\nEnter a positive integer greater than or equal to {}".format(min_len))
            
            print()
            while(True):
                try:
                    method2 = int(input("Choose the character set.\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n6. Give your own charcater set\n".format(nums, a_z, A_Z, symbols, master)))
                
                    if method2 == 1:
                        char_set = nums
                        break
                    elif method2 == 2:
                        char_set = a_z
                        break
                    elif method2 == 3:
                        char_set = A_Z
                        break
                    elif method2 == 4:
                        char_set = symbols
                        break
                    elif method2 == 5:
                        char_set = master
                        break
                    elif method2 == 6:
                        char_set = input("Enter your own characters\n")
                        break
                    else:
                        print("\nEnter 1, 2, 3, 4, 5 or 6")
                except(ValueError):
                    print("\nEnter 1, 2, 3, 4, 5 or 6")
            break
        else:
            print("\nEnter 1 or 2")
    except(ValueError):
        print("\nEnter 1 or 2")

print()
while(True):
    try:
        method3 = int(input("Additional options\n1. Give prefix\n2. Give suffix\n3. Give both prefix & suffix\n4. Neither prefix nor suffix\n"))

        if method3 == 1:
            prefix = input("\nType the prefix\n")
            suffix = ""
            break
        elif method3 == 2:
            suffix = input("\nType the suffix\n")
            prefix = ""
            break
        elif method3 == 3:
            prefix = input("\nType the prefix\n")
            suffix = input("\nType the suffix\n")
            break
        elif method3 == 4:
            prefix = ""
            suffix = ""
            break
        else:
            print("\nEnter 1, 2, 3 or 4")
    except(ValueError):
        print("\nEnter 1, 2, 3 or 4")
    
if method1 == 1:
    if file_type == 0:
        dictionary_attack(zip_extractor, dict_path, prefix, suffix)
    elif file_type == 1:
        dictionary_attack(sevenz_extractor, dict_path, prefix, suffix)
    elif file_type == 2:
        dictionary_attack(rar_extractor, dict_path, prefix, suffix)
    elif file_type == 3:
        dictionary_attack(pdf_extractor, dict_path, prefix, suffix)
elif method1 == 2:
    if file_type == 0:
        brute_force(zip_extractor, char_set, min_len, max_len, prefix, suffix)
    elif file_type == 1:
        brute_force(sevenz_extractor, char_set, min_len, max_len, prefix, suffix)
    elif file_type == 2:
        brute_force(rar_extractor, char_set, min_len, max_len, prefix, suffix)
    elif file_type == 3:
        brute_force(pdf_extractor, char_set, min_len, max_len, prefix, suffix)
    
print("\nProcess completed\n")
input()



    
