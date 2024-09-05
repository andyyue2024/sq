import math
import time
from datetime import datetime, date
import numpy as np
import pandas as pd
from gm.api import *
from h2o import save_model
from h2o.estimators import H2OGradientBoostingEstimator
from h2o.grid import H2OGridSearch
from sklearn import svm
from sq.gm import get_time_Ymd
from sq.trainers import Trainer
from sq.utils import print_log
import h2o
from h2o.automl import H2OAutoML
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.mixture import GaussianMixture
from sklearn.datasets import make_classification


class ManualTrainer(Trainer):
    """
    ManualTrainer use h2o or svm to train
    """

    FILE_PATH_FLAG_SH = "./data/flag_sh.xlsx"
    FILE_PATH_TRAIN_DATA_WITH_NA = "./data/train_data_with_na.xlsx"
    FILE_PATH_TRAIN_DATA = "./data/train_data.xlsx"
    FOLD_PATH = "./data"
    FILE_NAME_PREDICTION_DAT = "prediction_data.xlsx"
    FILE_PATH_PREDICTION_DATA = "./data/prediction_data.xlsx"
    MODEL_PATH = "./data/models"
    MODEL_NAME_LIST = [
        "Grid_GBM_py_3_sid_ad52_model_python_1724993029821_1_model_57",  # 0, ratios=[.8], auc: 0.95003,
        "StackedEnsemble_AllModels_1_AutoML_3_20240831_112417",  # 1, ratios=[.5], auc: 0.941627, sq_test3_1_h2o_7.log
        "StackedEnsemble_AllModels_1_AutoML_1_20240830_221403",  # 2, ratios=[.8], auc: 0.96869, sq_test3_1_h2o_2.log
        "StackedEnsemble_AllModels_1_AutoML_1_20240830_223216",  # 3, ratios=[.8], auc: 0.968709, sq_test3_1_h2o_3.log
        "StackedEnsemble_BestOfFamily_1_AutoML_1_20240830_224552",  # 4, ratios=[.9], auc: 0.975541, sq_test3_1_h2o_4
        "StackedEnsemble_AllModels_1_AutoML_1_20240830_230008",  # 5, ratios=[.95], auc: 0.976119, sq_test3_1_h2o_5.log
        "StackedEnsemble_BestOfFamily_1_AutoML_2_20240831_100856",  # 6, ratios=[.98], auc: 0.979502, sq_test3_1_h2o_6
        "StackedEnsemble_BestOfFamily_1_AutoML_1_20240831_155428",  # 7, ratios=2800:1038, auc: 0.982, sq_test3_1_h2o_8
    ]
    WINDOW_LIST = [3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    def __init__(self, target: str = None, start_date: str | datetime | date = "2004-08-01",
                 end_date: str | datetime | date = "2024-08-01", now: str | datetime | date = None,
                 model_index: int = 0, fast_prediction=False):
        super().__init__(target, start_date, end_date, now)
        if model_index < 0 or model_index >= len(ManualTrainer.MODEL_NAME_LIST):
            model_index = 0
        self.model_index = model_index
        self.best_model_name = ManualTrainer.MODEL_NAME_LIST[model_index]
        self.fast_prediction = fast_prediction
        self.date_prediction_dict = {}

    def train(self, *args, **kwargs):
        print_log("ManualTrainer train...")
        print_log("Model name: ", self.best_model_name)
        return super().train(*args, **kwargs)

    def prepare_data(self, file_name: str = FILE_PATH_TRAIN_DATA):
        """
        - get all date list and store to excel, and then make flag manually
        - get daily history data of target
        - calculate ma of different windows
        - store all data to excel for next step to train
        """
        start_time = time.time()
        # get all date list and store to excel
        # context.all_date.append(get_time_Ymd(context.now))
        # df = pd.DataFrame()
        # df["eob"] = context.all_date
        # df.to_excel(ManualTrainer.FILE_PATH_FLAG_SH, index=False)

        # get daily history data of target
        all_data = history(self.target, frequency='1d', start_time=self.start_date, end_time=self.end_date,
                           fill_missing='last', df=True)
        # days_close = all_data['close'].values
        # field_keys = ['eob', 'close']
        # ret_tmp_part = all_data[field_keys]
        df = pd.DataFrame()
        df['eob'] = all_data['eob'].apply(lambda x: get_time_Ymd(x))
        df['close'] = all_data['close']
        for window in ManualTrainer.WINDOW_LIST:
            field = "ma" + str(window)
            df[field] = all_data['close'].rolling(window=window).mean()
        # load prepared flag file
        df_flag = pd.read_excel(ManualTrainer.FILE_PATH_FLAG_SH)
        df_flag = df_flag[['eob', 'hold']]
        #  merge df
        trained_df = pd.merge(df, df_flag, on='eob', how='inner')
        # print(trained_df)
        trained_df.to_excel(ManualTrainer.FILE_PATH_TRAIN_DATA_WITH_NA, index=False)
        trained_df = trained_df.dropna()
        trained_df.to_excel(file_name, index=False)
        print_log(f"prepare data finished!, time elapsed: {time.time() - start_time} seconds")
        # prepare data finished!, time elapsed: 4.380619049072266 seconds

    def do_training_by_automl(self):
        """
        train model from ManualTrainer.FILE_PATH_TRAIN_DATA excel by H2OAutoML
        and save the model to dir ./data/model/
        :return:
        """
        start_time = time.time()
        # initiate H2O
        h2o.init()
        # load dataset
        trained_df = pd.read_excel(ManualTrainer.FILE_PATH_TRAIN_DATA)
        # response column: y
        response_column = "hold"
        trained_df[response_column] = trained_df[response_column].astype('category')
        data = h2o.H2OFrame(trained_df)
        data[response_column] = data[response_column].asfactor()
        print("response column levels: ", data[response_column].levels())  # [['0', '1']]
        # print(data[response_column].describe())
        # predictor columns: X
        predictor_columns = data.columns
        predictor_columns.remove(response_column)
        predictor_columns.remove("eob")
        # predictor_columns.remove("close")
        # split to train dataset and test dataset
        train, test = data.split_frame(ratios=[.8], seed=12345)
        # train = data.head(2800)
        # test = data.tail(1038)
        print("train shape:", train.shape)  # train shape: (3089, 24)
        print("test shape:", test.shape)  # test shape: (749, 24)
        # start AutoML
        aml = H2OAutoML(max_models=20, seed=1)
        aml.train(x=predictor_columns, y=response_column, training_frame=train)
        # 查看模型性能
        lb = aml.leaderboard
        print("*" * 20)
        print("leaderboard: ", lb)
        # 输出前5个模型的性能
        print("*" * 20)
        print("leaderboard.head: ", lb.head(rows=5))
        # 查看最佳模型
        best_model = aml.leader
        best_model_id = best_model.model_id
        print("*" * 20)
        print(f"Best Model: {best_model}")
        predictions = best_model.predict(test)
        h2o.save_model(best_model, path=ManualTrainer.MODEL_PATH)
        print("*" * 20)
        print("predictions.head: ", predictions.head())
        print("*" * 20)
        metrics = best_model.model_performance(test)
        print(f"metrics: {metrics}")
        accuracy = metrics.accuracy()
        print("*" * 20)
        print(f"Accuracy: {accuracy}")
        self.clf = best_model
        # shutdown H2O
        # h2o.shutdown()
        print_log(f"getting best model finished!, time elapsed: {time.time() - start_time} seconds")
        #     getting best model finished!, time elapsed: 640.3788826465607 seconds
        #     getting best model finished!, time elapsed: 700.7501661777496 seconds
        #     getting best model finished!, time elapsed: 816.4491987228394 seconds
        #     getting best model finished!, time elapsed: 1310.4281556606293 seconds
        #     getting best model finished!, time elapsed: 614.0460500717163 seconds
        #     getting best model finished!, time elapsed: 640.4960896968842 seconds

    def do_training_by_gbm(self):
        """
        train model from ManualTrainer.FILE_PATH_TRAIN_DATA excel by H2OGridSearch and H2OGradientBoostingEstimator
        and save the model to dir ./data/model/
        """
        start_time = time.time()
        # 初始化H2O
        h2o.init()
        # 加载数据集
        trained_df = pd.read_excel(ManualTrainer.FILE_PATH_TRAIN_DATA)
        # 指定响应列（目标变量）
        response_column = "hold"
        trained_df[response_column] = trained_df[response_column].astype('category')
        data = h2o.H2OFrame(trained_df)
        data[response_column] = data[response_column].asfactor()
        # 输出转换后的数据
        # print(data[response_column].levels())  # [['0', '1']]
        # print(data[response_column].describe())
        # 指定特征列
        predictor_columns = data.columns
        predictor_columns.remove(response_column)
        predictor_columns.remove("eob")
        # predictor_columns.remove("close")
        # 划分训练集和测试集
        train, test = data.split_frame(ratios=[.8], seed=1234)
        print("train shape:", train.shape)  # train shape: (3089, 24)
        print("test shape:", test.shape)  # test shape: (749, 24)
        # 创建一个GBM模型
        gbm = H2OGradientBoostingEstimator()
        # 定义参数网格
        param_grid = {
            "ntrees": [10, 50, 100, 200],
            "max_depth": [1, 2, 3, 4, 5],
            "learn_rate": [0.01, 0.1, 0.5]
        }

        # 创建一个Grid Search对象
        grid_search = H2OGridSearch(gbm, param_grid)
        # 训练模型
        grid_search.train(x=predictor_columns, y=response_column, training_frame=train)
        # 查看结果
        print("*" * 20)
        print("grid_search.show:")
        grid_search.show()
        # 获取最佳模型
        best_model = grid_search.get_grid(sort_by="accuracy", decreasing=True)[0]
        print("*" * 20)
        print(f"Best Model: {best_model}")
        predictions = best_model.predict(test)
        h2o.save_model(best_model, path=ManualTrainer.MODEL_PATH)
        print("*" * 20)
        print("predictions.head: ", predictions.head())
        print("*" * 20)
        metrics = best_model.model_performance(test)
        print(f"metrics: {metrics}")
        accuracy = metrics.accuracy()
        print(f"Accuracy: {accuracy}")
        self.clf = best_model
        # shutdown H2O
        # h2o.shutdown()
        print_log(f"getting best model finished!, time elapsed: {time.time() - start_time} seconds")
        #     getting best model finished!, time elapsed: 69.20550513267517 seconds

    def load_model_from_automl_and_test(self, file_name: str = FILE_PATH_TRAIN_DATA):
        """
        load a saved H2O model from disk
        and test
        :return:
        """
        h2o.init()
        # load dataset
        trained_df = pd.read_excel(file_name)
        data = h2o.H2OFrame(trained_df)
        train, test = data.split_frame(ratios=[.8], seed=1234)
        # test = data.tail(1038)
        best_model = h2o.load_model(ManualTrainer.MODEL_PATH + "/" + self.best_model_name)
        predictions = best_model.predict(test)
        print("*" * 20)
        print("predictions.head: ", predictions.head())
        metrics = best_model.model_performance(test)
        print("*" * 20)
        print(f"metrics: {metrics}")
        accuracy = metrics.accuracy()
        print("*" * 20)
        print(f"Accuracy: {accuracy}")
        self.clf = best_model
        # shutdown H2O
        # h2o.shutdown()

    @staticmethod
    def do_training_by_svm():
        start_time = time.time()
        # # 创建数据集
        # X, y = make_classification(n_samples=100, n_features=20, random_state=1)
        # # 划分训练集和测试集
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

        trained_df = pd.read_excel(ManualTrainer.FILE_PATH_TRAIN_DATA)
        # 假设目标列是名为'target_column'的列
        X = trained_df.drop(["eob", "hold"], axis=1)  # 选择除了目标列之外的所有列作为特征
        y = trained_df['hold']  # 选择目标列作为目标变量
        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # 输出结果
        print("X_train shape:", X_train.shape)  # X_train shape: (3070, 22)
        print("y_train shape:", y_train.shape)  # y_train shape: (3070,)
        print("X_test shape:", X_test.shape)  # X_test shape: (768, 22)
        print("y_test shape:", y_test.shape)  # y_test shape: (768,)
        # 网格搜索（Grid Search）是一种用于优化模型参数的穷举搜索方法。
        param_grid = {
            'C': [0.1, 1, 10, 100],  # 正则化参数
            'gamma': [1, 0.1, 0.01, 0.001],  # RBF核的γ参数
            'degree': [1, 2, 3, 4, 5],  # 设置度数范围
            'kernel': ['linear', 'poly', 'rbf', 'sigmoid']
            # 核函数类型 kernel : {'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'}
        }

        # 设置交叉验证的折数
        cv = 5
        # 实例化SVM模型
        svc = SVC()
        # 实例化网格搜索对象
        grid_search = GridSearchCV(svc, param_grid, cv=cv, scoring='accuracy')
        # 执行网格搜索
        grid_search.fit(X_train, y_train)
        # 最佳参数
        best_params = grid_search.best_params_
        # 最佳分数
        best_score = grid_search.best_score_
        # 最佳估计器
        best_estimator = grid_search.best_estimator_
        print("best_params:", best_params, ", best_score:", best_score, ", best_estimator:", best_estimator)
        # 使用最佳参数训练模型
        final_model = SVC(**best_params)
        final_model.fit(X_train, y_train)
        # # 训练SVM
        # self.clf = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True,
        #                    probability=False, tol=0.001, cache_size=200, verbose=False, max_iter=-1,
        #                    decision_function_shape='ovr', random_state=None)
        # self.clf.fit(x_train, y_train)
        print_log(f"getting best model finished!, time elapsed: {time.time() - start_time} seconds")

    def load_model_and_prepare_date_prediction_dict(self, file_name: str = FILE_PATH_PREDICTION_DATA):
        """
        - get daily history data of target between start_date and end_date
        - calculate ma of different windows
        - load a saved H2O model from disk
        - store all data to excel
        - prepare date-prediction dict
        """
        # get all date list and store to excel
        # context.all_date.append(get_time_Ymd(context.now))
        # df = pd.DataFrame()
        # df["eob"] = context.all_date
        # df.to_excel(ManualTrainer.FILE_PATH_FLAG_SH, index=False)

        # get daily history data of target
        all_data = history(self.target, frequency='1d', start_time=self.start_date, end_time=self.end_date,
                           fill_missing='last', df=True)
        # days_close = all_data['close'].values
        # field_keys = ['eob', 'close']
        # ret_tmp_part = all_data[field_keys]
        df = pd.DataFrame()
        df['eob'] = all_data['eob'].apply(lambda x: get_time_Ymd(x))
        df['close'] = all_data['close']
        for window in ManualTrainer.WINDOW_LIST:
            field = "ma" + str(window)
            df[field] = all_data['close'].rolling(window=window).mean()
        df_without_na = df.dropna()
        df_reset = df_without_na.reset_index(drop=True)
        h2o.init()
        test = h2o.H2OFrame(df_reset)
        best_model = h2o.load_model(ManualTrainer.MODEL_PATH + "/" + self.best_model_name)
        predictions = best_model.predict(test)
        print("*" * 20)
        print("predictions.head: ", predictions.head())
        # metrics = best_model.model_performance(test)
        # print("*" * 20)
        # print(f"metrics: {metrics}")
        # accuracy = metrics.accuracy()
        # print("*" * 20)
        # print(f"Accuracy: {accuracy}")
        df_prediction = pd.DataFrame(predictions.as_data_frame())
        df_reset['predict'] = df_prediction["predict"]
        df_reset.to_excel(file_name, index=False)
        # using zip() to make key-value，and than transfer to dict
        self.date_prediction_dict = dict(zip(df_reset['eob'], df_prediction["predict"]))
        # self.date_prediction_dict = df.set_index('eob')['predict'].to_dict()

    def do_predicting_fast(self, *args, **kwargs):
        """
        get prediction from date_prediction_dict of memory
        :param args:
        :param kwargs:
        :return:
        """
        if kwargs:
            self._now = kwargs.get("now")
        else:
            self.prediction = None
            return
        ret = self.date_prediction_dict.get(get_time_Ymd(self._now))
        if math.isnan(ret) or ret is None:
            self.prediction = None
            return
        self.prediction = int(ret)

    def do_training(self, *args, **kwargs):
        # self.prepare_data()
        # self.do_training_by_automl()
        # self.do_training_by_gbm()
        # self.do_training_by_svm()

        start_time = time.time()
        if self.fast_prediction:
            file_name = (ManualTrainer.FOLD_PATH + f"/model_{self.model_index}_"
                         + ManualTrainer.FILE_NAME_PREDICTION_DAT)
            self.load_model_and_prepare_date_prediction_dict(file_name)
        else:
            self.load_model_from_automl_and_test()
        print_log(f"Training finished!, time elapsed: {time.time() - start_time} seconds")

    def do_predicting(self, *args, **kwargs):
        if self.fast_prediction:
            self.do_predicting_fast(*args, **kwargs)
            return

        if kwargs:
            self._now = kwargs.get("now")
        else:
            self.prediction = None
            return
        all_data = history_n(symbol=self.target, frequency='1d', end_time=self.now, count=100,
                             fill_missing='last', df=True)
        df = pd.DataFrame()
        # df['eob'] = all_data['eob'].apply(lambda x: get_time_Ymd(x))
        df['close'] = all_data['close']
        for window in ManualTrainer.WINDOW_LIST:
            field = "ma" + str(window)
            df[field] = all_data['close'].rolling(window=window).mean()
        data = h2o.H2OFrame(df.dropna())
        if data.nrows == 0:
            self.prediction = None
            return
        # predict
        if self.clf is None:
            raise ValueError("self.clf is None.")
        predictions = self.clf.predict(data)
        # print_log("predictions.head: ", predictions.head())
        self.prediction = int(predictions[0, 0])
