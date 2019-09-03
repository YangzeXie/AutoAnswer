# encoding = utf-8  
import os, sys
import time
import wmi,zlib
from hashlib import md5
import hashlib

def get_cpu_info() :
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        cpu_id = cpu.ProcessorId.strip()     
        print ("cpu id:", cpu_id)
        return cpu_id

def encrypy(cpu_id):
	salt = ''
	len_chars = len(cpu_id) - 1  
	for i in range(len_chars):
		salt += cpu_id[len_chars - i]
	md5_obj = md5()
	md5_encrypy = md5_obj.update(cpu_id.encode("utf-8") + salt.encode("utf-8"))
	hash_encrypy = hashlib.sha1(str(md5_encrypy).encode("utf-8"))
	return hash_encrypy.hexdigest()
		



if __name__ == "__main__":
#     a = get_cpu_info()
    CPU_ID = get_cpu_info()
    CPU_ID_ENCRYPY = str(encrypy(CPU_ID))
    print (CPU_ID_ENCRYPY)