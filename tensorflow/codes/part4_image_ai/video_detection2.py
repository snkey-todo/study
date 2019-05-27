from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/resnet50_coco_best_v2.0.1.h5")
detector.loadModel()

# 自定义预测对象
custom_objects = detector.CustomObjects(person=True, bicycle=True, motorcycle=True)

# 开始预测
video_path = detector.detectCustomObjectsFromVideo(custom_objects = custom_objects,
                                      input_file_path="video/traffic.mp4",
                                      output_file_path="video/custom_detected",
                                      frames_per_second=20,
                                      log_progress=True)

print(video_path)