# FaceDetection_dlib
This is a face detection based on dlib and it can help you automatically put on the glasses on your face.

Here is the basic ideal
- first using dlib library to detect face and landmark(contains 5 landmarks)
- then derive the point coordinates of eye corner
- caculate the area of eyes 
- caculate the glasses area scale factor based on eyes' area
- add the glasses on the eyes

## The result shown below(Thr original picture is test.jpg)

![result](https://github.com/Birdylx/FaceDetection_dlib/blob/master/test_with_glass.jpg?raw=true)
