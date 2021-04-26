import pickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
def calbration_undistort(img,objpoints,imgpoints):
	ret,mtx,dist,rvecs,tvecs = cv2.calibrateCamera(objpoints,imgpoints,(img.shape[0],img.shape[1]),None,None)
	undist = cv2.undistort(img,mtx.dist,None,mtx)
	return undist
def generate_data():
	nx = 9 # the number of inside corners in x
	ny = 6 # the number of inside corners in y
	objpoints = [] # 3d points in world space(meter with z axis)
	imgpoints = [] # 2d points in pixel(image) space
	images = glob.glob('./camera_cal/calibration*.jpg')
	size = nx*ny
	objp = np.zeros((size,3),np.float32)
	for row in range(0,6):
		for col in range(0,9):
			index = row*nx + col
			objp[index][0] = col
			objp[index][1] = row
	print(objp)
	for frame in images:
	    img = mpimg.imread(frame)
	    print("[dbg]:the name of picture:"+frame)
	    filename = frame.split('/')[2]
	    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	    ret,corners = cv2.findChessboardCorners(gray,(9,6),None)
	    if(ret == True):
	    	imgpoints.append(corners)
	    	objpoints.append(objp)
	    	img = cv2.drawChessboardCorners(img,(9,6),corners,ret)
	    	cv2.imwrite('./camera_chessboard/'+filename,img)
	    else:
	    	print(filename+":have error in return")
	dict = {}
	dict['obj'] = objpoints
	dict['img'] = imgpoints
	savefile = open('./data.pickle','wb')
	pickle.dump(dict,savefile)
	savefile.close()
generate_data()