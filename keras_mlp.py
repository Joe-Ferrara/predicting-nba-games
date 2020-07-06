import pandas as pd

# preprocessing

print('pre-preocessing')

exec(open('pre_processing.py').read())

from sklearn.preprocessing import StandardScaler

# scale for support vector
# scale columns so mean is 0 and variance is 1
# different than what's done in paper

train_scaled = []
val_scaled = []
# test_scaled = []

for i in range(len(train_data)):
    scaler = StandardScaler()
    X_t = train_data[i][0]
    X_v = val_data[i][0]
    # X_test = test_data[i][0]
    scaler.fit(X_t)
    train_scaled.append([scaler.transform(X_t), train_data[i][1]])
    val_scaled.append([scaler.transform(X_v), val_data[i][1]])
    # test_scaled.append(scaler.transform(X_test))

def perc_corr(y, y_hat):
    """Return the percent of entries where y and y_hat agree.

    y, y_hat are series of 0's and 1's with the same length."""
    total = len(y)
    correct = 0
    for i in range(len(y)):
        if y.iloc[i] == y_hat[i]:
            correct += 1
    return 100*correct/total

def run_model(train_data, val_data, e, r, d):
    """e = epochs, r = l2 regularization, d = dropout"""
    train_perc = []
    val_perc = []
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
    return train_perc, val_perc

import tensorflow as tf
from tensorflow import keras

run_model(train_scaled, val_scaled, 20, .004, 0.2)
