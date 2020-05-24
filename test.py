import pandas as pd

# preprocessing

print('pre-processing')

exec(open('pre_processing.py').read())

# pre-processing outputs train_data, val_data, test_data

# functions

def perc_corr(y, y_hat):
    """Return the percent of entries where y and y_hat agree.

    y, y_hat are series of 0's and 1's with the same length."""
    total = len(y)
    correct = 0
    for i in range(len(y)):
        if y.iloc[i] == y_hat[i]:
            correct += 1
    return 100*correct/total

def run_test(model, train_data, val_data, test_data):
    train_perc = []
    val_perc = []
    test_perc = []
    for i in range(len(train_data)):
        X_t, y_t = train_data[i][0], train_data[i][1]
        model.fit(X_t, y_t)
        y_t_hat = model.predict(X_t)
        train_perc.append(perc_corr(y_t, y_t_hat))
        X_v, y_v = val_data[i][0], val_data[i][1]
        y_v_hat = model.predict(X_v)
        val_perc.append(perc_corr(y_v, y_v_hat))
        X_test, y_test = test_data[i][0], test_data[i][1]
        y_test_hat = model.predict(X_test)
        test_perc.append(perc_corr(y_test, y_test_hat))
    return train_perc, val_perc, test_perc

#######################
# logistic regression #
#######################

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model_str = 'logistic regression'
train_percents, val_percents, test_percents = run_test(model, train_data, val_data, test_data)
print(model_str)
print('train percentages')
percents = train_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('validation percentages')
percents = val_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('test percentages')
percents = test_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('')

####################
# nearest neighbor #
####################

from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=100)
model_str = 'nearest neighbor'
train_percents, val_percents, test_percents = run_test(model, train_data, val_data, test_data)
print(model_str)
print('train percentages')
percents = train_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('validation percentages')
percents = val_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('test percentages')
percents = test_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('')

#########
# scale #
#########

from sklearn.preprocessing import StandardScaler

# scale for support vector and mlp
# mean 0, variance 1
# different than what's done in paper

train_scaled = []
val_scaled = []
test_scaled = []

for i in range(len(train_data)):
    scaler = StandardScaler()
    X_t = train_data[i][0]
    X_v = val_data[i][0]
    X_test = test_data[i][0]
    scaler.fit(X_t)
    train_scaled.append([scaler.transform(X_t), train_data[i][1]])
    val_scaled.append([scaler.transform(X_v), val_data[i][1]])
    test_scaled.append([scaler.transform(X_test), test_data[i][1]])

#################################
# linear support vector machine #
#################################

from sklearn.svm import LinearSVC

model = LinearSVC(C=1, dual=False)
model_str = 'linear support vector classifier'
train_percents, val_percents, test_percents = run_test(model, train_scaled, val_scaled, test_scaled)
print(model_str)
print('train percentages')
percents = train_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('validation percentages')
percents = val_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('test percentages')
percents = test_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('')

##########################
# multi-layer perceptron #
##########################

import tensorflow as tf
from tensorflow import keras

def run_model(train_data, val_data, test_data, e, r, d):
    """e = epochs, r = l2 regularization, d = dropout"""
    train_perc = []
    val_perc = []
    test_perc = []
    for i in range(len(train_data)):
        shape = train_data[i][0].shape[1]
        model = keras.models.Sequential()
        model.add(keras.layers.Dense(100, activation='tanh', input_shape = (shape,),  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.add(keras.layers.Dropout(d))
        model.add(keras.layers.Dense(100, activation='tanh',  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.add(keras.layers.Dropout(d))
        model.add(keras.layers.Dense(50, activation='tanh',  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.add(keras.layers.Dropout(d))
        model.add(keras.layers.Dense(25, activation='tanh',  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.add(keras.layers.Dropout(d))
        model.add(keras.layers.Dense(10, activation='tanh',  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.add(keras.layers.Dropout(d))
        model.add(keras.layers.Dense(1, activation='sigmoid',  kernel_regularizer = keras.regularizers.l2(l = r)))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        X_t, y_t = train_data[i][0], train_data[i][1]
        X_v, y_v = val_data[i][0], val_data[i][1]
        model.fit(X_t, y_t, epochs=e, validation_data=(X_v,y_v))
        y_t_hat = model.predict(X_t)
        y_t_hat = y_t_hat.round()
        train_perc.append(perc_corr(y_t, y_t_hat))
        y_v_hat = model.predict(X_v)
        y_v_hat = y_v_hat.round()
        val_perc.append(perc_corr(y_v, y_v_hat))
        X_test, y_test = test_data[i][0], test_data[i][1]
        y_test_hat = model.predict(X_test)
        y_test_hat = y_test_hat.round()
        test_perc.append(perc_corr(y_test, y_test_hat))
    return train_perc, val_perc, test_perc

train_percents, val_percents, test_percents = run_model(train_scaled, val_scaled, test_scaled, 20, .004, 0.2)
model_str = 'multi-layer perceptron'
print(model_str)
print('train percentages')
percents = train_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('validation percentages')
percents = val_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
print('test percentages')
percents = test_percents
perc_strs = ''
for i in range(0, 2):
    perc_strs += '{:.2f}'.format(percents[i])
    perc_strs += '%, '
perc_strs += '{:.2f}'.format(percents[2])
perc_strs += '%'
print(perc_strs)
