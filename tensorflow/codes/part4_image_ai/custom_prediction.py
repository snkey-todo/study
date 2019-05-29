from imageai.Prediction.Custom import CustomImagePrediction
import os

execution_path = os.getcwd()

# 配置自定义模型
prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("")
prediction.setJsonPath("")
prediction.loadModel(num_objects=10)

# 预测
predictions, probabilities = prediction.predictImage("", result_count=5)

# 打印预测结果
for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction + " : " + eachProbability)