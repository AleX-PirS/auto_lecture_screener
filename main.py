from PIL import Image, ImageGrab
from datetime import datetime
import os
import cv2
import difflib
import time
import pytils.translit

def namer():
	current = datetime.now()
	keydata = str(current.date()).replace('-', '_')
	keytime = str(current.time()).replace('.', ':')
	keytime = keytime.replace(':', '_')
	name = keydata + '_' + keytime + '.bmp'
	
	return(name)

def CompareHash(hash1,hash2):
    l=len(hash1)
    i=0
    count=0
    while i<l:
        if hash1[i]!=hash2[i]:
            count=count+1
        i=i+1
    return count

def CalcImageHash(FileName):
    image = cv2.imread(FileName) #Прочитаем картинку
    resized = cv2.resize(image, (32, 32), interpolation = cv2.INTER_AREA) #Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) #Переведем в черно-белый формат
    avg=gray_image.mean() #Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0) #Бинаризация по порогу
    
    #Рассчитаем хэш
    _hash=""
    for x in range(32):
        for y in range(32):
            val=threshold_image[x,y]
            if val==255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
            
    return _hash

setting_sence = input('Нужно ли настроить чувствительность? Если нет, просто Enter, если да, то введите любой символ:\n')
if len(setting_sence) < 1:
	FACTOR = 2
else :
	while True:
		FACTOR = input('Введите чувствительность, целое число, где 0 - одно и то же фото (стандартная=2):\n')
		try:
			FACTOR = int(FACTOR)
			break
		except: 
			print('Чувствительность должна быть целым числом!')
			continue

setting_time = input('Нужно ли настроить задержку между проверками экрана? Если нет, просто Enter, если да, то введите любой символ:\n')
if len(setting_time) < 1:
	SLEEP_TIME = 1
else :
	while True:
		SLEEP_TIME = input('Введите задержку между проверками экрана в секундах (стандартная=1сек):\n')
		try:
			SLEEP_TIME = int(SLEEP_TIME)
			break
		except:
			print('Задержка - цисло!')
			continue

name_of_lecture = pytils.translit.translify(input('Введите название предмета: '))
 
name_of_folder = name_of_lecture + '_' +str(datetime.now().date()) + '_' + str(datetime.now().time())[:8].replace(':', '-')
os.mkdir(name_of_folder)

first_name = name_of_folder + '/' + namer()
second_name = ''

raw_img = ImageGrab.grab()
raw_img.save(first_name, "BMP")

count = 0
while True:
	time.sleep(SLEEP_TIME)
	second_name = name_of_folder + '/' + namer()
	raw_img = ImageGrab.grab()
	raw_img.save(second_name, "BMP")

	hash1=CalcImageHash(first_name)
	hash2=CalcImageHash(second_name)

	compare = CompareHash(hash1, hash2)

	if compare <= FACTOR:
		os.remove(second_name)
		continue
	else:
		count += 1
		first_name = second_name

	print(hash1)
	print(hash2)
	print(CompareHash(hash1, hash2), 'count =', count)
