# tensorflow设置日志打印级别

```python
import os

 # 默认的显示等级，显示所有信息
os.environ["TF_CPP_MIN_LOG_LEVEL"]='1'

# 只显示 warning 和 Error  
os.environ["TF_CPP_MIN_LOG_LEVEL"]='2'

# 只显示 Error
os.environ["TF_CPP_MIN_LOG_LEVEL"]='3'
```
