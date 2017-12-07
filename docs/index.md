#### `prophet@ESTAT` -- Applying Facebook `Prophet` model for forecasting ESTAT monthly indicators

**About**

This is a **blind/dummy** (no assumption whatsoever) application of  [`Prophet`](https://facebookincubator.github.io/prophet/) automatic procedure for forecast estimates of ESTAT [*tour_occ_nim*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_occ_nim&lang=en) time-series on the number of *"nights spent at tourist accommodation establishments"* per month.

**Description**

*(from the source [webpage](https://research.fb.com/prophet-forecasting-at-scale/))*

At its core, the [`Prophet`](https://facebookincubator.github.io/prophet/) procedure is an additive regression model with four main components (using [`Stan`](http://mc-stan.org/) Bayesian approach, see reference [below](#Reference)):
* a piecewise linear (or logistic) growth curve trend: Prophet automatically detects changes in trends by selecting changepoints from the data,
* a yearly seasonal component modeled using Fourier series,
* a weekly seasonal component using dummy variables,
* a user-provided list of important holidays.

In practice, non-linear trends are fit with yearly and weekly seasonality (plus holidays). The method is also robust to missing data, shifts in the trend, and large outliers.

**Usage**

Facebook has open sourced  [`Prophet software`](https://github.com/facebookincubator/prophet), a forecasting project with an [interface](https://pypi.python.org/pypi/fbprophet/) available in `Python`. We use this resource. 

Run the [`tour_forecast.py`](tour_forecast.py) source code or explore the [`run_forecast.ipynb`](run_forecast.ipynb) notebook to produce the following 5-years forecast estimates of ESTAT [*tour_occ_nim*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_occ_nim&lang=en) monthly indicator:

<img src="tour_occ_nim_predict.png" alt="tour_occ_nim prediction" width="800">

Another example is provided by the 1-year prediction of unemployment [*une_rt_m*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=une_rt_m&lang=en) monthly indicator:

<img src="une_rt_m_predict.png" alt="une_rt_m prediction" width="800">

**<a name="Reference"></a>Reference**

* Taylor, S.J. and Letham, B. (2017): [Forecasting at Scale](https://facebookincubator.github.io/prophet/static/prophet_paper_20170113.pdf).
