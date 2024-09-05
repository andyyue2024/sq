import time

import numpy as np
from gm.api import *
from sklearn import svm

from sq.trainers import Trainer
from sq.utils import print_log


class SVMTrainer(Trainer):
    """
    SVMTrainer
    """

    def train(self, *args, **kwargs):
        print_log("SVMTrainer train...")
        return super().train(*args, **kwargs)

    def do_training(self, *args, **kwargs):
        start_time = time.time()
        # 用于记录工作日
        # 获取目标股票的daily历史行情
        recent_data = history(self.target, frequency='1d', start_time=self.start_date, end_time=self.end_date,
                              fill_missing='last', df=True)
        days_value = recent_data['bob'].values
        days_close = recent_data['close'].values
        days = []
        # 获取行情日期列表
        print_log('prepare data to train SVM')
        for i in range(len(days_value)):
            days.append(str(days_value[i])[0:10])
        x_all = []
        y_all = []
        for index in range(15, (len(days) - 5)):
            # 计算三星期共15个交易日相关数据
            # start_day = days[index - 15]
            # end_day = days[index]
            # data = history(context.symbol, frequency='1d', start_time=start_day, end_time=end_day,
            # fill_missing='last', df=True)
            data = recent_data.iloc[index - 15: index, :]
            close = data['close'].values
            max_x = data['high'].values
            min_n = data['low'].values
            amount = data['amount'].values
            volume = []
            for i in range(len(close)):
                volume_temp = amount[i] / close[i]
                volume.append(volume_temp)
            close_mean = close[-1] / np.mean(close)  # 收盘价/均值
            volume_mean = volume[-1] / np.mean(volume)  # 现量/均量
            max_mean = max_x[-1] / np.mean(max_x)  # 最高价/均价
            min_mean = min_n[-1] / np.mean(min_n)  # 最低价/均价
            vol = volume[-1]  # 现量
            return_now = close[-1] / close[0]  # 区间收益率
            std = np.std(np.array(close), axis=0)  # 区间标准差
            # 将计算出的指标添加到训练集X
            # features用于存放因子
            features = [close_mean, volume_mean, max_mean, min_mean, vol, return_now, std]
            x_all.append(features)
        # 准备算法需要用到的数据
        for i in range(len(days_close) - 20):
            if days_close[i + 20] > days_close[i + 15]:
                label = 1
            else:
                label = 0
            y_all.append(label)
        x_train = x_all[: -1]
        y_train = y_all[: -1]
        # 训练SVM
        self.clf = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True,
                           probability=False, tol=0.001, cache_size=200, verbose=False, max_iter=-1,
                           decision_function_shape='ovr', random_state=None)
        self.clf.fit(x_train, y_train)
        print_log(f"Training finished!, time elapsed: {time.time() - start_time} seconds")

    def do_predicting(self, *args, **kwargs):
        # 获取预测用的历史数据
        data = history_n(symbol=self.target, frequency='1d', end_time=self.now, count=15,
                         fill_missing='last', df=True)
        close = data['close'].values
        train_max_x = data['high'].values
        train_min_n = data['low'].values
        train_amount = data['amount'].values
        volume = []
        for i in range(len(close)):
            volume_temp = train_amount[i] / close[i]
            volume.append(volume_temp)
        close_mean = close[-1] / np.mean(close)
        volume_mean = volume[-1] / np.mean(volume)
        max_mean = train_max_x[-1] / np.mean(train_max_x)
        min_mean = train_min_n[-1] / np.mean(train_min_n)
        vol = volume[-1]
        return_now = close[-1] / close[0]
        std = np.std(np.array(close), axis=0)
        # 得到本次输入模型的因子
        features = [close_mean, volume_mean, max_mean, min_mean, vol, return_now, std]
        features = np.array(features).reshape(1, -1)
        self.prediction = self.clf.predict(features)[0]

