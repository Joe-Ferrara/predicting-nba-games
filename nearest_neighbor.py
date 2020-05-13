import pandas as pd

# preprocessing

print('pre-preocessing')

exec(open('pre_processing.py').read())

def perc_corr(y, y_hat):
    """Return the percent of entries where y and y_hat agree.

    y, y_hat are series of 0's and 1's with the same length."""
    total = len(y)
    correct = 0
    for i in range(len(y)):
        if y.iloc[i] == y_hat[i]:
            correct += 1
    return 100*correct/total

def run_model(model, train_data, val_data):
    train_perc = []
    val_perc = []
    for i in range(len(train_data)):
        X_t, y_t = train_data[i][0], train_data[i][1]
        model.fit(X_t, y_t)
        y_t_hat = model.predict(X_t)
        train_perc.append(perc_corr(y_t, y_t_hat))
        X_v, y_v = val_data[i][0], val_data[i][1]
        y_v_hat = model.predict(X_v)
        val_perc.append(perc_corr(y_v, y_v_hat))
    return train_perc, val_perc


from sklearn.neighbors import KNeighborsClassifier

ns = [5, 10, 25, 50, 100]


model_str = 'nearest neighbor'
print('')
print(model_str)
print('number neighbors')
print(ns)
for n in ns:
    print('n = ' + str(n))
    model = KNeighborsClassifier(n_neighbors=n)
    train_percents, val_percents = run_model(model, train_data, val_data)
    print('train percentages')
    perc_strs = ['{:.2f}'.format(x) for x in train_percents]
    print(perc_strs)
    print('validation percentages')
    perc_strs = ['{:.2f}'.format(x) for x in val_percents]
    print(perc_strs)
    print('')
