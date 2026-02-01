from src.models.linear import build_model as build_linear_model


MODEL_REGISTRY = {"linear": build_linear_model}
