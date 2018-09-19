# MIT License
#
# Copyright (c) 2018 Dafiti OpenSource
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tests for module main.py. Fixtures comes from file conftest.py located at the same dir
of this file.
"""


import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
import pandas as pd
from pandas.core.indexes.range import RangeIndex
from pandas.util.testing import assert_frame_equal, assert_series_equal
from statsmodels.tsa.statespace.structural import UnobservedComponents
from statsmodels.tsa.statespace.structural import UnobservedComponentsResultsWrapper
from causalimpact import CausalImpact
from causalimpact.misc import standardize



def test_default_causal_cto(rand_data, pre_int_period, post_int_period):
    ci = CausalImpact(rand_data, pre_int_period, post_int_period)
    assert_frame_equal(ci.data, rand_data)
    assert ci.pre_period == pre_int_period
    assert ci.post_period == post_int_period
    pre_data = rand_data.loc[pre_int_period[0]: pre_int_period[1], :]
    assert_frame_equal(ci.pre_data, pre_data)

    post_data = rand_data.loc[post_int_period[0]: post_int_period[1], :]
    assert_frame_equal(ci.post_data, post_data)

    assert ci.alpha == 0.05
    normed_pre_data, (mu, sig) = standardize(pre_data)
    assert_frame_equal(ci.normed_pre_data, normed_pre_data)

    normed_post_data = (post_data - mu) / sig
    assert_frame_equal(ci.normed_post_data, normed_post_data)

    assert ci.mu_sig == (mu[0], sig[0])
    assert ci.model_args == {'standardize': True}

    assert isinstance(ci.model, UnobservedComponents)
    assert_array_equal(ci.model.endog, normed_pre_data.iloc[:, 0].values.reshape(-1, 1))
    assert_array_equal(ci.model.exog, normed_pre_data.iloc[:, 1:].values.reshape(
            -1,
            rand_data.shape[1] - 1
        )
    )
    assert ci.model.endog_names == 'y'
    assert ci.model.exog_names == ['x1', 'x2']
    assert ci.model.k_endog == 1
    assert ci.model.level
    assert ci.model.trend_specification == 'local level'

    assert isinstance(ci.trained_model, UnobservedComponentsResultsWrapper)
    assert ci.trained_model.nobs == len(pre_data)

    assert ci.inferences is not None
    assert ci.p_value > 0 and ci.p_value < 1
    assert ci.n_sims == 1000


def test_default_causal_cto_w_date(date_rand_data, pre_str_period, post_str_period):
    ci = CausalImpact(date_rand_data, pre_str_period, post_str_period)
    assert_frame_equal(ci.data, date_rand_data)
    assert ci.pre_period == pre_str_period
    assert ci.post_period == post_str_period
    pre_data = date_rand_data.loc[pre_str_period[0]: pre_str_period[1], :]
    assert_frame_equal(ci.pre_data, pre_data)

    post_data = date_rand_data.loc[post_str_period[0]: post_str_period[1], :]
    assert_frame_equal(ci.post_data, post_data)

    assert ci.alpha == 0.05
    normed_pre_data, (mu, sig) = standardize(pre_data)
    assert_frame_equal(ci.normed_pre_data, normed_pre_data)

    normed_post_data = (post_data - mu) / sig
    assert_frame_equal(ci.normed_post_data, normed_post_data)

    assert ci.mu_sig == (mu[0], sig[0])
    assert ci.model_args == {'standardize': True}

    assert isinstance(ci.model, UnobservedComponents)
    assert_array_equal(ci.model.endog, normed_pre_data.iloc[:, 0].values.reshape(-1, 1))
    assert_array_equal(ci.model.exog, normed_pre_data.iloc[:, 1:].values.reshape(
            -1,
            date_rand_data.shape[1] - 1
        )
    )
    assert ci.model.endog_names == 'y'
    assert ci.model.exog_names == ['x1', 'x2']
    assert ci.model.k_endog == 1
    assert ci.model.level
    assert ci.model.trend_specification == 'local level'

    assert isinstance(ci.trained_model, UnobservedComponentsResultsWrapper)
    assert ci.trained_model.nobs == len(pre_data)

    assert ci.inferences is not None
    assert ci.p_value > 0 and ci.p_value < 1
    assert ci.n_sims == 1000


def test_default_causal_cto_no_exog(rand_data, pre_int_period, post_int_period):
    rand_data = pd.DataFrame(rand_data.iloc[:, 0])
    ci = CausalImpact(rand_data, pre_int_period, post_int_period)
    assert_frame_equal(ci.data, rand_data)
    assert ci.pre_period == pre_int_period
    assert ci.post_period == post_int_period
    pre_data = rand_data.loc[pre_int_period[0]: pre_int_period[1], :]
    assert_frame_equal(ci.pre_data, pre_data)

    post_data = rand_data.loc[post_int_period[0]: post_int_period[1], :]
    assert_frame_equal(ci.post_data, post_data)

    assert ci.alpha == 0.05
    normed_pre_data, (mu, sig) = standardize(pre_data)
    assert_frame_equal(ci.normed_pre_data, normed_pre_data)

    normed_post_data = (post_data - mu) / sig
    assert_frame_equal(ci.normed_post_data, normed_post_data)

    assert ci.mu_sig == (mu[0], sig[0])
    assert ci.model_args == {'standardize': True}

    assert isinstance(ci.model, UnobservedComponents)
    assert_array_equal(ci.model.endog, normed_pre_data.iloc[:, 0].values.reshape(-1, 1))
    assert ci.model.exog is None
    assert ci.model.endog_names == 'y'
    assert ci.model.exog_names is None
    assert ci.model.k_endog == 1
    assert ci.model.level
    assert ci.model.trend_specification == 'local level'

    assert isinstance(ci.trained_model, UnobservedComponentsResultsWrapper)
    assert ci.trained_model.nobs == len(pre_data)

    assert ci.inferences is not None
    assert ci.p_value > 0 and ci.p_value < 1
    assert ci.n_sims == 1000


def test_default_causal_cto_w_np_array(rand_data, pre_int_period, post_int_period):
    data = rand_data.values
    ci = CausalImpact(data, pre_int_period, post_int_period)
    assert_array_equal(ci.data, data)
    assert ci.pre_period == pre_int_period
    assert ci.post_period == post_int_period
    pre_data = pd.DataFrame(data[pre_int_period[0]: pre_int_period[1] + 1, :])
    assert_frame_equal(ci.pre_data, pre_data)

    post_data = pd.DataFrame(data[post_int_period[0]: post_int_period[1] + 1, :])
    post_data.index = RangeIndex(start=len(pre_data), stop=len(rand_data))
    assert_frame_equal(ci.post_data, post_data)

    assert ci.alpha == 0.05
    normed_pre_data, (mu, sig) = standardize(pre_data)
    assert_frame_equal(ci.normed_pre_data, normed_pre_data)

    normed_post_data = (post_data - mu) / sig
    assert_frame_equal(ci.normed_post_data, normed_post_data)

    assert ci.mu_sig == (mu[0], sig[0])
    assert ci.model_args == {'standardize': True}

    assert isinstance(ci.model, UnobservedComponents)
    assert_array_equal(ci.model.endog, normed_pre_data.iloc[:, 0].values.reshape(-1, 1))
    assert_array_equal(ci.model.exog, normed_pre_data.iloc[:, 1:].values.reshape(
            -1,
            data.shape[1] - 1
        )
    )
    assert ci.model.endog_names == 'y'
    assert ci.model.exog_names == [1, 2]
    assert ci.model.k_endog == 1
    assert ci.model.level
    assert ci.model.trend_specification == 'local level'

    assert isinstance(ci.trained_model, UnobservedComponentsResultsWrapper)
    assert ci.trained_model.nobs == len(pre_data)

    assert ci.inferences is not None
    assert ci.p_value > 0 and ci.p_value < 1
    assert ci.n_sims == 1000


def test_causal_cto_w_no_standardization(rand_data, pre_int_period, post_int_period):
    ci = CausalImpact(rand_data, pre_int_period, post_int_period, standardize=False)
    pre_data = rand_data.loc[pre_int_period[0]: pre_int_period[1], :]
    post_data = rand_data.loc[post_int_period[0]: post_int_period[1], :]
    assert ci.normed_pre_data is None
    assert ci.normed_post_data is None
    assert ci.mu_sig is None
    assert_array_equal(ci.model.endog, pre_data.iloc[:, 0].values.reshape(-1, 1))
    assert_array_equal(ci.model.exog, pre_data.iloc[:, 1:].values.reshape(
            -1,
            rand_data.shape[1] - 1
        )
    )
    assert ci.p_value > 0 and ci.p_value < 1


def test_causal_cto_w_custom_model(rand_data, pre_int_period, post_int_period):
    pre_data = rand_data.loc[pre_int_period[0]: pre_int_period[1], :]
    post_data = rand_data.loc[post_int_period[0]: post_int_period[1], :]
    model = UnobservedComponents(endog=pre_data.iloc[:, 0], level='llevel',
                                 exog=pre_data.iloc[:, 1:])

    ci = CausalImpact(rand_data, pre_int_period, post_int_period, model=model)

    assert ci.model.endog_names == 'y'
    assert ci.model.exog_names == ['x1', 'x2']
    assert ci.model.k_endog == 1
    assert ci.model.level
    assert ci.model.trend_specification == 'local level'

    assert isinstance(ci.trained_model, UnobservedComponentsResultsWrapper)
    assert ci.trained_model.nobs == len(pre_data)


def test_causal_cto_raises_on_None_input(rand_data, pre_int_period, post_int_period):
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(None, pre_int_period, post_int_period)
    assert str(excinfo.value) == 'data input cannot be empty'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, None, post_int_period)
    assert str(excinfo.value) == 'pre_period input cannot be empty'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, None)
    assert str(excinfo.value) == 'post_period input cannot be empty'


def test_invalid_data_input_raises():
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact('test', [0, 5], [5, 10])
    assert str(excinfo.value) == 'Could not transform input data to pandas DataFrame.'

    data = [1, 2, 3, 4, 5, 6, 2 + 1j]
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(data, [0, 3], [3, 6])
    assert str(excinfo.value) == 'Input data must contain only numeric values.'

    data = np.random.randn(10, 2)
    data[0, 1] = np.nan
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(data, [0, 3], [3, 6])
    assert str(excinfo.value) == 'Input data cannot have NAN values.'


def test_invalid_response_raises():
    data = np.random.rand(100, 2)
    data[:, 0] = np.ones(len(data)) * np.nan
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(data, [0, 50], [50, 100])
    assert str(excinfo.value) == 'Input response cannot have just Null values.'

    data[0:2, 0] = 1    
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(data, [0, 50], [50, 100])
    assert str(excinfo.value) == ('Input response must have more than 3 non-null points '
        'at least.')

    data[0:3, 0] = 1    
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(data, [0, 50], [50, 100])
    assert str(excinfo.value) == 'Input response cannot be constant.'


def test_invalid_alpha_raises(rand_data, pre_int_period, post_int_period):
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, alpha=1)
    assert str(excinfo.value) == 'alpha must be of type float.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, alpha=2.)
    assert str(excinfo.value) == (
        'alpha must range between 0 (zero) and 1 (one) inclusive.')


def test_custom_model_input_validation(rand_data, pre_int_period, post_int_period):
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, model='test')
    assert str(excinfo.value) == 'Input model must be of type UnobservedComponents.'

    ucm = UnobservedComponents(rand_data.iloc[:101, 0], level='llevel',
        exog=rand_data.iloc[:101, 1:])
    ucm.level = False
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, model=ucm)
    assert str(excinfo.value) == 'Model must have level attribute set.'

    ucm = UnobservedComponents(rand_data.iloc[:101, 0], level='llevel',
        exog=rand_data.iloc[:101, 1:])
    ucm.exog = None
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, model=ucm)
    assert str(excinfo.value) == 'Model must have exog attribute set.'

    ucm = UnobservedComponents(rand_data.iloc[:101, 0], level='llevel',
        exog=rand_data.iloc[:101, 1:])
    ucm.data = None
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period, model=ucm)
    assert str(excinfo.value) == 'Model must have data attribute set.'


def test_kwargs_validation(rand_data, pre_int_period, post_int_period):
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, pre_int_period, post_int_period,
                          standardize='yes')
    assert str(excinfo.value) == 'Standardize argument must be of type bool.'


def test_periods_validation(rand_data, date_rand_data):
    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [5, 10], [4, 7])
    assert str(excinfo.value) == ('Values in training data cannot be present in the '
        'post-intervention data. Please fix your pre_period value to cover at most one '
        'point less from when the intervention happened.')

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20180101', '20180201'],
                          ['20180110', '20180210'])
    assert str(excinfo.value) == ('Values in training data cannot be present in the '
        'post-intervention data. Please fix your pre_period value to cover at most one '
        'point less from when the intervention happened.')

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [5, 10], [15, 11])
    assert str(excinfo.value) == 'post_period last number must be bigger than its first.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20180101', '20180110'],
                          ['20180115', '20180111'])
    assert str(excinfo.value) == 'post_period last number must be bigger than its first.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [0, 2], [15, 11])
    assert str(excinfo.value) == 'pre_period must span at least 3 time points.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20180101', '20180102'],
                          ['20180115', '20180111'])
    assert str(excinfo.value) == 'pre_period must span at least 3 time points.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [5, 0], [15, 11])
    assert str(excinfo.value) == 'pre_period last number must be bigger than its first.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20180105', '20180101'],
                          ['20180115', '20180111'])
    assert str(excinfo.value) == 'pre_period last number must be bigger than its first.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, 0, [15, 11])
    assert str(excinfo.value) == 'Input period must be of type list.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, '20180101', ['20180115', '20180130'])
    assert str(excinfo.value) == 'Input period must be of type list.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [0, 10, 30], [15, 11])
    assert str(excinfo.value) == ('Period must have two values regarding the beginning '
        'and end of the pre and post intervention data.')

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [0, None], [15, 11])
    assert str(excinfo.value) == 'Input period cannot have `None` values.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, [0, 5.5], [15, 11])
    assert str(excinfo.value) == 'Input must contain either int or str.'

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(rand_data, ['20180101', '20180110'],
                          ['20180111', '20180130'])
    assert str(excinfo.value) == (
        'If input period is string then input data must have index of type DatetimeIndex.'
    )

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20180101', '20180110'],
                          ['20180111', '20200130'])
    assert str(excinfo.value) == ('20200130 is not preset in data index.')

    with pytest.raises(ValueError) as excinfo:
        ci = CausalImpact(date_rand_data, ['20170101', '20180110'],
                          ['20180111', '20180120'])
    assert str(excinfo.value) == ('20170101 is not preset in data index.')


def test_default_causal_inferences(rand_data, pre_int_period, post_int_period):
    ci = CausalImpact(rand_data, pre_int_period, post_int_period)

    pre_data = rand_data.loc[pre_int_period[0]: pre_int_period[1], :]
    post_data = rand_data.loc[post_int_period[0]: post_int_period[1], :]

    normed_pre_data, (mu, sig) = standardize(pre_data)
    normed_post_data = (post_data - mu) / sig
    mu, sig = mu[0], sig[0]

    model = UnobservedComponents(endog=normed_pre_data.iloc[:, 0], level='llevel',
                                 exog=normed_pre_data.iloc[:, 1:])
    f_model = model.fit()
    pre_predictor = f_model.get_prediction()
    post_predictor = f_model.get_forecast(
        steps=len(normed_post_data), exog=normed_post_data.iloc[:, 1:]
    )
    init_nan_vec = pd.Series([np.nan] * (pre_int_period[1] + 1),
                                index=np.arange(pre_int_period[1] + 1))

    assert ci.inferences['post_cum_y'].iloc[-1] == np.cumsum(post_data['y']).iloc[-1]

    pre_preds = pre_predictor.predicted_mean * sig + mu
    pre_ci = pre_predictor.conf_int()
    pre_preds_lower = pre_ci.iloc[:, 0] * sig + mu
    pre_preds_upper = pre_ci.iloc[:, 1] * sig + mu
    post_preds = post_predictor.predicted_mean * sig + mu
    post_preds.inex = normed_post_data.index
    preds = pd.concat([pre_preds, post_preds])
    preds.name = 'preds'
    assert_series_equal(ci.inferences['preds'], preds)

    post_preds = pd.concat([init_nan_vec, post_preds])
    post_preds.name = 'post_preds'
    assert_series_equal(post_preds, ci.inferences['post_preds'])

    post_ci = post_predictor.conf_int()
    post_preds_lower = post_ci.iloc[:, 0] * sig + mu
    post_preds_upper = post_ci.iloc[:, 1] * sig + mu
    post_preds_lower_complete = pd.concat([init_nan_vec, post_preds_lower])
    post_preds_lower_complete.name = 'post_preds_lower'
    assert_series_equal(post_preds_lower_complete, ci.inferences['post_preds_lower'])
    post_preds_upper_complete = pd.concat([init_nan_vec, post_preds_upper])
    post_preds_upper_complete.name = 'post_preds_upper'
    assert_series_equal(post_preds_upper_complete, ci.inferences['post_preds_upper'])

    preds_lower = pd.concat([pre_preds_lower, post_preds_lower])
    preds_lower.name = 'preds_lower'
    assert_series_equal(preds_lower, ci.inferences['preds_lower'])

    preds_upper = pd.concat([pre_preds_upper, post_preds_upper])
    preds_upper.name = 'preds_upper'
    assert_series_equal(preds_upper, ci.inferences['preds_upper'])
    assert ci.inferences['post_cum_pred'].iloc[-1] == np.cumsum(post_preds).iloc[-1]

    ci.inferences['post_cum_pred_lower'].iloc[-1] == np.cumsum(post_preds_lower).iloc[-1]
    ci.inferences['post_cum_pred_upper'].iloc[-1] == np.cumsum(post_preds_upper).iloc[-1]

    point_effects = rand_data.iloc[:, 0] - preds
    point_effects.name = 'point_effects'
    assert_series_equal(point_effects, ci.inferences['point_effects'])

    point_effects_lower = rand_data.iloc[:, 0] - preds_lower
    point_effects_lower.name = 'point_effects_lower'
    assert_series_equal(point_effects_lower, ci.inferences['point_effects_lower'])
    
    point_effects_upper = rand_data.iloc[:, 0] - preds_upper
    point_effects_upper.name = 'point_effects_upper'
    assert_series_equal(point_effects_upper, ci.inferences['point_effects_upper'])

    post_point_effects = post_data.iloc[:, 0] - post_preds
    assert ci.inferences['cum_effects'].iloc[-1] == np.cumsum(post_point_effects).iloc[-1]
 
    post_point_effects_lower = post_data.iloc[:, 0] - post_preds_lower
    assert ci.inferences['cum_effects_lower'].iloc[-1] == np.cumsum(
        post_point_effects_lower).iloc[-1]
    
    post_point_effects_upper = post_data.iloc[:, 0] - post_preds_upper
    assert ci.inferences['cum_effects_upper'].iloc[-1] == np.cumsum(
        post_point_effects_upper).iloc[-1]

    # Summary testing.
    mean_post_y = post_data.iloc[:, 0].mean()
    sum_post_y = post_data.iloc[:, 0].sum()
    assert_allclose(ci.summary_data['average']['actual'], mean_post_y)
    assert_allclose(ci.summary_data['cumulative']['actual'], sum_post_y)

    mean_post_pred = post_preds.mean()
    sum_post_pred = post_preds.sum()
    assert_allclose(ci.summary_data['average']['predicted'], mean_post_pred)
    assert_allclose(ci.summary_data['cumulative']['predicted'], sum_post_pred)

    mean_post_pred_lower = post_preds_lower.mean()
    sum_post_pred_lower = post_preds_lower.sum()
    assert_allclose(ci.summary_data['average']['predicted_lower'], mean_post_pred_lower)
    assert_allclose(ci.summary_data['cumulative']['predicted_lower'], sum_post_pred_lower)

    mean_post_pred_upper = post_preds_upper.mean()
    sum_post_pred_upper = post_preds_upper.sum()
    assert_allclose(ci.summary_data['average']['predicted_upper'], mean_post_pred_upper)
    assert_allclose(ci.summary_data['cumulative']['predicted_upper'], sum_post_pred_upper)

    abs_effect = mean_post_pred - mean_post_y
    sum_abs_effect = sum_post_pred - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect'], abs_effect)
    assert_allclose(ci.summary_data['cumulative']['abs_effect'], sum_abs_effect)

    abs_effect_lower = mean_post_pred_lower - mean_post_y
    sum_abs_effect_lower = sum_post_pred_lower - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect_lower'], abs_effect_lower)
    assert_allclose(ci.summary_data['cumulative']['abs_effect_lower'],
                    sum_abs_effect_lower)

    abs_effect_upper = mean_post_pred_upper - mean_post_y
    sum_abs_effect_upper = sum_post_pred_upper - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect_upper'], abs_effect_upper)
    assert_allclose(ci.summary_data['cumulative']['abs_effect_upper'],
                    sum_abs_effect_upper)

    rel_effect = abs_effect / mean_post_y
    sum_abs_effect = sum_abs_effect / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect'], rel_effect)
    assert_allclose(ci.summary_data['cumulative']['rel_effect'], sum_abs_effect)

    rel_effect_lower = abs_effect_lower / mean_post_y
    sum_abs_effect_lower = sum_abs_effect_lower / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect_lower'], rel_effect_lower)
    assert_allclose(ci.summary_data['cumulative']['rel_effect_lower'],
                    rel_effect_lower)

    rel_effect_upper = abs_effect_upper / mean_post_y
    sum_abs_effect_upper = sum_abs_effect_upper / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect_upper'], rel_effect_upper)
    assert_allclose(ci.summary_data['cumulative']['rel_effect_upper'],
                    rel_effect_upper)

    assert ci.p_value is not None
    assert ci.p_value > 0
    assert ci.p_value < 1


def test_default_causal_inferences_w_date(date_rand_data, pre_str_period,
                                          post_str_period):
    ci = CausalImpact(date_rand_data, pre_str_period, post_str_period)

    pre_data = date_rand_data.loc[pre_str_period[0]: pre_str_period[1], :]
    post_data = date_rand_data.loc[post_str_period[0]: post_str_period[1], :]

    normed_pre_data, (mu, sig) = standardize(pre_data)
    normed_post_data = (post_data - mu) / sig
    mu, sig = mu[0], sig[0]

    model = UnobservedComponents(endog=normed_pre_data.iloc[:, 0], level='llevel',
                                 exog=normed_pre_data.iloc[:, 1:])
    f_model = model.fit()
    pre_predictor = f_model.get_prediction()
    post_predictor = f_model.get_forecast(
        steps=len(normed_post_data), exog=normed_post_data.iloc[:, 1:]
    )
    nobs = date_rand_data.index.get_loc(pre_str_period[1]) + 1
    init_nan_vec = pd.Series(
        [np.nan] * (nobs),
        index=pd.date_range(start=pre_str_period[0], periods=nobs)
    )

    assert ci.inferences['post_cum_y'].iloc[-1] == np.cumsum(post_data['y']).iloc[-1]

    pre_preds = pre_predictor.predicted_mean * sig + mu
    pre_ci = pre_predictor.conf_int()
    pre_preds_lower = pre_ci.iloc[:, 0] * sig + mu
    pre_preds_upper = pre_ci.iloc[:, 1] * sig + mu
    post_preds = post_predictor.predicted_mean * sig + mu
    post_preds.inex = normed_post_data.index
    preds = pd.concat([pre_preds, post_preds])
    preds.name = 'preds'
    assert_series_equal(ci.inferences['preds'], preds)

    post_preds = pd.concat([init_nan_vec, post_preds])
    post_preds.name = 'post_preds'
    assert_series_equal(post_preds, ci.inferences['post_preds'])

    post_ci = post_predictor.conf_int()
    post_preds_lower = post_ci.iloc[:, 0] * sig + mu
    post_preds_upper = post_ci.iloc[:, 1] * sig + mu
    post_preds_lower_complete = pd.concat([init_nan_vec, post_preds_lower])
    post_preds_lower_complete.name = 'post_preds_lower'
    assert_series_equal(post_preds_lower_complete, ci.inferences['post_preds_lower'])
    post_preds_upper_complete = pd.concat([init_nan_vec, post_preds_upper])
    post_preds_upper_complete.name = 'post_preds_upper'
    assert_series_equal(post_preds_upper_complete, ci.inferences['post_preds_upper'])

    preds_lower = pd.concat([pre_preds_lower, post_preds_lower])
    preds_lower.name = 'preds_lower'
    assert_series_equal(preds_lower, ci.inferences['preds_lower'])

    preds_upper = pd.concat([pre_preds_upper, post_preds_upper])
    preds_upper.name = 'preds_upper'
    assert_series_equal(preds_upper, ci.inferences['preds_upper'])
    assert ci.inferences['post_cum_pred'].iloc[-1] == np.cumsum(post_preds).iloc[-1]

    ci.inferences['post_cum_pred_lower'].iloc[-1] == np.cumsum(post_preds_lower).iloc[-1]
    ci.inferences['post_cum_pred_upper'].iloc[-1] == np.cumsum(post_preds_upper).iloc[-1]

    point_effects = date_rand_data.iloc[:, 0] - preds
    point_effects.name = 'point_effects'
    assert_series_equal(point_effects, ci.inferences['point_effects'])

    point_effects_lower = date_rand_data.iloc[:, 0] - preds_lower
    point_effects_lower.name = 'point_effects_lower'
    assert_series_equal(point_effects_lower, ci.inferences['point_effects_lower'])
    
    point_effects_upper = date_rand_data.iloc[:, 0] - preds_upper
    point_effects_upper.name = 'point_effects_upper'
    assert_series_equal(point_effects_upper, ci.inferences['point_effects_upper'])

    post_point_effects = post_data.iloc[:, 0] - post_preds
    assert ci.inferences['cum_effects'].iloc[-1] == np.cumsum(post_point_effects).iloc[-1]

    post_point_effects_lower = post_data.iloc[:, 0] - post_preds_lower
    assert ci.inferences['cum_effects_lower'].iloc[-1] == np.cumsum(
        post_point_effects_lower).iloc[-1]

    post_point_effects_upper = post_data.iloc[:, 0] - post_preds_upper
    assert ci.inferences['cum_effects_upper'].iloc[-1] == np.cumsum(
        post_point_effects_upper).iloc[-1]

    # Summary testing.
    mean_post_y = post_data.iloc[:, 0].mean()
    sum_post_y = post_data.iloc[:, 0].sum()
    assert_allclose(ci.summary_data['average']['actual'], mean_post_y)
    assert_allclose(ci.summary_data['cumulative']['actual'], sum_post_y)

    mean_post_pred = post_preds.mean()
    sum_post_pred = post_preds.sum()
    assert_allclose(ci.summary_data['average']['predicted'], mean_post_pred)
    assert_allclose(ci.summary_data['cumulative']['predicted'], sum_post_pred)

    mean_post_pred_lower = post_preds_lower.mean()
    sum_post_pred_lower = post_preds_lower.sum()
    assert_allclose(ci.summary_data['average']['predicted_lower'], mean_post_pred_lower)
    assert_allclose(ci.summary_data['cumulative']['predicted_lower'], sum_post_pred_lower)

    mean_post_pred_upper = post_preds_upper.mean()
    sum_post_pred_upper = post_preds_upper.sum()
    assert_allclose(ci.summary_data['average']['predicted_upper'], mean_post_pred_upper)
    assert_allclose(ci.summary_data['cumulative']['predicted_upper'], sum_post_pred_upper)

    abs_effect = mean_post_pred - mean_post_y
    sum_abs_effect = sum_post_pred - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect'], abs_effect)
    assert_allclose(ci.summary_data['cumulative']['abs_effect'], sum_abs_effect)

    abs_effect_lower = mean_post_pred_lower - mean_post_y
    sum_abs_effect_lower = sum_post_pred_lower - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect_lower'], abs_effect_lower)
    assert_allclose(ci.summary_data['cumulative']['abs_effect_lower'],
                    sum_abs_effect_lower)

    abs_effect_upper = mean_post_pred_upper - mean_post_y
    sum_abs_effect_upper = sum_post_pred_upper - sum_post_y
    assert_allclose(ci.summary_data['average']['abs_effect_upper'], abs_effect_upper)
    assert_allclose(ci.summary_data['cumulative']['abs_effect_upper'],
                    sum_abs_effect_upper)

    rel_effect = abs_effect / mean_post_y
    sum_abs_effect = sum_abs_effect / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect'], rel_effect)
    assert_allclose(ci.summary_data['cumulative']['rel_effect'], sum_abs_effect)

    rel_effect_lower = abs_effect_lower / mean_post_y
    sum_abs_effect_lower = sum_abs_effect_lower / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect_lower'], rel_effect_lower)
    assert_allclose(ci.summary_data['cumulative']['rel_effect_lower'],
                    rel_effect_lower)

    rel_effect_upper = abs_effect_upper / mean_post_y
    sum_abs_effect_upper = sum_abs_effect_upper / sum_post_y
    assert_allclose(ci.summary_data['average']['rel_effect_upper'], rel_effect_upper)
    assert_allclose(ci.summary_data['cumulative']['rel_effect_upper'],
                    rel_effect_upper)

    assert ci.p_value is not None
    assert ci.p_value > 0
    assert ci.p_value < 1
