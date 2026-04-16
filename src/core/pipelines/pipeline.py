from abc import ABC, abstractmethod


class BasePipeline(ABC):
    def __init__(self, config: dict):
        self.config = config
        self.steps = []

    @abstractmethod
    def run(self):
        raise NotImplementedError
