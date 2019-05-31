from imageai.Prediction import ImagePrediction
import os
execution_path = os.getcwd()

# 创建预测对象
prediction = ImagePrediction()

# 指定图片预测算法模型
prediction.setModelTypeAsInceptionV3()
# 算法模型所在的路径
prediction.setModelPath("/Users/zhusheng/WorkSpace/Tmp/dataset/models/inception_v3_weights_tf_dim_ordering_tf_kernels.h5")

# 加载模型
prediction.loadModel()


# 开始预测
prediction_results, prediction_probabilities = prediction.predictImage("image/cat.png", result_count=5)

for eachPrediction, eachProbability in zip(prediction_results,prediction_probabilities):
    print("eachPrediction-->", eachPrediction)
    print("eachProbability-->", eachProbability)

"""
InceptionV3模型

eachPrediction--> tabby
eachProbability--> 97.53087162971497
eachPrediction--> tiger_cat
eachProbability--> 2.4227475747466087
eachPrediction--> Egyptian_cat
eachProbability--> 0.04109963483642787
eachPrediction--> lynx
eachProbability--> 0.0038046291592763737
eachPrediction--> Persian_cat
eachProbability--> 0.0007754750185995363
"""