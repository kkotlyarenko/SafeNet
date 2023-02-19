import requests
import ssl, socket
import cv2
import json
from base64 import urlsafe_b64encode

def VT_check(url):
    ansstring = '\nАнализ VirusTotal:\n'
    clean = 0
    unrated = 0
    dangerous = 0
    url_id = urlsafe_b64encode(url.encode('utf-8')).strip(b'=').decode('utf-8')
    api_url = "https://www.virustotal.com/api/v3/urls/" + url_id  # + "/analyse"
    headers = {"x-apikey": "bccf6a1248b2f26a7d34b19965cb47aa342ebd720d4ff77572d0f68c68bf9f23"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        for key in result['data']['attributes']['last_analysis_results']:
            if result['data']['attributes']['last_analysis_results'][key]['result'] == 'clean':
                clean += 1
            elif result['data']['attributes']['last_analysis_results'][key]['result'] == 'unrated':
                unrated += 1
            else:
                dangerous += 1
    ansstring += str(' Безопасно: ' + str(clean) + '\n Неизвестно: ' + str(unrated) + '\n Опасно: ' + str(dangerous))
    if dangerous >= 2:
        ansstring += "\nВердикт: Сайт опасен!"
    else:
        ansstring += "\nВердикт: Сайт безопасен!"
    return ansstring


def check_url(url):
    ansstring = ''
#проверка переаресации
    response = requests.get(url, verify=False)
    if response.history:
        ansstring += " Запрос был переадресован" + '\n'
        ansstring += " Последний пункт:" + '\n'
        url = response.url
        ansstring += '  ' + response.url + '\n'
    else:
        ansstring += " Запрос не был переадресован" + '\n'

# проверка безопасности переаресованной страницы
    if "https" in url:
        ansstring += " Переадресованная ссылка поддерживает HTTPS" + '\n'
    else:
        ansstring += " Переадресованная ссылка не поддерживает HTTPS" + '\n'

#изменение ссылки для проверки ssl
    temp = url.replace('https://', '')
    temp = temp.replace('http://', '')
    temp = temp.replace('www.', '')
    hostname = ""
    i = 0
    while temp[i] != '/':
        hostname += temp[i]
        i += 1
        if (i >= (len(temp))):
            break

#проверка ssl
    isssl = True
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        try:
            s.connect((hostname, 443))
            cert = s.getpeercert()
        except:
            isssl = False
            ansstring += " SSL сертификат не обнаружен"
    if isssl:
        subject = dict(x[0] for x in cert['subject'])
        issued_to = subject['commonName']
        issuer = dict(x[0] for x in cert['issuer'])
        issued_by = issuer['commonName']
        ansstring += " SSL: " + issued_to + ' ' + issued_by + '\n'

    return ansstring

def checkQR(image):
    resstring = ' '
    img = cv2.imread(image)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)

    if bbox is not None:
        qurl = f"{data}"
    else:
        return str("QR-код не обнаружен")
    resstring += "QR link: " + qurl + "\n"
    if "http" not in qurl:
        return str("Ссылка не обнаружена")
    i = 0
    cnt = 0
    temp = qurl
    qurl = ''
    while True:
        if temp[i] == '/':
            cnt += 1
        qurl += temp[i]
        i += 1
        if (i >= (len(temp))) or cnt == 3:
            break
    return str("Результат проверки QR: \n" + resstring + check_url(qurl) + VT_check(qurl))


def checkURL(url):
    return str("Результат проверки URL: \n" + check_url(url) + VT_check(url))
