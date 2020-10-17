import cv2
import numpy as np
import time

whT = 320 # target width
confThr = 0.5
nmsThr = 0.5

xScal = 2
yScal = 1.5
wScal = 2
hScal = 2

feed = cv2.VideoCapture(0)

classDict = {
 1: u'person',
 2: u'bicycle',
 3: u'car',
 4: u'motorcycle',
 5: u'airplane',
 6: u'bus',
 7: u'train',
 8: u'truck',
 9: u'boat',
 10: u'traffic light',
 11: u'fire hydrant',
 12: u'stop sign',
 13: u'parking meter',
 14: u'bench',
 15: u'bird',
 16: u'cat',
 17: u'dog',
 18: u'horse',
 19: u'sheep',
 20: u'cow',
 21: u'elephant',
 22: u'bear',
 23: u'zebra',
 24: u'giraffe',
 25: u'backpack',
 26: u'umbrella',
 27: u'handbag',
 28: u'tie',
 29: u'suitcase',
 30: u'frisbee',
 31: u'skis',
 32: u'snowboard',
 33: u'sports ball',
 34: u'kite',
 35: u'baseball bat',
 36: u'baseball glove',
 37: u'skateboard',
 38: u'surfboard',
 39: u'tennis racket',
 40: u'bottle',
 41: u'wine glass',
 42: u'cup',
 43: u'fork',
 44: u'knife',
 45: u'spoon',
 46: u'bowl',
 47: u'banana',
 48: u'apple',
 49: u'sandwich',
 50: u'orange',
 51: u'broccoli',
 52: u'carrot',
 53: u'hot dog',
 54: u'pizza',
 55: u'donut',
 56: u'cake',
 57: u'chair',
 58: u'couch',
 59: u'potted plant',
 60: u'bed',
 61: u'dining table',
 62: u'toilet',
 63: u'tv',
 64: u'laptop',
 65: u'mouse',
 66: u'remote',
 67: u'keyboard',
 68: u'cell phone',
 69: u'microwave',
 70: u'oven',
 71: u'toaster',
 72: u'sink',
 73: u'refrigerator',
 74: u'book',
 75: u'clock',
 76: u'vase',
 77: u'scissors',
 78: u'teddy bear',
 79: u'hair drier',
 80: u'toothbrush'}

classNames = [classDict[i] for i in range(1, len(classDict)+1)]

modelConfig = 'yolov3.cfg'
modelWeight = 'yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeight)

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)

print('OpenCL avail: ', cv2.ocl.haveOpenCL())

def findObject(outputs, img):
  ht, wt, ct = img.shape
  bbox = []
  classIds = []
  conf = []

  for i in outputs:
    for de in i:
      scores = de[5:]
      classId = np.argmax(scores)
      confi = scores[classId]
      if confi > confThr:
        w,h = int(de[2]*whT), int(de[3]*whT)
        x,y = int((de[0]*whT)-w/2), int((de[1]*whT)-h/2)
        bbox.append([x,y,w,h])
        classIds.append(classId)
        conf.append(float(confi))
  indices = cv2.dnn.NMSBoxes(bbox, conf, confThr, nmsThr)
  for i in indices:
    i = i[0]
    box = bbox[i]
    x,y,w,h = box[0]*xScal,int(box[1]*yScal),box[2]*wScal,box[3]*hScal
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    lbl = str(classNames[classIds[i]]) + ': ' + str(int(conf[i] * 100)) + '%'
    print(lbl)
    cv2.putText(img, lbl, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

while True:

  startTime = time.time()

  suc, img = feed.read()

  blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], crop=False)
  net.setInput(blob)

  layerNames = net.getLayerNames()
  outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]


  # pass data in
  outputs = net.forward(outputNames)
  findObject(outputs, img)

  endTime = time.time()
  # show FPS
  fps = 'fps: ' + str(int(100*(endTime-startTime)))
  cv2.putText(img, fps, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
  cv2.imshow('thing', img)

  cv2.waitKey(1)