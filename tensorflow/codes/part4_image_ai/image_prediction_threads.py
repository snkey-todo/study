from imageai.Prediction import ImagePrediction
import os
import threading
execution_paht = os.getcwd()

thread_prediction = ImagePrediction()
thread_prediction.setModelTypeAsResNet()
thread_prediction.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/resnet50_weights_tf_dim_ordering_tf_kernels.h5")

all_image_array = []

all_files = os.listdir("/Users/zhusheng/WorkSpace/Tmp/dataset/mycat/")
for each_file in all_files:
    if(each_file.endswith(".jpg") or each_file.endswith(".png")):
        file_path = os.path.join("/Users/zhusheng/WorkSpace/Tmp/dataset/mycat/", each_file)
        all_image_array.append(file_path)
print(all_image_array)


class PredictionThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        thread_prediction.loadModel()

        # 一张一张的预测
        for eachPicture in all_image_array:
            print(eachPicture)
            predictions, probabilities = thread_prediction.predictImage(eachPicture, result_count=1)

            # 打印预测结果
            for prediction, percentage_probability in zip(predictions, probabilities):
                print(prediction, " : ", percentage_probability)

# 开启线程进行预测
predictionThread = PredictionThread()
predictionThread.start()
