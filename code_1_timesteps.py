from keras.layers.core import Dense #全连接层
from keras.layers.recurrent import LSTM #LSTM模型
from keras.layers.core import Activation,Dropout #激活函数，随机置零
from keras.models import Sequential,load_model #序列模型，加载模型
from sklearn.metrics import mean_squared_error #评价指标
import panda as pd #pandas方便读取和处理，但数据大之后速度较慢
from matplotlib import pyplot as plt #最基本的绘图方法
import numpy as np

#定义网络基本参数
UNITS = 50 #LSTM内神经元数量
EPOCHS = 10 #批次数
BATCH_SIZE = 64 #单次输入例数

#回归模型构建，单层LSTM，输出维度为1
def creat_model(units, trainX, train_Y):
    model.add(LSTM(units,input_shape=(train_X.shape[1], train_X.shape[2]),return_sequences=False))
    model.add(Dense(1)) #全连接层，神经元个数应与输出维度相同
    model.add(Activation("tanh")) #激活函数
    model.compile(loss='mse', optimizer='adam') #编译模型
    return model

#读取数据
data = pd.read_excel('../data/data2.xlsx', sheet_name=r'汇总数据2', usecols=range(1, 9)).values

#数据归一化设置
scaler = MinMaxScaler(feature_range=(0, 1), copy=False)

#数据划分
Sp = int(0.8 * len(data)) #设置数据划分点
X = data[:, :-1]
y = data[:, -1]
X = scaler.fit_transform(X) #仅对X作归一化操作,全部归一化则需要逆归一化操作inverse_transform
train_X, test_X = X[:Sp, :-1], X[Sp:, :-1] #前7维为X，后1维为Y
train_y, test_y = y[:Sp], y[Sp:] #前7维为X，后1维为Y

#模型加载（如果有现存模型）
# model = load_model('1-timestep_easy_lstm.h5')

#模型训练
model = creat_model(units=50, trainX=train_X, train_Y=train_y)
model.fit(train_X, train_y, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1) #verbose为0不显示过程，默认1显示过程，2间隔一段时间显示过程

#模型保存
model.save('1-timestep_easy_lstm.h5')

#模型预测
result = model.predict(test_X)

#测试曲线绘制
plt.rcParams['font.sans-serif'] = ['SimHei'] #设置字体才可写中文，否则乱码
plt.rcParams['axes.unicode_minus'] = False #
plt.plot(result, color='red')
plt.plot(test_y, color='blue')
plt.title(r'红色预测,蓝色真实')
plt.show()
