import argparse
import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from azureml.core.run import Run

parser = argparse.ArgumentParser("train random forest on iris")
parser.add_argument("--output_dir", type=str, help="output dir")
args = parser.parse_args()

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

mse = mean_squared_error(y_test, clf.predict(X_test))
run = Run.get_context()
run.log("lr diabetes mse", mse)

os.makedirs(args.output_dir, exist_ok=True)

output_file = os.path.join(args.output_dir, "model.pkl")
with open(output_file, "wb") as fp:
    pickle.dump(clf, fp)