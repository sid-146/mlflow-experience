from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer

"""
Module contains transformers for data preprocessing steps.
Each transformer should inherit from BaseEstimator and TransformerMixin to be compatible with scikit-learn pipelines.
The STEP_REGISTRY is a temporary mapping of step names to their corresponding transformer classes, 
which can be used to dynamically create pipelines based on configuration.
"""

# Todo: Currently working on only dataframe, make it for numpy and other data formats


class RenameColumnsTransformer(BaseEstimator, TransformerMixin):
    """Transformer to rename columns in a DataFrame based on a provided mapping."""

    def __init__(self, mapping):
        self.mapping = mapping

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.rename(columns=self.mapping)


class MissingValueTransformer(BaseEstimator, TransformerMixin):
    """Transformer to handle missing values in a DataFrame based on a specified strategy."""

    def __init__(self, strategy="mean"):
        self.strategy = strategy
        self.fill_values = {}

    def fit(self, X, y=None):
        if self.strategy == "mean":
            self.fill_values = X.mean(numeric_only=True)
        elif self.strategy == "median":
            self.fill_values = X.median(numeric_only=True)
        elif self.strategy == "mode":
            self.fill_values = X.mode().iloc[0]
        return self

    def transform(self, X):
        return X.fillna(self.fill_values)


class CleaningTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, replacements: dict):
        self.replacements = replacements

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        for col, mapping in self.replacements.items():
            X[col] = X[col].replace(mapping)
        return X


class FilterTransformer(BaseEstimator, TransformerMixin):
    """Transformer to filter rows in a DataFrame based on a specified condition."""

    """This is NOT ideal inside sklearn pipelines (because pipelines expect same row count)."""

    def __init__(self, condition: str):
        self.condition = condition

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.query(self.condition)


class ColumnTransformerBuilder:
    def __init__(self, numeric=None, categorical=None):
        self.numeric = numeric or {}
        self.categorical = categorical or {}

    def build(self):
        transformers = []

        # Numeric pipeline
        if self.numeric:
            cols = self.numeric["columns"]
            if self.numeric.get("scaling") == "standard":
                transformers.append(("num", StandardScaler(), cols))

        # Categorical pipeline
        if self.categorical:
            cols = self.categorical["columns"]
            if self.categorical.get("encoding") == "onehot":
                transformers.append(
                    ("cat", OneHotEncoder(handle_unknown="ignore"), cols)
                )

        return ColumnTransformer(transformers=transformers)

    def fit(self, X, y=None):
        self.ct = self.build()
        self.ct.fit(X)
        return self

    def transform(self, X):
        return self.ct.transform(X)

    def fit_transform(self, X, y=None):
        return self.build().fit_transform(X)
