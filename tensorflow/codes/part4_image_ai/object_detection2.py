from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

# 指定模型
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/yolo.h5")
detector.loadModel()

# 开始预测
# extract_detected_objects, 将检测的结果拆分成单独的图片
detections, obj_path = detector.detectObjectsFromImage(input_image="image/obj_input2.jpg", output_image_path="image/obj_output2.jpg", minimum_percentage_probability=30, extract_detected_objects=True)
print("detections:",detections)
print("obj_path", obj_path)

# 打印预测结果
for eachObj, eachPath in zip(detections, obj_path):
    print(eachObj["name"], ":", eachObj["percentage_probability"], ":", eachObj["box_points"])
    print("Object's image saved in " + eachPath)
    print("------------------------")