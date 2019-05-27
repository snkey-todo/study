from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

def forFrame(frame_number, output_array, output_count):
    print("FOR FRAME " , frame_number)
    print("Output for each object : ", output_array)
    print("Output count for unique objects : ", output_count)
    print("------------END OF A FRAME --------------")

def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    print("SECOND : ", second_number)
    print("Array for the outputs of each frame ", output_arrays)
    print("Array for output count for unique objects in each frame : ", count_arrays)
    print("Output average count for unique objects in the last second: ", average_output_count)
    print("------------END OF A SECOND --------------")

def forMinute(minute_number, output_arrays, count_arrays, average_output_count):
    print("MINUTE : ", minute_number)
    print("Array for the outputs of each frame ", output_arrays)
    print("Array for output count for unique objects in each frame : ", count_arrays)
    print("Output average count for unique objects in the last minute: ", average_output_count)
    print("------------END OF A MINUTE --------------")


detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/yolo.h5")
detector.loadModel()

# 自定义预测对象
custom_objects = detector.CustomObjects(person=True, bicycle=True, motorcycle=True)

# 开始预测
video_path = detector.detectCustomObjectsFromVideo(custom_objects = custom_objects,
                                      input_file_path="video/traffic.mp4",
                                      output_file_path="video/traffic_detedted2",
                                      frames_per_second=10,
                                                   per_second_function=forSeconds,
                                                   per_frame_function=forFrame,
                                                   per_minute_function=forMinute,
                                                   minimum_percentage_probability=30
                                                   )

print(video_path)