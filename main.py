# coding: utf-8
import os
import wmi
import dynamic
from hashlib import md5
import hashlib
import pytesseract
from PIL import Image
import webbrowser
from selenium import webdriver

def screenshot():
    os.system('adb shell screencap -p /sdcard/.screencap/2.png')
    os.system('adb pull /sdcard/.screencap/2.png .')

def get_cpu_info() :
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        cpu_id = cpu.ProcessorId.strip()     
        print ("机器码为 :", cpu_id)
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


def startRec():
    global browser
    browser = webdriver.Chrome()
    #browser = webdriver.Firefox()
    software = input("选择APP,输入对应序号回车：\n1.西瓜视频（百万英雄）\n2.冲顶大会\n3.优酷\n4.蘑菇街\n5.网易\n6.UC\n")
    if software == '1':
        qbox  = (100,400,1000,600)
        abox_1 = (110,750,800,820)
        abox_2 = (110,930,800,1000)
        abox_3 = (110,1130,800,1200)
    elif software == '2':
        qbox  = (50,350,1000,550)
        abox_1 = (110,670,800,750)
        abox_2 = (110,840,800,900)
        abox_3 = (110,1000,800,1070)
    elif software == '3':
        qbox  = (0,400,1000,700)
        abox_1 = (180,750,800,810)
        abox_2 = (180,960,800,1030)
        abox_3 = (180,1180,800,1240)
    elif software == '4':
        qbox  = (50,600,1000,800)
    elif software == '5':
        qbox  = (220,500,900,700)
        abox_1 = (260,800,800,860)
        abox_2 = (260,970,800,1030)
        abox_3 = (260,1140,800,1210)
    elif software == '6':
        qbox  = (100,400,1000,600)
        abox_1 = (200,680,800,750)
        abox_2 = (200,900,800,960)
        abox_3 = (200,1120,800,1180)        
    else:
        print("错误：未选择APP\n")
        startRec()
    while input("按回车开始识别 : ") != '0':
        screenshot()
        img2 = Image.open("./2.png")
        qimg = img2.crop(qbox)
        aimg_1 = img2.crop(abox_1)
        aimg_2 = img2.crop(abox_2)
        aimg_3 = img2.crop(abox_3)
        qimg.save("./crop.png")
        aimg_1.save("./aimg_1.png")
        aimg_2.save("./aimg_2.png")
        aimg_3.save("./aimg_3.png")
        question = pytesseract.image_to_string(qimg,lang='chi_sim')
        answer_1 = pytesseract.image_to_string(aimg_1,lang='chi_sim')
        answer_2 = pytesseract.image_to_string(aimg_2,lang='chi_sim')
        answer_3 = pytesseract.image_to_string(aimg_3,lang='chi_sim')
        
        print(question)
        print(answer_1)
        print(answer_2)
        print(answer_3)
        question=question.replace(' ','').replace('\n','')

        answer_1=answer_1.replace(' ','').replace('\n','')
        answer_2=answer_2.replace(' ','').replace('\n','')
        answer_3=answer_3.replace(' ','').replace('\n','')
        question=question[question.find('.') + 1:question.find('?')]
        #webbrowser.open("https://www.baidu.com/s?ie=UTF-8&wd=" + question,new = 0)
        browser.get("https://www.baidu.com/s?ie=UTF-8&wd=" + question)
        js_1 = "document.getElementById(\"content_left\").innerHTML = document.getElementById(\"content_left\").innerHTML.split(\""+ answer_1 + "\").join('<span style=\"background:\#00FF00;\">"+ answer_1 + "</span> ')"
        js_2 = "document.getElementById(\"content_left\").innerHTML = document.getElementById(\"content_left\").innerHTML.split(\""+ answer_2 + "\").join('<span style=\"background:\#FFFF00;\">"+ answer_2 + "</span> ')"
        js_3 = "document.getElementById(\"content_left\").innerHTML = document.getElementById(\"content_left\").innerHTML.split(\""+ answer_3 + "\").join('<span style=\"background:\#00FFFF;\">"+ answer_3 + "</span> ')"
             
        if answer_1 != '':
            browser.execute_script(js_1)
        if answer_2 != '':
            browser.execute_script(js_2)
        if answer_3 != '':
            browser.execute_script(js_3)


def checkLisence():
    global user_id 
    if os.path.exists("Lisence") != True:
        user_id = input("请输入注册码 : ")
        fh = open("Lisence",'w')
        fh.write(user_id)
        fh.close()
        checkLisence()
    elif os.path.exists("Lisence") == True:
        user_id = open("./Lisence").read()
        if user_id != CPU_ID_ENCRYPY:
            user_id = input("授权文件与本机不匹配，请重新授权 : ")
            fh = open("Lisence",'w')
            fh.write(user_id)
            fh.close()
            checkLisence()
        elif user_id == CPU_ID_ENCRYPY:
            startRec()


def main():
    global CPU_ID 
    CPU_ID= get_cpu_info()
    global CPU_ID_ENCRYPY 
    CPU_ID_ENCRYPY = str(encrypy(CPU_ID))
    checkLisence()


if __name__ == '__main__':
    main()