# Selecting relevant features for the decision tree model
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder



print("Initializing please wait for 15 seconds")
print(" ")
print(" ")
# Load the data from the specified file path
insurance_data_gbm = pd.read_csv('sample.csv')

features_decision_tree = ['Age', 'Smokes', 'Drinks Alcohol', 'Exercises Irregularly']
target_decision_tree = 'Claim Amount'

insurance_data_gbm[target_decision_tree].fillna(insurance_data_gbm[target_decision_tree].mean(), inplace=True)


# Preparing the feature matrix and target vector for the decision tree model
X_decision_tree = insurance_data_gbm[features_decision_tree]
y_decision_tree = insurance_data_gbm[target_decision_tree]

# One-hot encoding for categorical variables in the decision tree dataset
categorical_features_decision_tree = ['Smokes', 'Drinks Alcohol', 'Exercises Irregularly']
one_hot_encoder_decision_tree = OneHotEncoder(handle_unknown='ignore')

# Creating a column transformer for the decision tree dataset
preprocessor_decision_tree = ColumnTransformer(transformers=[
    ('onehot', one_hot_encoder_decision_tree, categorical_features_decision_tree)
], remainder='passthrough')

# Splitting the data into training and testing sets for the decision tree model
X_train_decision_tree, X_test_decision_tree, y_train_decision_tree, y_test_decision_tree = train_test_split(X_decision_tree, y_decision_tree, test_size=0.2, random_state=0)

# Creating a decision tree pipeline
from sklearn.tree import DecisionTreeRegressor

decision_tree_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor_decision_tree),
    ('regressor', DecisionTreeRegressor(random_state=0))
])

# Training the decision tree model
decision_tree_pipeline.fit(X_train_decision_tree, y_train_decision_tree)

# Predicting on the test set with the decision tree model
y_pred_decision_tree = decision_tree_pipeline.predict(X_test_decision_tree)

# Evaluating the decision tree model
mse_decision_tree = mean_squared_error(y_test_decision_tree, y_pred_decision_tree)   #118005.2436689857
r2_decision_tree = r2_score(y_test_decision_tree, y_pred_decision_tree)    #0.8380264103082545

# sample data
# user_data = {'Age': 27, 'Sex': 'Female'}

def getQuotes(input_data):

    default_values = {
        'Age': input_data.get('Age', 0),
        'Smokes': input_data.get('Smokes', 'Unknown'),
        'Drinks Alcohol': input_data.get('Drinks Alcohol','Unknown'),
        'Exercises Irregularly': input_data.get('Exercises Irregularly', 'Unknown')
    }

    user_data_df = pd.DataFrame([default_values])


    predicted_claim_amount = decision_tree_pipeline.predict(user_data_df)

    print("Predicted Claim Amount:", predicted_claim_amount[0])
    return predicted_claim_amount[0]

# getQuotes(user_data)
