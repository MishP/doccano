import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import re

def process_text(x):
    # remove non-english characters
    x.replace('company', '').replace('noncompany', '')
    x = re.sub("[^a-zA-Z]"," ",x)
    # remove punctuation marks
    x = re.sub("\.,\?\!","",x)
    x = re.sub("[ ]+"," ",x)
    # lowercase
    return x.lower().strip()

def run_model_on_file(input_filename, output_filename, user_id, method='bow'):
    # nlp = spacy.load("en_core_web_sm")
    print('Reading input file...')
    df = pd.read_csv(input_filename)

    # df_labeled = df_labeled[['text', 'label_id']]
    df['text'] = df['text'].apply(process_text)
    df['label'] = df['label_id']
    
    df = df[ df['text']!='' ]

    if method=='w2v':
        import spacy
        # from spacy.lang.en.stop_words import STOP_WORDS
        nlp = spacy.load("en_core_web_sm")
        df['vec'] = df['text'].apply(lambda x: nlp(x).vector)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer(smooth_idf=False)
    vectorizer.fit(df['text'])

    if method == 'w2v':
        def df_to_matrix(df):
            X = np.array([np.array(x) for x in df['vec'].values])
            if 'label' in df.columns:
                y = df['label'].values
            else:
                y = [None] * len(df)
            return X,y

    else:
        def df_to_matrix(df):
            X = vectorizer.transform(df['text'])
            # df['vec'] = transformer.fit_transform(df['vec'])
            y = df['label']
            return X,y

    def run_model(tmp_df):
        X, y = df_to_matrix(tmp_df)
        predictions_probabilities = model.predict_proba(X)
        confidence = np.max(predictions_probabilities, axis=1)
        predictions = np.argmax(predictions_probabilities, axis=1)
        tmp_df['prediction'] = [model.classes_[v] for v in predictions]
        tmp_df['confidence'] = confidence
        tmp_df['is_error'] = (tmp_df['prediction'] != y)
        return tmp_df

    X, y = df_to_matrix(df[ ~pd.isnull(df['label']) ])
    y = y.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    print('Training the model...')

    # model_params = {'bootstrap': True, 'criterion': 'gini', 'max_depth': 16, 'max_features': 'sqrt', 'min_samples_leaf': 16, 'min_samples_split': 16, 'n_estimators': 200}
    # model = RandomForestClassifier(**model_params)

    model = LogisticRegression(verbose=True)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_train)
    print('Performance on train set:')
    print(metrics.classification_report(y_train, y_pred))

    print('Performance on test set:')
    y_pred = model.predict(X_test)
    print(metrics.classification_report(y_test, y_pred))

    columns=['text', 'label', 'prediction', 'is_error', 'confidence']
    tmp_df = df.copy()
    tmp_df['label'] = None
    print('Running the model on the entire dataset...')
    tmp_df = run_model(df)

    tmp_df['user_id'] = user_id
    tmp_df = tmp_df.rename({'confidence': 'prob',
                            'id': 'document_id'}, axis=1)
    tmp_df['label_id'] = tmp_df['prediction']
    # save to CSV file
    print('Saving output...')
    tmp_df[['document_id', 'label_id', 'user_id', 'prob']].to_csv(output_filename, index=False, header=True)

    print('Done running the model!')
    return tmp_df


if __name__ == '__main__':
    run_model_on_file('../../ml_input.csv', '../../ml_out_manual.csv', user_id=2)