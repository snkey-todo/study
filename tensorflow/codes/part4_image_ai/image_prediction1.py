from imageai.Prediction import ImagePrediction
import os

# 获取当前python文件所在的路径
execution_path = os.getcwd()

# 创建预测对象
prediction = ImagePrediction()
# 指定图片预测算法模型
prediction.setModelTypeAsSqueezeNet()
# 算法模型所在的路径
prediction.setModelPath("/Users/zhusheng/WorkSpace/yingcloudDev/code/squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
# 加载模型
prediction.loadModel()


# 开始预测
prediction_results, prediction_probabilities = prediction.predictImage("image/cat.png", result_count=5)

for eachPrediction, eachProbability in zip(prediction_results,prediction_probabilities):
    print("eachPrediction-->", eachPrediction)
    print("eachProbability-->", eachProbability)

"""
SqueezeNet模型

eachPrediction--> tabby
eachProbability--> 47.68999516963959
eachPrediction--> Egyptian_cat
eachProbability--> 45.005470514297485
eachPrediction--> tiger_cat
eachProbability--> 6.412443518638611
eachPrediction--> lynx
eachProbability--> 0.8891490288078785
eachPrediction--> tiger
eachProbability--> 0.001844802318373695
"""

