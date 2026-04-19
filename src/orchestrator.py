import pandas as pd

from src.core.context.contexts import RunContext
from src.core.handler.data.loader import DataLoader
from src.core.handler.data.splitter import DataSplitter
from src.core.logging.logger import console
from src.core.pipelines.preprocessing import PreprocessingPipeline
from src.core.trackers.mlflow_tracker import MLflowTracker


class Orchestrator:
    def __init__(self, context: RunContext):
        self.context = context
        self.data_loader = DataLoader(context=context)
        self.data_splitter = DataSplitter(context=context)
        self.mlflow_tracker = MLflowTracker(context=context)

    def build(self):
        console.info(
            f"Starting pipeline build for model : {self.context.mlflow.experiment_name}"
        )
        self.mlflow_tracker.start_run()
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

        # Todo: Start from here
        # Todo: Build Pipeline to handle following functions.
        # Todo: Input will be the training set and output will be the processed training set, and same for test set but different processing.
        pipeline = PreprocessingPipeline(
            context=self.context,
            # mlflow_tracker=self.mlflow_tracker,
        )
        console.info("Building preprocessing pipeline...")
        # Todo: Add mlflow tracking in pipeline
        self.pipeline = pipeline.build()
        console.info("Preprocessing pipeline steps added successfully.")

        # Todo: Feature Engineering to be added here only then fit_transform can be done.

        console.info("Preprocessing transformation completed. Ready for training.")

        # temp code following
        # self.mlflow_tracker.log_artifact(self.context.dataset.train.path, "train_data.csv")

        # Upload logs file to artifacts
        self.mlflow_tracker.log_artifact(
            console.handlers[1].baseFilename,
            f"logs/{self.mlflow_tracker.run.info.run_name}.log",
        )
        return

    # Following are placeholder they can be removed.
    def train(self):
        if not self.pipeline:
            console.warning("Pipeline  not built yet. Building and training...")
            self.build()
        self.pipeline.fit(
            self.data_loader.X,
            # self.data_loader.y,
        )

    def predict():
        return
