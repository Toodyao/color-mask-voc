#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.cElementTree as ET
import numpy as np
import cv2

file_name = 'paris_007.xml'

annotation = ['wall', 'sky', 'roof', 'chimney', 'door', 'shop', 'window', 'balcony']

# color (B, G, R)
color = {'window': (0, 0, 255), 'wall': (0, 255, 255), 'balcony': (255, 0, 128), 'door': (0, 128, 255),
         'roof': (255, 0, 0), 'chimney': (128, 128, 128), 'sky': (255, 255, 128), 'shop': (0, 255, 0)}


def draw(shape_xml, draw_name):
    if shape_xml.tag == 'bndbox':
        cv2.rectangle(img, (int(float(shape_xml[0].text)), int(float(shape_xml[1].text))),
                      (int(float(shape_xml[2].text)), int(float(shape_xml[3].text))), color[draw_name], -1)
    if shape_xml.tag == 'polygon':
        points = shape_xml.getchildren()
        points_np = np.empty((0, 2), np.uint8)
        # print(draw_name, np.array([int(points[0].text), int(points[1].text)]))
        for i in range(0, len(points)-1, 2):
            curr = np.array([int(float(points[i].text)), int(float(points[i+1].text))])
            points_np = np.vstack((points_np, curr))
        # print(points_np)
        cv2.fillConvexPoly(img, points_np, color[draw_name])


tree = ET.parse(file_name)
root = tree.getroot()

size_xml = root.find('size')
width = int(size_xml.find('width').text)
height = int(size_xml.find('height').text)
depth = int(size_xml.find('depth').text)

# Create image
img = np.zeros([height, width, depth], np.uint8)

# Draw wall as background
cv2.rectangle(img, (0, 0), (width, height), color['wall'], -1)

# Draw in order of annotation list
for i in range(0, len(annotation)):
    for obj in root.findall('object'):
        obj_name = obj.find('name').text
        if obj_name == annotation[i]:
            draw(obj[4], obj_name)

cv2.imshow("test", img)
cv2.imwrite("test.png", img)
cv2.waitKey(0)
