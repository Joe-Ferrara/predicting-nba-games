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


from sklearn.svm import SVC # support vector classifier

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

from sklearn.svm import LinearSVC

model = LinearSVC(C=1, dual=False)
model_str = 'linear support vector classifier'
print('')
print(model_str)
train_percents, val_percents = run_model(model, train_scaled, val_scaled)
print('')
print(model_str)
print('train percentages')
perc_strs = ['{:.2f}'.format(x) for x in train_percents]
print(perc_strs)
print('validation percentages')
perc_strs = ['{:.2f}'.format(x) for x in val_percents]
print(perc_strs)


model_str = 'rbf support vector classifier'
print('')
print(model_str)
Cs = [0.2]
gammas = [0.003, 0.005]
print('Cs')
print(Cs)
print('gammas')
print(gammas)
for c in Cs:
    for g in gammas:
        print('C = ' + str(c))
        print('gamma = ' + str(g))
        model = SVC(C = c, gamma = g)
        train_percents, val_percents = run_model(model, train_scaled, val_scaled)
        print('train percentages')
        perc_strs = ['{:.2f}'.format(x) for x in train_percents]
        print(perc_strs)
        print('validation percentages')
        perc_strs = ['{:.2f}'.format(x) for x in val_percents]
        print(perc_strs)
        print('')

# C = 1
# support vector classifier
# train percentages
# ['85.73', '69.20', '85.43']
# validation percentages
# ['59.46', '59.46', '59.46']
