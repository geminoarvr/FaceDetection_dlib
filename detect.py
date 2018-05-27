import numpy as np
import matplotlib.pyplot as plt
import cv2
import dlib

def add_glass():

    # dlib detect face and landmarks
    predictor_path = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)

    # detect face
    detector = dlib.get_frontal_face_detector()

    # cap = cv2.VideoCapture(0)
    img = cv2.imread("test.jpg")

    for i in range(1):
    # while cap.isOpened():
        # ret, img = cap.read()
        dets = detector(img, 1)

        # if detect face
        if len(dets) > 0:
            for d in dets:
                x, y, w, h = d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top()
                # cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

                # landmark detect
                shape = predictor(img, d)
                # for point in shape.parts():
                #     cv2.circle(img,(point.x,point.y),3,color=(0,255,0))

                #draw one face
                glass_img = plt.imread("眼镜.jpg")
                (nh, nw, nc) = glass_img.shape

                #寻找左右眼角坐标点，做差得到眼睛的宽度，计算眼镜缩放比例，得到眼镜缩放大小
                eye_left = shape.parts()[2]
                eye_right = shape.parts()[0]

                #添加padding，使眼镜放大一点，覆盖眼睛
                width = eye_right.x-eye_left.x+60
                ratio = width/nw
                height = int(nh*ratio)

                #创建两个蒙版，一层用于眼镜，一层用于原图
                glass_img = cv2.resize(glass_img, (width, height))
                glass_img_gray = cv2.cvtColor(glass_img, cv2.COLOR_BGR2GRAY)
                ret, glass_img_mask = cv2.threshold(glass_img_gray, 200, 255, cv2.THRESH_BINARY)
                glass_img_mask1 = cv2.bitwise_not(glass_img_mask)
                cv2.imshow("mask",glass_img_mask)
                cv2.imshow("mask1",glass_img_mask1)

                # bias偏置将镜框往上抬一点
                bias = 15
                roi = img[eye_left.y-bias:eye_left.y+height-bias,eye_left.x-30:eye_left.x+width-30].copy()

                img1_bg = cv2.bitwise_and(roi,roi,mask=glass_img_mask)
                img2_fg = cv2.bitwise_and(glass_img,glass_img,mask=glass_img_mask1)
                dst = cv2.add(img1_bg,img2_fg)

                img[eye_left.y -bias:eye_left.y + height-bias , eye_left.x-30:eye_left.x + width-30] = dst

        cv2.imshow("Video",img)
        cv2.imwrite("test_with_glass.jpg",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=="__main__":
    add_glass()