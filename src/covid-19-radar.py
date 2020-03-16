#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2020 Arthur Pinheiro
#
# MIT Licence. See http://opensource.org/licenses/MIT

import sys
import os

from workflow import Workflow3, web


UPDATE_SETTINGS = {'github_slug': 'xilopaint/alfred-covid-19-radar'}


def update_workflow():
    """Update and install workflow if a newer version is available."""
    if wf.update_available:
        wf.add_item(
            title='A newer version of COVID-19 Radar is available.',
            subtitle='Action this item to install the update.',
            autocomplete='workflow:update',
            valid=True,
            icon='icons/update.png'
        )


def update_cache():
    """Return JSON object."""
    # Confirmed
    r = web.get('https://covid2019-api.herokuapp.com/timeseries/confirmed')
    r.raise_for_status()
    data_confirmed = r.json()
    wf.cache_data('confirmed', data_confirmed)

    # Deaths
    r = web.get('https://covid2019-api.herokuapp.com/timeseries/deaths')
    r.raise_for_status()
    data_deaths = r.json()
    wf.cache_data('deaths', data_deaths)

    # Recovered
    r = web.get('https://covid2019-api.herokuapp.com/timeseries/recovered')
    r.raise_for_status()
    data_recovered = r.json()
    wf.cache_data('recovered', data_recovered)

    return data_confirmed


def show_locations(data):
    """Show locations."""
    for i, item in enumerate(data['confirmed']):
        if item['Province/State']:
            title = '{} / {}'.format(
                item['Country/Region'], item['Province/State']
            )
        else:
            title = item['Country/Region']

        arg = '{};{}'.format(title, i)

        wf.add_item(title=title, valid=True, arg=arg)

    return wf.send_feedback()


def show_stats(i):
    """Show stats."""
    title = 'Back to Locations'
    wf.add_item(title=title, valid=True, arg='back', icon='icons/back.png')

    # Confirmed
    data = wf.cached_data('confirmed', update_cache, 3600)
    dates = data['confirmed'][i]
    current_date = data['dt']
    title = 'Confirmed: {}'.format(dates[current_date])
    wf.add_item(title=title, valid=True)

    # Deaths
    data = wf.cached_data('deaths', update_cache, 3600)
    dates = data['deaths'][i]
    current_date = data['dt']
    title = 'Deaths: {}'.format(dates[current_date])
    wf.add_item(title=title, valid=True)

    # Recovered
    data = wf.cached_data('recovered', update_cache, 3600)
    dates = data['recovered'][i]
    current_date = data['dt']
    title = 'Recovered: {}'.format(dates[current_date])
    wf.add_item(title=title, valid=True)

    return wf.send_feedback()


def main(wf):
    """Run workflow."""
    update_workflow()

    if '--lookup' in wf.args:
        i = int(os.environ['i'])
        show_stats(i)

    else:
        data = wf.cached_data('confirmed', update_cache, 3600)
        show_locations(data)


if __name__ == '__main__':
    wf = Workflow3(update_settings=UPDATE_SETTINGS)
    sys.exit(wf.run(main))
