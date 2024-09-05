# coding = utf - 8
# from __future__ import unicode_literals, print_function, absolute_import, annotations

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = (
    "pandas",
    "numpy",
    "matplotlib",
    "statsmodels",
    "sklearn",
    "tensorflow",
    "keras",
    "gm",
    "tushare")
_missing_dependencies = []

for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:  # pragma: no cover
        _missing_dependencies.append(f"{_dependency}: {_e}")

if _missing_dependencies:  # pragma: no cover
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(_missing_dependencies)
    )
del _hard_dependencies, _dependency, _missing_dependencies

from sq.config import (
    LOG_LEVEL,
)
from sq.gm import (
    # layer
    BlackFilter,
    PermanentBlackFilter,
    WhiteFilter,
    AverageOrder,
    GMOrder,
    ManualOrder,
    MultiFactors1Order,
    SingleFactor1Order,
    SingleFactor2Order,
    SingleFactor3Order,
    SingleFactor4Order,
    SingleFactor5Order,
    SingleFactor6Order,
    SVMOrder,
    VIPAOrder,
    AllSymbolSelector,
    DefensiveStrategySorter,
    FamaFrenchSorter,
    GrowthModelSorter,
    HowardRothmanSorter,
    MultiFactors1Sorter,
    MultiFactors2Sorter,
    MultiFactors3Sorter,
    MultiFactors3Sorter,
    MultiFactorsPBROESorter,
    PairTradeSorter,
    SingleFactor1Sorter,
    # models
    GMModel,
    SVMModel,
    # trainers
    ManualTrainer,
    SVMTrainer,
    # tools
    tools,

)
from sq.layers import (
    # BaseLayer,
    Filter,
    TopNFilter,
    Merge,
    Order,
    OrderOp,
    Selector,
    Sorter,
    Layer,
)
from sq.models import (
    # BaseModel,
    Model,
)
from sq.trainers import (
    # BaseTrainer,
    Trainer,
)
from sq.tushare import (
    TuShareModel,
)
from sq.utils import (
    print_log,
)

# Use __all__ to let type checkers know what is part of the public API.
# sq is a py.typed library: the public API is determined
__all__ = [
    # config
    "LOG_LEVEL",

    # layer
    # "BaseLayer",
    "Filter",
    "TopNFilter",
    "Merge",
    "Order",
    "OrderOp",
    "Selector",
    "Sorter",
    "Layer",

    # models
    # "BaseModel",
    "Model",

    # trainers
    # "BaseTrainer",
    "Trainer",

    # utils
    "print_log",

    # gm.layers
    "BlackFilter",
    "PermanentBlackFilter",
    "WhiteFilter",
    "AverageOrder",
    "GMOrder",
    "ManualOrder",
    "MultiFactors1Order",
    "SingleFactor1Order",
    "SingleFactor2Order",
    "SingleFactor3Order",
    "SingleFactor4Order",
    "SingleFactor5Order",
    "SingleFactor6Order",
    "SVMOrder",
    "VIPAOrder",
    "AllSymbolSelector",
    "DefensiveStrategySorter",
    "FamaFrenchSorter",
    "GrowthModelSorter",
    "HowardRothmanSorter",
    "MultiFactors1Sorter",
    "MultiFactors2Sorter",
    "MultiFactors3Sorter",
    "MultiFactorsPBROESorter",
    "PairTradeSorter",
    "SingleFactor1Sorter",

    # gm.models
    "GMModel",
    "SVMModel",

    # gm.trainers
    "ManualTrainer",
    "SVMTrainer",

    # tushare models
    # "BaseTuShareModel",
]
