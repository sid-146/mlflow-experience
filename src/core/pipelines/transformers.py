from typing import List

from sklearn import set_config
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    OrdinalEncoder,
    MinMaxScaler,
    RobustScaler,
)
from sklearn.compose import ColumnTransformer

from src.core.logging.logger import console


"""
Module contains transformers for data preprocessing steps.
Each transformer should inherit from BaseEstimator and TransformerMixin to be compatible with scikit-learn pipelines.
The STEP_REGISTRY is a temporary mapping of step names to their corresponding transformer classes,
which can be used to dynamically create pipelines based on configuration.
"""

# setting output type to pandas to match output format for each transformers, sklearn default to numpy arrays
set_config(transform_output="pandas")


# Todo: Currently working on only dataframe, make it for numpy and other data formats
class RenameColumnsTransformer(BaseEstimator, TransformerMixin):
    """Transformer to rename columns in a DataFrame based on a provided mapping."""

    def __init__(self, mapping=None):
        self.mapping = mapping

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.mapping is None:
            return X
        return X.rename(columns=self.mapping)


class MissingValueTransformer(BaseEstimator, TransformerMixin):
    """Transformer to handle missing values in a DataFrame based on column-specific strategies."""

    def __init__(self, params=None):
        # Handle both policy objects and simple dict parameters
        self.params = params
        self.fill_values = {}
        self.strategies = {}

    # Todo: Improve this function. Too complex
    def fit(self, X, y=None):
        if self.params is None:
            return self

        # Handle MissingValuePolicy with columns
        if hasattr(self.params, "columns"):
            for col_config in self.params.columns:
                col_name = col_config.name
                strategy = col_config.strategy

                if strategy == "mean":
                    self.fill_values[col_name] = X[col_name].mean()
                elif strategy == "median":
                    self.fill_values[col_name] = X[col_name].median()
                elif strategy == "mode":
                    self.fill_values[col_name] = X[col_name].mode().iloc[0]
                elif strategy == "constant":
                    self.fill_values[col_name] = col_config.fill_value

                self.strategies[col_name] = strategy
        else:
            # Fallback for simple strategy parameter
            strategy = getattr(self.params, "strategy", "mean")
            if strategy == "mean":
                self.fill_values = X.mean(numeric_only=True)
            elif strategy == "median":
                self.fill_values = X.median(numeric_only=True)
            elif strategy == "mode":
                self.fill_values = X.mode().iloc[0]

        return self

    def transform(self, X):
        if self.fill_values:
            return X.fillna(self.fill_values)
        return X


class CleaningTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, replacements: dict = None):
        self.replacements = replacements or {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not self.replacements:
            return X
        X = X.copy()
        for col, mapping in self.replacements.items():
            if col in X.columns:
                X[col] = X[col].replace(mapping)
        return X


class FilterTransformer(BaseEstimator, TransformerMixin):
    """Transformer to filter rows in a DataFrame based on a specified condition."""

    """This is NOT ideal inside sklearn pipelines (because pipelines expect same row count)."""

    def __init__(self, condition: str = None):
        self.condition = condition

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if self.condition is None:
            return X
        return X.query(self.condition)


# All code commented below can be done using Column Transformer.
# Either Create a new class as following code or use ColumnTransformer packaged inside another class to handle
class ScalingTransformer(BaseEstimator, TransformerMixin):
    """
    Orchestrates multiple scaling and encoding strategies based on
    a per-column configuration policy.
    """

    #

    def __init__(self, params):
        self.ct = None
        self.params = params
        self._strategy_map = {
            "standard": StandardScaler(),
            "minmax": MinMaxScaler(),
            "robust": RobustScaler(),
        }

    def build(self):
        # Todo: identify a way to introduce type hinting
        if not self.params or not hasattr(self.params, "columns"):
            return "passthrough"

        grouped = {}

        for col_detail in self.params.columns:
            strategy = col_detail.strategy
            name = col_detail.name

            existing: List[str] = grouped.get(strategy, [])
            existing.append(name)
            grouped[strategy] = existing

        transformers = []
        for strategy, cols in grouped.items():
            obj = self._strategy_map.get(strategy)

            if not obj:
                console.warning(f"Strategy '{strategy}' not mapped. Skipping...")
                continue

            transformers.append((f"{strategy}_scaling", obj, cols))

        return ColumnTransformer(
            transformers=transformers,
            remainder="passthrough",
            verbose_feature_names_out=False,
        )

    def fit(self, X, y=None):
        self.ct = self.build()
        if self.ct != "passthrough":
            self.ct.fit(X, y)
        return self

    def transform(self, X):
        if self.ct == "passthrough":
            return X
        return self.ct.transform(X)

    def get_feature_names_out(self, input_features=None):
        if self.ct == "passthrough":
            return input_features
        return self.ct.get_feature_names_out(input_features)


# #####################################################################
class EncodingTransformer(BaseEstimator, TransformerMixin):
    """
    Orchestrates multiple encoding strategies based on
    a per-column configuration policy.
    """

    def __init__(self, params):
        self.ct = None
        self.params = params
        self._strategy_map = {
            "one_hot": OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            "ordinal": OrdinalEncoder(),
            # "label": LabelEncoder(),  # Note: LabelEncoder is not suitable for DataFrames directly
            # "target": TargetEncoder(),  # Requires category_encoders library
        }

    def build(self):
        if not self.params or not hasattr(self.params, "columns"):
            return "passthrough"

        grouped = {}
        orders = []

        for col_detail in self.params.columns:
            strategy = col_detail.strategy
            name = col_detail.name
            orders.append(col_detail.order)

            existing: List[str] = grouped.get(strategy, [])
            existing.append(name)
            grouped[strategy] = existing

        transformers = []
        for strategy, cols in grouped.items():
            obj = self._strategy_map.get(strategy)

            if not obj:
                console.warning(f"Strategy '{strategy}' not mapped. Skipping...")
                continue

            transformers.append((f"{strategy}_encoding", obj, cols))

        return ColumnTransformer(
            transformers=transformers,
            remainder="passthrough",
            verbose_feature_names_out=False,
        )

    def fit(self, X, y=None):
        self.ct = self.build()
        if self.ct != "passthrough":
            self.ct.fit(X, y)
        return self

    def transform(self, X):
        if self.ct == "passthrough":
            return X
        return self.ct.transform(X)

    def get_feature_names_out(self, input_features=None):
        if self.ct == "passthrough":
            return input_features
        return self.ct.get_feature_names_out(input_features)
