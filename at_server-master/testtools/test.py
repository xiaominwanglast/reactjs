import requests,threading

url = 'http://t2-managerdaikuan.2345.com/foundation-oss/fs/uploadFile?us=iDx7xglcXlgWo9tUZ2O%2Fqr080yiEKbHo2YYdsA2PRKQwMf4biuDrAg%3D%3D'
f = open('/Users/xiaosong/Desktop/ceshipng.jpg', 'rb')

def uploadFile(url,f):
    data = {'file': f}
    print(1,f.readlines())
    result = requests.post(url, files=data)
    print(result.text)


threading.Thread(target=uploadFile, args=(url,f)).start()
threading.Thread(target=uploadFile, args=(url,f)).start()

