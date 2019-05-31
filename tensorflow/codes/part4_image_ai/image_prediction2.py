from imageai.Prediction import ImagePrediction
import os
execution_path = os.getcwd()

# 创建预测对象
prediction = ImagePrediction()

# 指定图片预测算法模型
prediction.setModelTypeAsResNet()
# 算法模型所在的路径
prediction.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")

# 加载模型
prediction.loadModel()


# 开始预测
prediction_results, prediction_probabilities = prediction.predictImage("image/cat.png", result_count=5)

for eachPrediction, eachProbability in zip(prediction_results,prediction_probabilities):
    print("eachPrediction-->", eachPrediction)
    print("eachProbability-->", eachProbability)

"""
ResNet50模型

eachPrediction--> Egyptian_cat
eachProbability--> 54.8492431640625
eachPrediction--> tabby
eachProbability--> 35.49413979053497
eachPrediction--> tiger_cat
eachProbability--> 5.88301382958889
eachPrediction--> lynx
eachProbability--> 3.1602896749973297
eachPrediction--> snow_leopard
eachProbability--> 0.23085731081664562
"""