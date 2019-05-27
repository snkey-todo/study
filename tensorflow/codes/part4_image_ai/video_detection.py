from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/resnet50_coco_best_v2.0.1.h5")
detector.loadModel()

# 开始预测
video_path = detector.detectObjectsFromVideo(input_file_path="video/traffic.mp4",
                                output_file_path="video/traffic_detected",
                                frames_per_second=20,
                                log_progress=True)

# 打印预测结果
print(video_path)