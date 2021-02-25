from flask import Flask,request,jsonify
import urllib.request
from PIL import Image
import json 
import numpy as np
from skimage.io import imread, imshow
import cv2
import os
import re
from skimage.filters import prewitt_h,prewitt_v
import skimage.measure
import matplotlib.pyplot as plt
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

IMG_DIR = "C:/Users/Sven2219/Desktop/flags/"

@app.route("/",methods=['POST','GET'])
@cross_origin()
def res():
    if(request.method=='POST'):
        res = request.get_json('name')
        path = str(res["name"])
        img_array = imread(IMG_DIR+path, as_gray=True)
        img_array = cv2.resize(img_array, (20, 16))
        edges_prewitt_vertical = prewitt_v(img_array)
        img_array = edges_prewitt_vertical
        img_array = skimage.measure.block_reduce(img_array, (2, 2), np.max)
        #azure conn
        url = 'https://ussouthcentral.services.azureml.net/workspaces/c0b4ca8ee9184b3bb5a36a323f73602b/services/1a0eda8a2f1d43eeada0d7bf06d37498/execute?api-version=2.0&details=true'
        api_key = 'uqnW5IlpMk+Oa6wCKCuX+KE5iBzPy7LYVirZWksrpncL1wv18RIh+RFLWJujCJg59gK33e0Bf1kLivMynFjsnw=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key),'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type,Authorization','Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,OPTIONS'}
        formatedList = []
        img_array = (img_array.flatten())
        #convert array of numbers to array of string
        for i in range(len(img_array)):
            t = str(img_array[i])
            formatedList.append(t)
        
        formatedList.append('')


        data =  {
            "Inputs": {
                    "input1":
                    {
                        "ColumnNames": ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p25", "p26", "p27", "p28", "p29", "p30", "p31", "p32", "p33", "p34", "p35", "p36", "p37", "p38", "p39", "p40", "p41", "p42", "p43", "p44", "p45", "p46", "p47", "p48", "p49", "p50", "p51", "p52", "p53", "p54", "p55", "p56", "p57", "p58", "p59", "p60", "p61", "p62", "p63", "p64", "p65", "p66", "p67", "p68", "p69", "p70", "p71", "p72", "p73", "p74", "p75", "p76", "p77", "p78", "p79", "p80", "Class"],
                        "Values": [formatedList]
                    },        
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))
        req = urllib.request.Request(url, body, headers) 
        response = urllib.request.urlopen(req)

        result = response.read()
        parsedResult = json.loads(result)
        data = parsedResult["Results"]["output1"]["value"]["Values"]
        datalen = len(data[0])
        return str(data[0][datalen-1])
    else:
        return 'Get request'
    

if __name__ == '__main__':
    app.run(port=5000,debug=True)