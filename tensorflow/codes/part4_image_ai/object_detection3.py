from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

# 指定模型
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/yolo.h5")
detector.loadModel()

"""
默认ObjectDetection会识别所以的物体，但是我们是可以指定只识别什么物体
"""

# 自定义只识别摩托车和汽车
custom_objects = detector.CustomObjects(car=True, motorcycle=True)

# 开始预测
detections = detector.detectCustomObjectsFromImage(custom_objects = custom_objects,
                                      input_image="image/obj_input2.jpg",
                                      output_image_path="image/obj_output3.jpg",
                                      minimum_percentage_probability=30)


for eachObj in detections:
    print(eachObj["name"], ":", eachObj["percentage_probability"], ":", eachObj["box_points"])
    print("-----------------")