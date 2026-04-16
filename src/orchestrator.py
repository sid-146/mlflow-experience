import pandas as pd

from src.core.context.contexts import RunContext
from src.core.logging.logger import console
from src.core.handler.data.loader import DataLoader
from src.core.handler.data.splitter import DataSplitter


class Orchestrator:
    def __init__(self, context: RunContext):
        self.context = context
        self.data_loader = DataLoader(context=context)
        self.data_splitter = DataSplitter(context=context)

    def build(self):
        console.info(
            f"Starting pipeline build for model : {self.context.mlflow.experiment_name}"
        )
        console.debug("Reading data from source...")

        # Read Data from source.
        self.data_loader.load_data()
        console.debug(
            f"Data loaded successfully with shape: {self.data_loader.data.shape}"
        )
        console.debug("Pipeline build completed successfully.")

        # Split Dataset
        console.debug("Splitting dataset into train and test sets...")
        if self.context.dataset.test:
            console.info("Test dataset provided, skipping train-test split.")
        else:
            console.info("No test dataset provided, proceeding with train-test split.")
            self.data_splitter.split(
                X=self.data_loader.X,
                y=self.data_loader.y,
            )

        return

    # Following are placeholder they can be removed.
    def train():
        return

    def predict():
        return
