import pickle
import json
import os

print('Welcome')
print('You can use this program to add or remove bounding boxes to the result of the auto annotation tool')

path_image = input('type the folder path of the RGB image: ')
path_bbox = input('type the folder path of the bounding box data: ')
bbox_type = input('what is the file format of the bounding box data (pickle/json): ')

def rem_bbox():
    ### load each bbox
    ### let user choose which bbox to remove
    ### return the number of removed bbox, and the bbox

def add_bbox():
    ### load each bbox
    ### let user choose the added bbox
    ### return the number of added bbox, and the bbox

def bbox_editor():
    ### ask want to add or remove
    ### call add_bbox if add is chosen
    ### call rem_bbox if rem is chosen
    ### print the number of change

def show_ori():
    ### load the image and show the resulting bbox
    ### ask user whether he want to make a change
    ### if yes, call bbox_editor
    ### if not, continue


#### iterate over the file

####
