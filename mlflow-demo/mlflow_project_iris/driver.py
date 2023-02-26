import mlflow

# mlflow run https://github.com/haruiz/iris-classifier -P nsplits=20
if __name__ == '__main__':
    mlflow.projects.run(
        'https://github.com/haruiz/iris-clf-project',
        backend='local',
        parameters={
            'nsplits': 5
        })
