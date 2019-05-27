from imageai.Prediction import ImagePrediction
import os

# 获取当前python文件所在的路径
execution_path = os.getcwd()

multiple_prediction = ImagePrediction()
multiple_prediction.setModelTypeAsDenseNet()
multiple_prediction.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/DenseNet-BC-121-32.h5")
multiple_prediction.loadModel()


all_image_array = []

all_files = os.listdir("/Users/zhusheng/WorkSpace/Tmp/dataset/mycat/")
for each_file in all_files:
    if(each_file.endswith(".jpg") or each_file.endswith(".png")):
        file_path = os.path.join("/Users/zhusheng/WorkSpace/Tmp/dataset/mycat/", each_file)
        all_image_array.append(file_path)
print(all_image_array)


# 开始预测，一次预测一个图片集合
results_array = multiple_prediction.predictMultipleImages(all_image_array, result_count_per_image=5)

# 打印预测结果
for each_result in results_array:
    predictions, percentage_probabilities = each_result["predictions"], each_result["percentage_probabilities"]
    for index in range(len(predictions)):
        print(predictions[index] , " : ", percentage_probabilities[index])
    print("-----------------------")