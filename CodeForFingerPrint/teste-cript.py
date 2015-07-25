import cv2
import numpy as np
import hashlib
import cPickle
from pysimplesoap.client import SoapClient


img = cv2.imread('img1.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT(100)
kp = sift.detect(gray,None)

key = []
bla = ''
for i in kp:
    bla = str(i.pt)
    key.append(bla)
print(len(key))
len_key = len(key)
teste = []
for i in range(len_key):
    teste.append(hashlib.md5(key[i]).hexdigest())
print(teste)

str1 = ','.join(str(e) for e in teste)
#f = open("keypoints-teste.txt", "w")
#teste = key[0:-1]
#f.write(teste)
print('fim')


def test_soap_sub():
    print('passou aqui')
    client = SoapClient(wsdl="http://127.0.0.1:8000/TG/webservice/call/soap?WSDL")   


    response = client.getKeyPointPerson(auth='0DDEE29FAA57CF9DBEE480986E7B0686',
                                   person_data={'full_name':'Samara Cardoso dos Santos', 'email':'samara.cardoso@urbemobile.com.br', 
                                                'cellphone':'12988211378', 'birth_date':'03-27-1994',
                                                'keypoints':str1})
    try:
        result = response
        print(result)
    except SoapFault as e:
        result = e
    return dict(xml_request=client.xml_request, 
                xml_response=client.xml_response,
                result=result)


test_soap_sub()
