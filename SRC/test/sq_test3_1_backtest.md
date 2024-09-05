# backtest for models
## 1.best model 
> model index 6: StackedEnsemble_BestOfFamily_1_AutoML_2_20240831_100856
> 
> For SHSE.000922, by day, 20081101~20240830, pnl_ratio 3771226.98%.

vs 

> origin_flag_data
>
> For SHSE.000922, by day, 20081101~20240830, pnl_ratio 4358978.06%.
> 
> For SHSE.000922, by day, 20040801~20240801, pnl_ratio 5160317.29%.
> 
## 2.backtest result detail as fellow:
For SHSE.000922, by day, 20081101~20240830, model_index = 0~7
```python
    # 1.For SHSE.000922, by month, 20220801~20240831, pnl_ratio  -7.20%.
    # every executing spend about 24.7 seconds. And during period, it spends about 1248 seconds.
    # model index 1: StackedEnsemble_AllModels_1_AutoML_3_20240831_112417
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': -0.07217770024414062,
    #            'pnl_ratio_annual': -0.034618739276098986, 'sharp_ratio': -0.37101658976479046,
    #            'max_drawdown': 0.13254109494017283, 'open_count': 6, 'close_count': 6, 'win_count': 3,
    #            'lose_count': 3, 'win_ratio': 0.5, 'calmar_ratio': -0.26119249498976443}
    # probable reason is date_rule by month rather then by day.

    # 2.For SHSE.000922, by month, 20081101~20240830, pnl_ratio  481.43%.
    # every executing spend about 24.7 seconds. And during period, it spends about 4757 seconds.
    # model index 1: StackedEnsemble_AllModels_1_AutoML_3_20240831_112417
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 4.81436749095459,
    #            'pnl_ratio_annual': 0.30402147650491784, 'sharp_ratio': 0.44046116760162357,
    #            'max_drawdown': 0.38304976688042175, 'open_count': 44, 'close_count': 44, 'win_count': 30,
    #            'lose_count': 14, 'win_ratio': 0.6818181818181818, 'calmar_ratio': 0.7936866245367681, 'risk_ratio': 0.0}
    # probable reason is date_rule by month rather then by day.

    # 3.For SHSE.000922, by week, 20240101~20240830, pnl_ratio  4.40%.
    # every executing spend about 24.7 seconds. And during period, it spends about 903 seconds.
    # model: StackedEnsemble_AllModels_1_AutoML_3_20240831_112417
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 0.0441538931640625,
    #            'pnl_ratio_annual': 0.06659574795406122, 'sharp_ratio': 0.8182839447739283,
    #            'max_drawdown': 0.037555279040363265, 'open_count': 6, 'close_count': 6, 'win_count': 4,
    #            'lose_count': 2, 'win_ratio': 0.667, 'calmar_ratio': 1.7732726172127797, 'risk_ratio': 0.0}
    # probable reason is date_rule by week rather then by day.

    # 3.For SHSE.000922, by day, 20220801~20240831, pnl_ratio 118.9%.
    # every executing spend about 0.36 seconds. And during period, it spends about 242 seconds.
    # model: StackedEnsemble_AllModels_1_AutoML_1_20240830_221403
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 1.1890411473632811,
    #            'pnl_ratio_annual': 0.5703022585907984, 'sharp_ratio': 4.176448901653619,
    #            'max_drawdown': 0.02663430283051175, 'open_count': 26, 'close_count': 26, 'win_count': 25,
    #            'lose_count': 1, 'win_ratio': 0.9615384615384616, 'calmar_ratio': 21.412321629739488,
    #            'risk_ratio': 0.0}


    # 10.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 2381784.08 %.
    # every executing spend about 0.16 seconds. And during period, it spends about 704 seconds.
    # model index 0: Grid_GBM_py_3_sid_ad52_model_python_1724993029821_1_model_57
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 23817.84088962527,
    #            'pnl_ratio_annual': 1504.0678070438103, 'sharp_ratio': 2.353314515646186,
    #            'max_drawdown': 0.11128486258615171, 'open_count': 188, 'close_count': 188, 'win_count': 182,
    #            'lose_count': 6, 'win_ratio': 0.9680851063829787, 'calmar_ratio': 13515.475259534323,
    #             'risk_ratio': 0.0}

    # 11.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 484365.24%.
    # every executing spend about 0.35 seconds. And during period, it spends about 1302 seconds.
    # model index 1: StackedEnsemble_AllModels_1_AutoML_3_20240831_112417
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 4843.652452998243,
    #            'pnl_ratio_annual': 305.8707863917576, 'sharp_ratio': 2.053345074283247,
    #            'max_drawdown': 0.11128476471175894, 'open_count': 172, 'close_count': 172,
    #            'win_count': 152, 'lose_count': 20, 'win_ratio': 0.8837209302325582,
    #            'calmar_ratio': 2748.541430482421, 'risk_ratio': 0.0}

    # 12.For SHSE.000922, by day, 20081001~20240830, pnl_ratio 1633224.43%.
    # every executing spend about 0.42 seconds. And during period, it spends about 1598 seconds.
    # model 2: StackedEnsemble_AllModels_1_AutoML_1_20240830_221403
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 16332.244324413428,
    #            'pnl_ratio_annual': 1031.361449552059, 'sharp_ratio': 2.337845278792665,
    #            'max_drawdown': 0.1405694952596901, 'open_count': 180, 'close_count': 180,
    #            'win_count': 176, 'lose_count': 4, 'win_ratio': 0.9777777777777777,
    #            'calmar_ratio': 7337.021788736646, 'risk_ratio': 0.0}

    # 13.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 1633224.43%.
    # every executing spend about 0.37 seconds. And during period, it spends about 1419 seconds.
    # model index 3: StackedEnsemble_AllModels_1_AutoML_1_20240830_223216
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 16332.244324413428,
    #            'pnl_ratio_annual': 1031.361449552059, 'sharp_ratio': 2.337845278792665,
    #            'max_drawdown': 0.1405694952596901, 'open_count': 180, 'close_count': 180,
    #             'win_count': 176, 'lose_count': 4, 'win_ratio': 0.9777777777777777,
    #             'calmar_ratio': 7337.021788736646, 'risk_ratio': 0.0}

    # 14.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 3182218.06%.
    # every executing spend about 0.18 seconds. And during period, it spends about 694 seconds.
    # model index 4: StackedEnsemble_BestOfFamily_1_AutoML_1_20240830_224552
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 31822.18062873413,
    #            'pnl_ratio_annual': 2009.5321677314805, 'sharp_ratio': 2.49662998495853,
    #            'max_drawdown': 0.14057980045232765, 'open_count': 180, 'close_count': 180,
    #            'win_count': 179, 'lose_count': 1, 'win_ratio': 0.9944444444444445,
    #            'calmar_ratio': 14294.601082556934, 'risk_ratio': 0.0}

    # 15.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 3761131.58%.
    # every executing spend about 0.37 seconds. And during period, it spends about 1450 seconds.
    # model index 5: StackedEnsemble_AllModels_1_AutoML_1_20240830_230008
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 37611.31581599839,
    #            'pnl_ratio_annual': 2375.1090437438424, 'sharp_ratio': 2.511382562534336,
    #            'max_drawdown': 0.11128496392686264, 'risk_ratio': 0.9999999976529464, 'open_count': 182,
    #            'close_count': 181, 'win_count': 180, 'lose_count': 1, 'win_ratio': 0.994475138121547}

    # 16.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 3771226.98%.
    # every executing spend about 0.16 seconds. And during period, it spends about 728 seconds.
    # model index 6: StackedEnsemble_BestOfFamily_1_AutoML_2_20240831_100856
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 37712.26986085459,
    #            'pnl_ratio_annual': 2381.4841694138277, 'sharp_ratio': 2.4679789956534623,
    #            'max_drawdown': 0.11128493557160711, 'risk_ratio': 0.9999999919424891,
    #            'open_count': 182, 'close_count': 181, 'win_count': 179, 'lose_count': 2,
    #            'win_ratio': 0.988950276243094, 'calmar_ratio': 21399.879122735747}


    # 17.For SHSE.000922, by day, 20081101~20240830, pnl_ratio 481734.91%.
    # every executing spend about 0.16 seconds. And during period, it spends about 727 seconds.
    # model index 7: StackedEnsemble_BestOfFamily_1_AutoML_1_20240831_155428
    # init_model_13_1 backtest finished:
    #           {'account_id': '16362727-4aff-11ef-8fae-80304917db79', 'pnl_ratio': 4817.349149783349,
    #            'pnl_ratio_annual': 304.2097646489485, 'sharp_ratio': 0.6643770119780699,
    #            'max_drawdown': 0.20365390121361607, 'risk_ratio': 0.999999936559408,
    #            'open_count': 145, 'close_count': 144, 'win_count': 128, 'lose_count': 16,
    #            'win_ratio': 0.8888888888888888, 'calmar_ratio': 1493.758591591416}
    # probable reason is train data from first 2800 rows between 20080801 and 20200422.
