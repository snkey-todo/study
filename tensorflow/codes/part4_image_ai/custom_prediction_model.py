from imageai.Prediction.Custom import ModelTraining

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()

# 数据集
model_trainer.setDataDirectory("/Users/zhusheng/WorkSpace/Tmp/dataset/idenprof")

# 开始训练模型
"""
num_objects:
num_experiments:迭代次数
batch_size：批处理大小
show_network_summary：在控制台输出神经网络概要
"""
model_trainer.trainModel(num_objects=10,
                         num_experiments=100
                         ,enhance_data=True,
                         batch_size=32,
                         show_network_summary=True)
