import argparse

import matplotlib.pyplot as plt
import mlflow
import pandas
import seaborn as sns
from sklearn import model_selection
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.validation import check_is_fitted
from datetime import datetime
from mlflow.models.signature import infer_signature
from sklearn.datasets import load_iris
from mlflow.tracking import MlflowClient
from sklearn.metrics import accuracy_score


def fetch_data() -> pandas.DataFrame:
    """
    Fetch the data from the database
    :return:
    """
    iris = load_iris()  # get data from db
    data = iris.data
    target = iris.target
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pandas.DataFrame(data, columns=names[:-1])
    dataset['class'] = target
    return dataset


def split_dataset(data: pandas.DataFrame, test_size=0.2, random_state=7):
    """
    Split the dataset into train and validation
    :param data:
    :param test_size:
    :param random_state:
    :return:
    """
    X = data.iloc[:, 0:4]
    y = data.iloc[:, 4]
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, y, test_size=test_size,
                                                                                    random_state=random_state)
    return X_train, X_validation, Y_train, Y_validation


def generate_confusion_matrix_figure(model_name, model):
    """
    Generate a confusion matrix figure
    :param model_name:  Name of the model
    :param model: The model
    :return:
    """
    data = fetch_data()
    X_train, X_validation, Y_train, Y_validation = split_dataset(data)
    try:
        check_is_fitted(model)
    except NotFittedError:
        model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    cm = confusion_matrix(Y_validation, predictions)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f"Confusion Matrix for {model_name}")
    sns.heatmap(cm, annot=True, ax=ax, fmt='g')
    return fig


def run_experiment(experiment_id, n_splits=5):
    """
    Run the experiment
    :param experiment_id: id of the experiment
    :param n_splits: number of splits for cross validation
    :return:
    """
    data = fetch_data()
    X, y = data.iloc[:, 0:4], data.iloc[:, 4]

    models = {
        'LR': LogisticRegression(solver='liblinear', multi_class='ovr'),
        'LDA': LinearDiscriminantAnalysis(),
        'KNN': KNeighborsClassifier(),
        'CART': DecisionTreeClassifier(),
        'NB': GaussianNB(),
        'SVM': SVC(gamma='auto')
    }

    # Run each model in a separate run
    for model_name, model in models.items():
        print(f"Running {model_name}...")

        # create a unique run id
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_id = f"{model_name}-{run_id}"

        # start a new run in MLflow
        with mlflow.start_run(experiment_id=experiment_id, run_name=run_id) as run:
            kfold = model_selection.KFold(n_splits=n_splits, random_state=7, shuffle=True)
            cv_results = model_selection.cross_val_score(model, X, y, cv=kfold, scoring='accuracy')
            print(f"Accuracy: {cv_results.mean():.3f} ({cv_results.std():.3f})")

            # Log the model accuracy to MLflow
            mlflow.log_metric("accuracy", cv_results.mean())
            mlflow.log_metric("std", cv_results.std())
            mlflow.log_param("model_name", model_name)
            mlflow.log_param("n_splits", n_splits)

            for fold_idx, kflod_result in enumerate(cv_results):
                mlflow.log_metric(key="crossval", value=kflod_result, step=fold_idx)

            # # fit model on the training set and log the model to MLflow
            X_train, X_validation, Y_train, Y_validation = split_dataset(data)
            model.fit(X_train, Y_train)
            signature = infer_signature(X_train, model.predict(X_train))
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path=model_name,
                signature=signature
            )
            print("Model saved in run %s" % mlflow.active_run().info.run_uuid)
            # log artifacts
            fig = generate_confusion_matrix_figure(model_name, model)
            mlflow.log_figure(fig, f"{model_name}-confusion-matrix.png")


def get_best_run(experiment_id, metric):
    """
    Get the best run for the experiment
    :param experiment_id:  id of the experiment
    :param metric:  metric to use for comparison
    :return:
    """
    client = MlflowClient()

    # Get all the runs for the experiment
    runs = client.search_runs(experiment_id)

    # Find the run with the highest accuracy metric
    best_run = None
    best_metric_value = 0
    for run in runs:
        metric_value = run.data.metrics[metric]
        if metric_value > best_metric_value:
            best_metric_value = metric_value
            best_run = run
    # Return the best run
    return best_run


def eval_best_model(experiment_id, metric):
    """
    Evaluate the best model
    :param experiment_id:  id of the experiment
    :param metric:  metric to use for comparison when selecting the best model
    :return:
    """
    model = get_best_model(experiment_id, metric)
    # Get the test dataset
    data = fetch_data()
    X_train, X_validation, Y_train, Y_validation = split_dataset(data)
    # Evaluate the model
    predictions = model.predict(X_validation)
    accuracy = accuracy_score(Y_validation, predictions)
    print(f"Best model accuracy: {accuracy:.3f}")


def get_best_model(experiment_id, metric):
    """
    Get the best model for the experiment
    :param experiment_id:
    :param metric:
    :return:
    """
    # Get the best run
    best_run = get_best_run(experiment_id, metric)
    # Get the model artifact URI
    model_uri = f"runs:/{best_run.info.run_id}/{best_run.data.params['model_name']}"
    # Load the model as a PyFuncModel
    model = mlflow.pyfunc.load_model(model_uri)
    return model


def register_best_model(experiment_id, metric, registered_model_name):
    """
    Register the best model in the experiment as a new model in the MLflow Model Registry
    :param experiment_id:
    :param metric:
    :param registered_model_name:
    :return:
    """
    # Get the best run
    best_run = get_best_run(experiment_id, metric)
    # Get the model artifact URI
    model_uri = f"runs:/{best_run.info.run_id}/{best_run.data.params['model_name']}"
    # registered_model = find_model_by_name(registered_model_name)
    # if registered_model is None:
    registered_model = mlflow.register_model(model_uri, registered_model_name)
    return registered_model


def find_model_by_name(registered_model_name):
    """
    Check if a model with the given name already exists in the model registry
    :param registered_model_name:
    :return:
    """
    client = MlflowClient()
    model = client.get_registered_model(registered_model_name)
    return model


def promote_model_to_stage(registered_model_name, stage, version=None):
    """
    Promote the latest version of a model to the given stage
    :param registered_model_name:
    :param stage:
    :return:
    """
    client = MlflowClient()
    model = client.get_registered_model(registered_model_name)
    if version is not None:
        client.transition_model_version_stage(
            name=registered_model_name,
            version=version,
            stage=stage,
        )
        return
    latest_versions = [mv.version for mv in model.latest_versions]
    client.transition_model_version_stage(
        name=registered_model_name,
        version=max(latest_versions),
        stage=stage,
    )


def rollback_model_version(registered_model_name, stage, version):
    """
    Rollback the model version to the given version
    :param registered_model_name:
    :param stage:
    :param version:
    :return:
    """
    client = MlflowClient()
    client.transition_model_version_stage(
        name=registered_model_name,
        version=version,
        stage=stage
    )


def call_model_at_stage(registered_model_name, stage, data):
    """
    Call the production model to get predictions
    :param registered_model_name:
    :param stage:
    :param data:
    :return:
    """
    model = mlflow.pyfunc.load_model(
        model_uri=f"models:/{registered_model_name}/{stage}"
    )
    # Evaluate the model
    predictions = model.predict(data)
    return predictions


def list_experiments_artifacts(experiment_id):
    """
    List the artifacts for all the runs in the experiment
    :param experiment_id:
    :return:
    """
    client = MlflowClient()

    # Get all the runs for the experiment
    runs = client.search_runs(experiment_id)

    # Get the artifacts for each run
    for run in runs:
        print(f"Run ID: {run.info.run_id}")
        artifacts = client.list_artifacts(run.info.run_id)
        for artifact in artifacts:
            print(f" - {artifact.path}")


def list_experiment_models(experiment_id):
    """
    List the models for all the runs in the experiment
    :param experiment_id:
    :return:
    """
    client = MlflowClient()

    # Get all the runs for the experiment
    runs = client.search_runs(experiment_id)

    # Get the artifacts for each run
    for run in runs:
        print(f"Run ID: {run.info.run_id}")
        artifacts = client.list_artifacts(run.info.run_id)
        for artifact in artifacts:
            if artifact.path.endswith(".pkl"):
                print(f" - {artifact.path}")


def create_experiment(experiment_name):
    """
    Create a new experiment in MLflow
    :param experiment_name:
    :return:
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is not None:
        experiment_id = experiment.experiment_id
    else:
        experiment_id = mlflow.create_experiment(experiment_name)
    return experiment_id


def get_best_model_uri(experiment_id, metric):
    """
    Get the best model URI for the experiment
    :param experiment_id:
    :param metric:
    :return:
    """
    # Get the best run
    best_run = get_best_run(experiment_id, metric)
    # Get the model artifact URI
    model_uri = f"runs:/{best_run.info.run_id}/{best_run.data.params['model_name']}"
    return model_uri


if __name__ == '__main__':
    # mlflow.set_tracking_uri("http://myserver.com/mlflow:5000")
    parser = argparse.ArgumentParser()
    parser.add_argument('--nsplits', type=int, default=5)
    parser.add_argument('--nephocs', type=int, default=500)
    args = parser.parse_args()

    # Create a new experiment in MLflow and get experiment ID
    experiment_name = f"Iris Classifier"
    experiment_id = create_experiment(experiment_name)

    #run_experiment(experiment_id, n_splits=args.nsplits)
    # list_experiment_models(experiment_id)
    run = get_best_run(experiment_id, metric="accuracy")
    print(run.info.run_name,
          run.data.metrics["accuracy"],
          run.data.params["model_name"])

    model_uri = get_best_model_uri(experiment_id, metric="accuracy")
    print(model_uri)

    # model_name = "iris-classifier-uao-mar4-23"
    # stage = "Production"
    # register_best_model(experiment_id, "accuracy", model_name)
    # promote_model_to_stage(model_name, stage)
    # rollback_model_version(model_name, stage, 2)

    # data = [{
    #     "sepal-length": 6.9,
    #     "sepal-width": 3.1,
    #     "petal-length": 5.1,
    #     "petal-width": 2.3
    # }]
    # predictions = call_model_at_stage(model_name, stage, data)
    # print(predictions)
