# Predicting market trends with Speculator
The example.py file should be followed while reading this document.

Speculator combines technical analysis with machine learning to predict trends.
Each machine learning model has an identical interface, allowing you to easily
change between models without any difficulties.

For this example, we will use a random forest classifier.  Note that you could just
replace the model type from 'rf' to 'dnn' and this example would work the exact same way.

We can break up the process of classifying market data with a random forest in short steps:
1. Gather raw data
2. Parse data in data sets
3. Create a random forest model
4. Train the random forest model by feeding our parsed data sets
5. Predict a target

**Let's follow that process line-by-line in example.py.**

## Gather data
We must first create a sp.market.Market object.  These values are used for getting the JSON from [Poloniex's API](https://poloniex.com/support/api/)
This takes 4 keyword arguments:
* symbol: [Ticker from Poloniex API](https://poloniex.com/public?command=returnTicker)
* unit: Unit of time to check history ('hour', 'day', 'week', 'month', or 'year')
* count: Number of units to check history
* period: Seconds per chart candlesticks (300, 900, 1800, 7200, 14400, or 86400)

Returns: Market instance
``` python
m = market.Market(symbol='USDT_BTC', unit='month', count=6, period=86400)
```
This creates a Market instance, with market data from USD Tether to Bitcoin.
Its data is from the last 6 months.  Each entry in data is 1 day long (86400 seconds).

## Parse data in data sets
Now that we have our data, we must prepare it to be fed into our model.
Our model needs two axes of data, the x (features) and y (target market trend) axes.
The Market interface makes this extremely simple.

We can get evaluate the features of our raw dataset by using the features function of a Market object.
The features function takes 1 keyword argument:
* partition: How many dates to consider when evaluating technical analysis indicators
<p align="center">
  <img src="http://i.cubeupload.com/osMGQ1.png">
</p>

Returns: Pandas DataFrame of market features.  Each value is a numpy.float32.
``` python
x = m.features(partition=14)
```
This gathers feature data, with 14 data entries per calculation.
Financially, this is similar to a 14 day RSI (or other indicators) if the period is 1 day (86400 seconds).

With the features, we can evaluate the target market trend as bearish, neutral, or bullish.
The targets function takes 1 positional argument:
* x: Pandas DataFrame x axis (market features)
It also takes 1 keyword argument:
* delta: Buffer for the neutral market trend zone
<p align="center">
  <img src="https://i.cubeupload.com/K74Iur.png">
</p>

Returns: Pandas Series for target market trends of `features`.  Each value is a numpy.int8 code for a string market trend defined by a 1:1 mapping in market.TARGET\_CODES
``` python
y = market.targets(x, delta=25)
```
This will evaluate targets from the x axis (market features) that we just created.
The delta value of 25 indicates that a deviation of price by less than 12.5 on either side of the closing price is considered neutral.  Anything more than 12.5 is considered bearish or bullish, depending on the direction the price went after the last market closing price.

## Create and Train the Random Forest Model
Speculator creates and trains the model in the same step.
All you have to do is feed the x and y axes (features and targets) to the model, and specify the model.
Speculator will handle splitting the datasets, feeding them into the model, and training it.

The market.setup\_model function takes 2 positional arguments:
* x: X axis
* y: Y axis
It also takes a variable amount of keyword arguments.  Most are defined by Scikit Learn's RandomForestClassifier.
However, there are some specific to Speculator's API:
* model\_type: Machine learning model to use ('random\_forest')
* seed: Random state to produce consistent results.  Default is None, and behaves as if there was no seed.

Returns: Trained model instance of `model\_type`
``` python
model = market.setup_model(x[:-1], y, model_type='random_forest', seed=1,
                           n_estimators=65, n_jobs=4)
```
If you've been carefully paying attention, you'll see that the last element was not fed to the model (`x[:-1]`).
When we trained the y axis targets, we based each target off of the previous closing price and the current closing prices deviation from that.
Therefore, the last target could not be predicted, causing the targets to be 1 less in dimension than the features DataFrame.
To fix this, we slice the x DataFrame to align with the y Series.

We use seed=1 for consistency in the example, but this should not be used if actually trying to predict multiple times.
`n_estimators=65` and `n_jobs=4` are keyword arguments for [Scikit Learn's RandomForestClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).  The values we supplied tells the model to use 65 trees in the forest, and use 4 CPU threads.  This allows the model to be more accurate while simultaneously running faster.

## Predict a target
The model is built, trained, and now ready to predict the trends.  Simply use the .\_predict\_trends function on any x axis (feature data set) and the predictions will be returned.

The predict function takes 1 positional argument:
* x: Pandas DataFrame axis of features

Returns: List of predictions

We'll start by trying our model on our test set
``` python
trends = model._predict_trends(model.features.test)
```
`trends` is now a list of numpy.int8, corresponding to our market.
Various representations, like the confusion matrix or accuracy score, can be returned by comparing the actual test targets to what we predicted.
``` python
conf_mx = model.confusion_matrix(model.targets.test, trends)
acc = model.accuracy(model.features.test, model.targets.test)
```

Cool, so our model is trained and can predict test sets.  How about predicting the next trend?
Just use the predict method on the set we want to predict.
Remember when we excluded the last entry in the feature DataFrame when training our model?
Let's use that same entry but in the predict function instead.

Get the last entry:
``` python
next_date = x.tail(1)
```
and predict the trend using that entry:
``` python
trends = model._predict_trends(next_date)
```
Since the predict method returns a list, and we only predicted 1 entry, just get the value in the 0th index.
But wait, predict returns a 0, 1, or 2.  That's not readable and user-friendly.  We only use those values for the model.  We want to display what that number means.
The `market.target_code_to_name` function uses a reverse dictionary lookup to get the name corresponding to the code.  This is only possible because we defined the target codes (0, 1, 2) as a 1:1 mapping to a name.

Ok, but how confident is the answer that was given?
``` python
model._predict_probas(next_date)
model._predict_logs(next_date) # Logarithm probabilities
```

**Congratulations, you just created a RandomForest market model to predict trends in ~5 lines of code!**

