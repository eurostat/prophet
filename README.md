prophet
=======

Applying _Facebook_ `Prophet` model for forecasting _Eurostat_ monthly indicators
---

This is a **blind/dummy** (no assumption whatsoever) application of  [`Prophet`](https://facebookincubator.github.io/prophet/) automatic procedure for forecast estimates of Eurostat [*tour_occ_nim*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_occ_nim&lang=en) time-series on the number of *"nights spent at tourist accommodation establishments"* per month.

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

Run the [`tour_forecast.py`](tour_forecast.py) source code or explore the [`run_forecast.ipynb`](run_forecast.ipynb) notebook to produce the following 5-years forecast estimates of Eurostat [*tour_occ_nim*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=tour_occ_nim&lang=en) monthly indicator:

<img src="https://github.com/eurostat/prophet/blob/master/docs/tour_occ_nim_predict.png" alt="tour_occ_nim prediction" width="800">

Another example is provided by the 1-year prediction of unemployment [*une_rt_m*](http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=une_rt_m&lang=en) monthly indicator:

<img src="https://github.com/eurostat/prophet/blob/master/docs/une_rt_m_predict.png" alt="une_rt_m prediction" width="800">

**About**

<table align="centre">
    <tr> <td align="left"><i>status</i></td> <td align="left">since 2017 &ndash; closed </td> </tr> 
    <tr> <td align="left"><i>contributors</i></td> 
    <td align="left" valign="middle">
<a href="https://github.com/gjacopo"><img src="https://github.com/gjacopo.png" width="40"></a>
</td> </tr> 
    <tr> <td align="left"><i>license</i></td> <td align="left"><a href="https://joinup.ec.europa.eu/sites/default/files/eupl1.1.-licence-en_0.pdfEUPL">EUPL</a> </td> </tr> 
</table>

**<a name="Reference"></a>Reference**

* Taylor, S.J. and Letham, B. (2017): [Forecasting at Scale](https://facebookincubator.github.io/prophet/static/prophet_paper_20170113.pdf).
