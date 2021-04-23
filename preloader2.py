#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author(s): Jonathan Robinson (@robin0025) & Catherine Kennon (@kennonc)

###########################################################################
#
# Set of functions for descriminate preloading (to RAM) and displaying preloaded images.
# containing:
# 1 - folderLister = Use function to take string from prompt
#
# 2 - preLoadFolder = for folder loading and excluding
#	Simple One folder no exclusion example:
#	- #PRELOAD IMAGES
#   	- stimFolder = "STIMULI"
# 	- #Images must be in same folder
#       - #LoadedImg, path = preloader2.preLoadFolder(win, 'png', [stimFolder])
#
# 3 - preLoadpwd = just load PWD
#
# 4 - RECOMMENDED: preloadMinImg = Load any image files appearing in excel (with no dupplicates)
# 	- window = display variable being used, 
#       - THVar = Trial Handler Variable, 
#	- imgColList = List of names of image column in excel, 
#	- folder = folder for images)
#
# 5 - preloadXlsx1Col = This function preloads an image to the XLSX file already loaded
#	- window = display variable being used
#	- THVar = Trial Handler Variable 
#	- imgFile = name of image column in excel

# 6 - imgMatchFolder = match up request image with loaded image and component
#	- Example image match (replace imgComp.setImage(imgFile))	
#       - imgMatchFolder(LoadedImg, <imgFile.jpg>, img_0)
#
# 7 - imgMatchPwd = matches images loaded from pwd (this and above can probably be merged)
#
# 8 - xlsxSingleMatcher = loads ordered images based on count.
###########################################################################


import os, sys, glob
from psychopy import visual
path = os.getcwd()



# Use function to take string from prompt
def folderLister(taskStrList): #takes a list object for each of the columns typed in.
    loadList = []
    for task in taskStrList: #go through each 'task' ...list item
        folders = task.split(" ") #split them into folders
        for fold in folders:
            if fold not in loadList: #if the folder name hasn't been added to the list then append it.
                loadList.append(fold)
    return(loadList) #return string list of unique folders use as folderList arguement in 'preLoadFolder'


# Function allows you to either use simple folder loading 
def preLoadFolder(window,fileType,folderList=['NaN'],excludList=['NaN'],subFolder='NaN'):
    imgList = []
    imgObjList = []
    if 'NaN' in folderList:
        for infile in glob.glob(os.path.join(path,('*.' + fileType))):
#            imgList.append(infile)
            IdMatch = 0 #reset rejector
            for excl in excludList:
                if path+'/'+'/'+excl in infile: #find excluded identities
                    IdMatch = IdMatch+1 #if excluded add to counter
                else:
                    continue
            if IdMatch != 1: #if not excluded append
               imgList.append(infile) 
            else:
                continue
    else:
        if 'NaN' in subFolder:
            #print('No stim subfolder for readability we recommend the following structure "SCRIPTFOLDER/GENERALSTIM_FOLDER/STIM_FOLDER/STIM.png"')
            for folder in folderList: #look through each subdirectory
                for infile in glob.glob(os.path.join(path,(folder+'/*.'+fileType))): #for files with filetype ending loop through them
                    IdMatch = 0 #reset rejector
                    for excl in excludList:
                        if path+'/'+folder+'/'+excl in infile: #find excluded identities
                            IdMatch = IdMatch+1 #if excluded add to counter
                        else:
                            continue
                    if IdMatch != 1: #if not excluded append
                       imgList.append(infile) 
                    else:
                        continue
        else:
            for folder in folderList: #look through each subdirectory
                for infile in glob.glob(os.path.join(path,(subFolder+'/'+folder+'/*.'+fileType))): #for files with filetype ending loop through them
                    IdMatch = 0 #reset rejector
                    for excl in excludList:
                        if path+'/'+subFolder+'/'+folder+'/'+excl in infile: #find excluded identities
                            IdMatch = IdMatch+1 #if excluded add to counter
                        else:
                            continue
                    if IdMatch != 1: #if not excluded append
                       imgList.append(infile) 
                    else:
                        continue
    #print imgList
    for img in imgList:
        imgObjList.append(visual.ImageStim(window, img, ori=0, pos=[0, 0])) #make base image stim objects
        imgObjList[-1].image = img
    
    
    return (imgObjList,path)




def preLoadpwd(window, fileType): #This function preloads images based on items in the experiment folder with two important arguments
    #(window = display variable being used, fileType = the image filetype)
    imgList = []
    imgObjList = []
    for infile in glob.glob(os.path.join(path,('*.' + fileType))):
        imgList.append(infile)
    for img in imgList:
        imgObjList.append(visual.ImageStim(window, img, ori=0, pos=[0, 0]))
        imgObjList[-1].image = img
    return (imgObjList,path)
    

###Below functions are for non duplicate images in excel document.###             
def preloadMinImg(window, THVar, imgColList, folder): #This function preloads an image from the XLSX file already loaded
    #(window = display variable being used, THVar = Trial Handler Variable, imgColList = name of image column in excel, folder = folder for images)
    # use with imgMatchFolder()
    #Can be used with either sequential of randomly handled trials.
    imgMatch = []
    for ind in THVar.sequenceIndices:
        Trial = THVar.trialList[ind]
	for imgCol in imgColList:
	    if Trial.imgCol not in imgMatch:
                imgMatch.append(Trial.imgCol)
    
    # Make list of images with path attached
    imgList = []
    imgObjList = []
    for item in imgMatch:
	for infile in glob.glob(os.path.join(path,(folder+'/'+item))):
            imgList.append(infile)
    
    # Actually load images 
    for img in imgList:
        imgObjList.append(visual.ImageStim(window, img, ori=0, pos=[0, 0]))
        imgObjList[-1].image = img
    

    return (imgObjList,path)



###Below functions are for loading every single image appearing in your excel document.###             
def preloadXlsx1Col(window, THVar, imgFile): #This function preloads an image to the XLSX file already loaded
    #(window = display variable being used, THVar = Trial Handler Variable, imgFile = name of image column in excel)
    #ONLY TO BE USED FOR UNIQUE IMAGE PER TRIAL SITUATION
    #Can be used with either sequential of randomly handled trials.
    imgMatch = []
    for ind in THVar.sequenceIndices:
        Trial = THVar.trialList[ind]
        imgMatch.append(Trial.imgFile)

    imgList = []
    imgObjList = []
    for item in imgMatch:
        for infile in glob.glob(os.path.join(path,item)):
            imgList.append(infile)
    for img in imgList:
        imgObjList.append(visual.ImageStim(window, img, ori=0, pos=[0, 0]))
        imgObjList[-1].image = img
    return (imgObjList,path)


def imgMatchFolder(imgObjList, imgFile, imgComp): #This function matches images to the file already loaded
    #(loaded = variable of loaded image objects, imgFile = name of image column in excel, imgComp = name of the image component) 
    print('WARNING: recommend images names padded with zeros')
    for img in imgObjList:
        if imgFile in img.image: #more efficient way to look for images
            imgComp.setImage(img.image)
    if imgFile == None:
        imgComp.setImage(imgFile)
        

def imgMatchPwd(imgObjList, imgFile, imgComp): #This function matches images to the file already loaded
    #(loaded = variable of loaded image objects, imgFile = name of image column in excel, imgComp = name of the image component) 
    for img in imgObjList:
        if img.image == (os.path.join(path, str(imgFile))):
            imgComp.setImage(img.image)
    if imgFile == None:
        imgComp.setImage(imgFile)


def xlsxSingleMatcher(imgObjList, countVar, imgComp): #This function just takes the problem out of the hands of the user, it requires the user to make a count variable to iterate through
    #(imgObjList = an image object created by another function, countVar = a count variable added to in your paradigm, imgComp = The image component needing to be filled)
    imgComp.setImage(imgObjList[countVar].image)
    
    
    
