# -*- coding: utf-8 -*-

import logging
import requests
from bs4 import BeautifulSoup
import os
import time

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
app = Flask(__name__)


# ------------------------------------------ api ------------------------------------------
@app.route("/api/detect_EPISODE_num", methods=['GET', 'POST'])
def detect_EPISODE_num():
    url="https://www.cartoonmad.com/comic/1221.html"
    r = requests.get(url)
    r.encoding = 'big5'

    soup = BeautifulSoup(r.text, 'html.parser')


    #str = soup.find_all('table').prettify()
    result = soup.find_all('table', attrs={"width":800})
    #logging.debug(str)
    #logging.debug(type(result) )

    result_list = []
    #for x in result:
    #    result_list.append(str(x))

    result_list.append(str(result[1]))
    r2=''.join(result_list)
#=========================

    soup2 = BeautifulSoup(r2, 'html.parser')
    result2=soup2.find_all('a', href=True)


    result_list2 = []
    for x in result2:
        result_list2.append(str(x.getText()))
        #result_list2.append('<br>')




    #return ''.join(result_list2)

    return render_template('detect_EPISODE_num.html', result_list=result_list2)


@app.route("/api/get_EPISODE_head_img", methods=['GET', 'POST'])
def get_EPISODE_img():

    url = "https://www.cartoonmad.com/comic/122100002035001.html"


    r = requests.get(url)
    r.encoding = 'big5'

    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.find_all('img', attrs={"oncontextmenu":'return false'})

    result_list = []
    for image in images:
        #print image source
        print( image['src'] )

        result_list.append(image['src'])
    return render_template('get_EPISODE_head_img.html', result_list=result_list)


#from_EPISODE = '1',end_EPISODE = '2'
@app.route("/api/download/<imgUrl>/<from_EPISODE>/<end_EPISODE>", methods=['GET', 'POST'])
def download(imgUrl, from_EPISODE, end_EPISODE):

    download_util(url=imgUrl, epi_folder=EPISODE, idx=img_string)

    return render_template('download.html')

"""
    for EPISODE_int in range(int(from_EPISODE), int(end_EPISODE) + 1):

        EPISODE = fix_int_to_string(EPISODE_int)
        print('--- EPISODE:' + EPISODE + ' ---')

        running = True
        for x in one_to_infinity():
            if running == False:
                break

            img_string = fix_int_to_string(x)
            imgUrl = "http://web1.cartoonmad.com/c26vn522e83/1221/" + EPISODE + "/" + img_string + ".jpg"
            print('--- EPISODE:' + EPISODE + ' --- IMAGE:' + img_string)
            download(url=imgUrl, epi_folder=EPISODE, idx=img_string)
            time.sleep(0.2)

"""


# time.sleep( 0.2 )

    # ===========================================

def one_to_infinity():
    i = 1
    while True:
        yield i
        i += 1

def download_util(url, epi_folder, idx):
    try:
        if not os.path.exists('./img/' + epi_folder):
            os.makedirs('./img/' + epi_folder)
        myPath = os.path.abspath('./img/' + epi_folder)
        fullfilename = os.path.join(myPath, idx)
        urllib.request.urlretrieve(url, fullfilename)
    except Exception as e:
        print("Exception: ", e, " at ", url)
        global running
        running = False

# have bug when return str
# TypeError: can only concatenate str (not "NoneType") to str
def fix_int_to_string(x):
    if len(str(x)) == 1:
        fix_str = '00' + str(x)
        return fix_str

    elif len(str(x)) == 2:
        fix_str = '0' + str(x)
        return fix_str



#===========================================

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True,host='0.0.0.0')