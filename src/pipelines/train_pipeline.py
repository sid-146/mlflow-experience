from src.pipelines.pipeline import BasePipeline

from sklearn.pipeline import Pipeline


class Trainer(BasePipeline):
    def __init__(self, config: dict):
        super().__init__(config)
        self.pipeline: Pipeline = None
        self.X_train = None
        self.Y_train = None

    def build(self):
        print("Building training pipeline...")

    def run(self):
        if not self.pipeline:
            self.build()

        print("Running training pipeline...")
        self.pipeline = self.pipeline.fit(self.X_train, self.Y_train)
        
    