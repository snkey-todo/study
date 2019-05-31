from imageai.Prediction import ImagePrediction
import os
execution_path = os.getcwd()

# 创建预测对象
prediction = ImagePrediction()

# 指定图片预测算法模型
prediction.setModelTypeAsDenseNet()
# 算法模型所在的路径
prediction.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/DenseNet-BC-121-32.h5")

# 加载模型
prediction.loadModel()


# 开始预测
prediction_results, prediction_probabilities = prediction.predictImage("image/cat.png", result_count=5)

for eachPrediction, eachProbability in zip(prediction_results,prediction_probabilities):
    print("eachPrediction-->", eachPrediction)
    print("eachProbability-->", eachProbability)

"""
DenseNet121模型

eachPrediction--> Egyptian_cat
eachProbability--> 67.63618588447571
eachPrediction--> tabby
eachProbability--> 26.069360971450806
eachPrediction--> tiger_cat
eachProbability--> 5.755872279405594
eachPrediction--> lynx
eachProbability--> 0.12627518735826015
eachPrediction--> tiger
eachProbability--> 0.10607598815113306
"""