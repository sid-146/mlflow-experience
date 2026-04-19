from typing import List, Any, Optional

from sklearn.pipeline import Pipeline

from src.core.context.contexts import RunContext
from src.core.handler.data.loader import DataLoader
from src.core.handler.data.splitter import DataSplitter
from src.core.logging.logger import console
from src.core.pipelines.preprocessing import PreprocessingPipeline
from src.core.pipelines.model_builder import ModelBuilder
from src.core.trackers.mlflow_tracker import MLflowTracker


# Todo: p0 Pipeline failing silently.
# Todo: p0 Add tracking first thing.
class Orchestrator:
    def __init__(self, context: RunContext):
        # Base Data
        self.context = context
        self.pipeline_steps: List[Any] = []
        self.pipeline: Optional[Pipeline] = None

        # Builder Objects
        # Todo: Share only required data with these pipelines.
        self.data_loader = DataLoader(context=context)
        self.data_splitter = DataSplitter(context=context)
        self.preprocessor = PreprocessingPipeline(context=context)
        self.model_builder = ModelBuilder(context=context.model)

        # Tracking Objects
        self.mlflow_tracker = MLflowTracker(context=context)

    def __enter__(self):
        console.debug("ContextManager for Orchestrator started.")
        return self
        # Can add some logic here.

    def _get_all_pipeline_steps(self) -> List[Any]:
        """
        Private method responsible for fetching all necessary pipeline steps
        from the constituent builders and returning a single, flat list of objects.
        This centralizes the pipeline composition logic.
        """
        steps: List[Any] = []
        for name, obj in self.pipeline_steps:
            steps.append(obj)

        return steps

    def build(self):
        # Todo: Add mlflow tracking in pipeline
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
            # following function is implemented correctly, it is not storing x_train, y_train, x_test, y_test
            x_train, x_test, y_train, y_test = self.data_splitter.split(
                X=self.data_loader.X,
                y=self.data_loader.y,
            )
            self.data_loader.X, self.data_loader.y = x_train, y_train
            self.data_loader.X_test, self.data_loader.y_test = x_train, y_train

        # Build Preprocessing Pipeline
        # Todo: Add feature engineering pipeline here once done.
        console.info("Building preprocessing pipeline...")
        self.pipeline_steps = self.preprocessor.build()
        console.info(
            "Preprocessing pipeline build completed. Ready for feature engineering..."
        )

        # Model Builder Pipeline
        # Todo: Feature Engineering to be added here.
        console.info(
            "Feature Engineering pipeline build completed. Ready for model object creation..."
        )
        model_step = self.model_builder.build()

        self.pipeline_steps.extend(
            model_step if isinstance(model_step, list) else [model_step]
        )
        console.info("Model instance created. Ready for pipeline instance creation...")

        # make pipeline
        self.pipeline = Pipeline(self.pipeline_steps)
        console.info(
            "Pipeline instance created. Pipeline ready for training and testing..."
        )

        # temp code following
        # self.mlflow_tracker.log_artifact(self.context.dataset.train.path, "train_data.csv")

        return

    # Following are placeholder they can be removed.
    def train(self):
        if not self.pipeline_steps:
            console.warning("Pipeline not built yet. Building and training...")
            self.build()

        self.pipeline = self.pipeline.fit(
            self.data_loader.X,
            self.data_loader.y,
        )
        console.info("Training completed, pipeline fitted with training dataset.")
        y_pred = self.pipeline.predict(self.data_loader.X)
        self.evaluate(y_true=self.data_loader.y, y_pred=y_pred)

    def test(self):
        console.info(
            f"Starting testing on {self.data_loader.X_test.shape} number of records."
        )
        y_pred = self.pipeline.predict(self.data_loader.X_test)
        self.evaluate(y_true=self.data_loader.y_test, y_pred=y_pred)

    def predict(self, X):
        y_pred = self.pipeline.predict(X)
        return y_pred

    # Todo: Fix this function
    def evaluate(self, y_true, y_pred):
        # give x and y, make prediction call, evaluate result
        # Generate a dictionary of name nad calling function/object to evaluate result
        # will be used by training and testing
        """
        Generates predictions and evaluates results on the provided X and y_true.
        (Note: This method is often replaced by CV for better reliability.)
        """

        console.info("--- Starting Evaluation (on provided dataset) ---")

        # 2. Use a structured loop (as previously detailed)
        # Example placeholder logic:
        from sklearn.metrics import accuracy_score, f1_score

        metrics = {
            "Accuracy": accuracy_score(y_true, y_pred),
            "F1 Score": f1_score(y_true, y_pred),
        }

        for metric_name, score in metrics.items():
            console.info(f"| {metric_name:<10}: {score:.4f}")

        console.info("--- Evaluation Complete ---")

    def __exit__(self, exc_type, exc, tb):
        # Can add exist logic here, like uploading artifacts or any cleanup.
        self.mlflow_tracker.log_artifact(
            console.handlers[1].baseFilename,
            f"logs/{self.mlflow_tracker.run.info.run_name}.log",
        )
