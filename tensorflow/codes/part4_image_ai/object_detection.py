from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

# 指定预测模型
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/resnet50_coco_best_v2.0.1.h5")
detector.loadModel()


# 开始预测
detections = detector.detectObjectsFromImage(input_image="image/obj_input.jpg", output_image_path="image/obj_output.jpg", minimum_percentage_probability=30)

# 打印预测结果
for eachObj in detections:
    print(eachObj["name"], ":", eachObj["percentage_probability"], ":", eachObj["box_points"])
    print("----------------------")
