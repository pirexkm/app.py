 

   
 

import json
import os

 
 
import subprocess
import time
import socket
import requests
import random
from protobuf_decoder.protobuf_decoder import Parser
import json
import time
import threading
from byte import *
from accountmangment import *
from like import *
from datetime import datetime
import base64
 
import sys
import time

 
 
 
def dec_to_hex(ask):
    ask_result = hex(ask)
    final_result = str(ask_result)[2:]
    if len(final_result) == 1:
        final_result = "0" + final_result
        return final_result
    else:
        return final_result
def convert_to_hex(PAYLOAD):
    hex_payload = ''.join([f'{byte:02x}' for byte in PAYLOAD])
    return hex_payload
def convert_to_bytes(PAYLOAD):
    payload = bytes.fromhex(PAYLOAD)
    return payload
def GET_LOGIN_DATA(JWT_TOKEN , PAYLOAD):
    url = 'https://clientbp.common.ggbluefox.com/GetLoginData'
    headers = {
        'Expect': '100-continue',
        'Authorization': f'Bearer {JWT_TOKEN}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB43',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
        'Host': 'clientbp.common.ggbluefox.com',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    response = requests.post(url, headers=headers, data=PAYLOAD)
    response = response.text[60:]
    return response



def GET_PAYLOAD_BY_DATA(JWT_TOKEN , NEW_ACCESS_TOKEN):
    token_payload_base64 = JWT_TOKEN.split('.')[1]
    token_payload_base64 += '=' * ((4 - len(token_payload_base64) % 4) % 4)
    decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode('utf-8')
    decoded_payload = json.loads(decoded_payload)
    NEW_EXTERNAL_ID = decoded_payload['external_id']
    SIGNATURE_MD5 = decoded_payload['signature_md5']
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    PAYLOAD = b'\x1a\x132023-12-24 04:21:34"\tfree fire(\x01:\x081.102.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\rEMS - MobinilZ\x04WIFI`\x80\nh\xc0\x07r\x03320z\x1eARM64 FP ASIMD AES VMH | 0 | 6\x80\x01\xbf.\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.0\x9a\x01+Google|6ec2d681-b32f-4b2d-adc2-63b4c643d683\xa2\x01\x0e156.219.174.33\xaa\x01\x02ar\xb2\x01 4666ecda0003f1809655a7a8698573d0\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x0cgoogle G011A\xea\x01@15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6\xf0\x01\x01\xca\x02\rEMS - Mobinil\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xe6\xdb\x02\xe8\x03\xff\xbb\x02\xf0\x03\xaf\x13\xf8\x03\xfc\x04\x80\x04\xaf\xca\x02\x88\x04\xe6\xdb\x02\x90\x04\xaf\xca\x02\x98\x04\xe6\xdb\x02\xc8\x04\x03\xd2\x04?/data/app/com.dts.freefireth-2kDmep_84HTIG7I7CUiJxw==/lib/arm64\xe0\x04\x01\xea\x04_df3bb3771c4b2d46f751a3e7d0347ba7|/data/app/com.dts.freefireth-2kDmep_84HTIG7I7CUiJxw==/base.apk\xf0\x04\x03\xf8\x04\x02\x8a\x05\x0264\x9a\x05\n2019116797\xa8\x05\x03\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xca\x05 \x11\\\x10F\x07][\x05\x1e\x00XL\x0fXEZ\x149]R[]\x05b\nZ\t\x05`\x0eU5\xd2\x05\x0eShibin al Kawm\xda\x05\x03MNF\xe0\x05\xa6A\xea\x05\x07android\xf2\x05\\KqsHT+kkoTQE5BlBobUYX1gU2WQkP3UxRmOCvqs5/lkAGJsABcsIABFyS2oXUc9QDamooQF50iepFI53iz6yQPfFRAw=\xf8\x05\xac\x02'
    PAYLOAD = PAYLOAD.replace(b"2023-12-24 04:21:34" , formatted_time.encode("UTF-8")) 
    PAYLOAD = PAYLOAD.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6" , NEW_ACCESS_TOKEN.encode("UTF-8"))
    PAYLOAD = PAYLOAD.replace(b"4666ecda0003f1809655a7a8698573d0" , NEW_EXTERNAL_ID.encode("UTF-8"))
    PAYLOAD = PAYLOAD.replace(b"7428b253defc164018c604a1ebbfebdf" , SIGNATURE_MD5.encode("UTF-8"))
    PAYLOAD = PAYLOAD.hex()
    PAYLOAD = encrypt_api(PAYLOAD)
    PAYLOAD = bytes.fromhex(PAYLOAD)
    HOST = GET_LOGIN_DATA(JWT_TOKEN , PAYLOAD)
    return HOST
def guest_token(uid , password,uids):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {"Host": "100067.connect.garena.com","User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close",}
    data = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
    response = requests.post(url, headers=headers, data=data)
    data = response.json()
    NEW_ACCESS_TOKEN = data['access_token']
    NEW_OPEN_ID = data['open_id']
    OLD_ACCESS_TOKEN = "37c00ba521e42f7fb8e374a2b5d07c2417e054abca6d7e0f25a83a8243f1d00a"
    OLD_OPEN_ID = "c5a8e6bfd6ff9246a9cc4e043f7f5753"
    data = TOKEN_MAKER(OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,uid,uids)
def TOKEN_MAKER(OLD_ACCESS_TOKEN , NEW_ACCESS_TOKEN , OLD_OPEN_ID , NEW_OPEN_ID,uid,account_iddd):
        
        PYLOAD = b'C\xb9\xed\x02\xee;\xe0W6\xe1\xd6&\x9d4Q3\xb3\xb4\x92\xa6\xae\xcf\x16\xfe\xf4\x9e\xe3R\x99h%\xee~I_\x85\x99\xc8f\xf8\xb7/\xa7/k\xe2k\xb3\x92\xfd\xf6\xe3\x96\x1e[\xaae\x11d\x12\xda\xd8\xfb+\x82X\xf0gW\xae>\x0c\xdd\xda@\xa4\xa0]bW\xeb\xd2s>\xb1\x110\xe4os\x91\x98 \xe2\x9c\xed\xd5\xfavI\x8a\xadR\x1b\xe0g0f\xd3\x98Xc\x1fU\xd1!\x12!\'\x14\x85\xaf\x8c\x1d\x9a\x99\xdcS\x84\xbe\x82\xfd:.m\xc9\re6r\xb0\x81\xa8\xf3\xef\xb6?,\x1a\xbe1\xce\xf6\xebu{H\xe3\xdcQ \xac\xcd\x08\x01\x84qJk\x8f\x9dn\xe97\xd8&\x97\xdc_t3y\xd2\xccy\xd1z\x83\xae\xf8o\x84\xb2\xf4(ZH\xfa\'\xd6/\xad\x0b\x90\x99\xe5\xab\x00\xec\xd7rE\x90\x8b\x1f\xddA\xe3J2\xe0\xe9\xd8\x10I\x80\xdaJ^\xbc\x8b\xf1Q)c\x99\xc5>,b\x89w\xf6D\xbc\xdcg\xed\xeekI-\x1etX\xf8B<_\x1a\x1fo\x02\x81}\xe6\xe7\x95\xab^\t\xda\xc4\x18\x93\x16\x93T\x89-\x8f\xb9\x8al\x01\xa9\t\xd1\xb0s\x1d^\x021c \x91\xccc\x91\xec\xf5\xf3g\xdb\x11\x15JgYm7\xa1\x17\xc6U\xd4\xde\xb6v\x83\xf6\xb5Kg!q\xdf9l\xe4`H\xcf\xbc\xba\x93j6%hl\x9d\x0e\xbf\xb0\xd7\x0ff\xf0\xcf\x06P5\x8f\xe1\xb2\xfc\xadJ\xf5IY\x93\xd8\xd3\xee\x01\xb5\xa1\xbd\x03-n\xa2%I\x07\x15I\xe1\x19\xec\x14VF\x86\x99\xad\xd3\xcc\xe3\x07\xcb)\xa3\xaf\xf0J\x13W\x03\rI\xed\xfd!\x1b\x18\x87\xe1\xab\xb1\xde\xacj\x87\\\xa3v\xb9]\xa6\xd8\n:3[u\xd0\xf4y\xd9\xfa\n`\x9c\x19f#\xf8\xc4\xba\x12\xb4\xe5\x03;\x1c\xc3\xd6Q\xd3\xc7%\t\x7f\x93/\x82h\xbaO\xfd\xb9\xb1\x93W\xf8\\-\xa1L\x11\x9a\xd7\xcf\xb8%\x03+\x8a\xf1v\x80\xd6\x86 \x0b\x1at\xf6\xdf8\xf0W\xb3\x0cG\x8f\xb6\xcd\xf5\xb5\\/(-\xaeI\xa494c!\xce&g`\xf1F\x18V\x87-\xc4\x8efP\xaa\x91\xef\xe2\xf3"\xb6A\x00\xe7j\xa5~Dii\x8f\xe4\x93\xf0YM\xab\x07\x05d\xba\x01\xa6z\xff\xc9r\xd2\xf2<R,W \xf0\x97\xe6\xb9t\xf5l\xf7\x87\xc8\xb8\x16\xccy\xf7\xe9\x1b\x1d:\xad\xb2%\xec\xc2\xe8N\x12\xe5\xda\x08\xa9\xd2\x07j|\xc9\xad\xef\xed\r\xcfC2\xb6Ew\x94\xcb]\xa7\x94qVr\x8c=\xa0\x8d\xf8\x1a\xa6M\xd61y\xce%L\x95CK7\x03\xaeo\xa7u4\x82\xb7R\x83\xd0(<\x0e\x0f\xf7\xeb\xdb\x8e\xb8o)u\x9a\xd7\\/\x07*\xc9`\xd0\x9dtl\xf7\xefY\xf8\xb7\xbe\xa7q\xf5\xf6b\x11K\xf1\x96\xd4\xb6\xa3\xa1\xca\x9c\xef\xbb\xa4uq\xb5\xaf\xf4}\x07:T\xbd\xb3\xac\xd9yB\xb8\x80\x02\xa7\xcb:\xe3\x11\x07[\x127\xe1\xe2\x1e\xab!\x1f\xee\xec\x8b\x86\xc7\x82\x9ejj\xb0\x8dl\n\x1cTc \'v\xdf\n\x17\x9a\x95^\xaa#Z\xad\x12\xb4\xd3\xed\xa6q\x08\xab\x0e\xf3\x12\x06\xa2p\xf0\x1do\x01\x8c\xad\x87\x02\xb0I\x8d\xd6L(\xb3\x12~\xbc\xb2u$^\xb1\xbf\x98m\xd9\xd2\x02\xb2\xb3\xab\x1a\xc2 \x81X)a\x19\x84\xcc\xb3\x97FM\x0cSO\xce/\xbf+\xc1"V\xc1\xc1z\xd8\xb6\x08\x95\xd3\x85\xd5,\xba\x10\xc2\xb9}m\xc2,\xe1#MW\xe9\x93lc\x90\x02\xf3\x181\xde\x83\xcb\xc0]\xf8\xa8\xe8\xc4\xaf\xe4\xebI\xd3\xea\xad\x99\x10\xc3eX\x8da\xab\xd9\x0f\xe4\x98\xa2\xa7h<u\xcd\xbf\x1c\x15"\xd2Q\xfdU\x89\x8b\xefd\x87\xec'
        a = convert_to_hex(PYLOAD)
        data = bytes.fromhex(decrypt_api(a))
        data = data.replace(OLD_OPEN_ID.encode(),NEW_OPEN_ID.encode())
        data = data.replace(OLD_ACCESS_TOKEN.encode() , NEW_ACCESS_TOKEN.encode())
        d = encrypt_api(data.hex())
        Final_Payload = convert_to_bytes(d)
        URL = "https://loginbp.common.ggbluefox.com/MajorLogin"
        headers = {"Expect": "100-continue","Authorization": "Bearer ","X-Unity-Version": "2018.4.11f1","X-GA": "v1 1","ReleaseVersion": "OB46","Content-Type": "application/x-www-form-urlencoded","Content-Length": str(len(Final_Payload.hex())),"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N975F Build/PI)","Host": "loginbp.common.ggbluefox.com","Connection": "close","Accept-Encoding": "gzip, deflate, br"}
        RESPONSE = requests.post(URL, headers=headers, data=Final_Payload,verify=False)
        if RESPONSE.status_code == 200:
            if len(RESPONSE.text) < 10:
                return False
            BASE64_TOKEN = RESPONSE.text[RESPONSE.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6IjEiLCJ0eXAiOiJKV1QifQ"):-1]
            second_dot_index = BASE64_TOKEN.find(".", BASE64_TOKEN.find(".") + 1)
            BASE64_TOKEN = BASE64_TOKEN[:second_dot_index+44]
            print(BASE64_TOKEN)
            code =   like(BASE64_TOKEN,account_iddd)
            if code != 200:
                delete_account_by_id(uid)
                random_accounts = get_random_account ()
                for account in random_accounts:
                    print(f"{account[0]}, {account[1]}")
                    id =   account[0]
                    password =   account[1]
                    tok2 = threading.Thread(target=guest_token, args=(id, password))
                    time.sleep(0.1)
                    tok2.start()
        else:
            return False
def start_like(uid):
    random_accounts = get_random_accounts()
    for account in random_accounts:
        print(f"{account[0]}, {account[1]}")
        id =   account[0]
        password =   account[1]
        time.sleep(0.050)
        tok2 = threading.Thread(target=guest_token, args=(id, password,uid))
        tok2.start()
 