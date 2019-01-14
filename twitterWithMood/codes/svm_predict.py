import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.externals import joblib

if __name__ == '__main__':

    # load test file
    test_path = '../data/Test Data/'
    test_file = 'test_trump_nlp.csv'
    data = pd.read_csv(test_path + test_file, error_bad_lines=False)
    # data = data.dropna()
    data['retweet_count'] = pd.to_numeric(data['retweet_count'])
    data_X = data[['user_friends_count', 'user_followers_count', 'retweet_count', 'exclamation_number', 'length',
                 'question_number', 'uppercase_ratio', 'nlppred']].values
    # Standardization
    scaler = StandardScaler()
    scaler.fit(data_X)
    data_X = scaler.transform(data_X)

    # load svm model
    model = joblib.load('../codes/Model/happiness_index_svm.model')
    p_label = model.predict(data_X)

    # output result to file
    result = data[['created_at']]
    result.rename(columns={'created_at': 'dateTime'}, inplace=True)
    result['prediction'] = p_label
    result['prediction'] = result['prediction'].astype(int)
    output_file = test_file.replace('nlp', 'svm_result')
    result.to_csv(output_file, index=False)
