# -*- coding: utf-8 -*-

import requests
from datetime import datetime

requests.packages.urllib3.disable_warnings()


__author__ = 'WOODONGGYU'
__copyrights__ = 'Copyright 2020 (C) WOODONGGYU. ALL RIGHTS RESERVED'
__credits__ = ''
__license__ = ''
__maintainer__ = 'WOODONGGYU'
__email__ = 'mrwoo92@naver.com'
__status__ = 'developing'
__version__ = '0.1'
__date__ = '2020-03-23'
__updated__ = ''


class MISP:
    """"""

    def __init__(self, server, apikey):
        self.server = server
        self.headers = {
            'Authorization': apikey,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def event(self, id=None):
        """Return events

        Arg:
            id (str): event_id or event_uuid

        Return:
            output[1] (list): list of event info
        """

        if id:
            url = self.server + '/events/{}'.format(id)
        else:
            url = self.server + '/events'

        output = self._get_request(url)
        if output[0]:
            return output[1]

    def attributes(self):
        """Return attributes"""

        url = self.server + '/attributes'
        output = self._get_request(url)
        if output[0]:
            return output[1]

    def attr_filter(self, attributes, filter, timefilter=None):
        """Return filtered attributes

        These method provides attribute filter
        The `filter` variable works by based on AND logical operator

        For example,
        When `filter` is {'category': 'Network activity', 'event_id': '6'},
        Returns the attributes with the `category` == `Network activity` and `event_id` == `6`

        When using `timefilter`, You must use a single dictionary key called timestamp
            ex) timefilter = {'timestamp': '['>', '=', '<'][date]'}

        Args:
            attributes (list): list of attribute
            filter (dict): key, value to filter
            timefilter (dict): timestamp to filter

        Return:
            _attributes (list): filtered attributes
        """

        for index, attr in enumerate(attributes):
            for key, value in filter.items():
                try:
                    if attr[key] != value:
                        attributes[index].clear()
                except KeyError:
                    pass
                except Exception as error:
                    print(error)
        # remove empty dict
        _attributes = [attr for attr in attributes if len(attr)]
        attributes = _attributes

        if timefilter:
            # split inequality, basetime
            ineq = timefilter['timestamp'][0]
            basetime = timefilter['timestamp'][1:]

            for index, attr in enumerate(attributes):
                attr_time = self._convert_time(int(attr['timestamp']))

                if ineq == '=':
                    if attr_time != basetime:
                        attributes[index].clear()
                elif ineq == '>':
                    if attr_time <= basetime:
                        attributes[index].clear()
                elif ineq == '<':
                    if attr_time >= basetime:
                        attributes[index].clear()
        # remove empty dict
        _attributes = [attr for attr in attributes if len(attr)]

        return _attributes

    def feed(self, id=None):
        """Fetch enabled feeds

        Arg:
            id (list): feed id

        Return:
             msg (list): result message
        """

        msg = list()

        # fetch specific enabled feeds
        if id:

            for index in id:
                url = self.server + '/feeds/fetchFromFeed/{}'.format(index)

                output = self._get_request(url)
                if output[0]:
                    msg.append(output[1])
                else:
                    msg.append(output[1])
        # fetch all enabled feeds
        else:
            url = self.server + '/feeds/fetchFromAllFeeds'

            output = self._get_request(url)
            if output[0]:
                msg.append(output[1])
        return msg

    def _get_request(self, url):
        """Request for GET method URL"""

        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()

    def _post_request(self, url, data):
        """Request for POST method URL"""

        response = requests.post(url, headers=self.headers, data=data, verify=False)
        if response.status_code == 200:
            return True, response.json()
        return False, response.json()

    def _convert_time(self, timestamp):
        """Returns convert timestamp to time"""

        d = datetime.fromtimestamp(timestamp)

        return d.strftime('%Y%m%d')


# example
if __name__ == '__main__':
    misp = MISP(
        server='',
        apikey=''
    )

    misp.feed(id=[50, 150])

    event = misp.event(id='5e61ae8e-e4f4-44f2-9d9f-476b7c769fdd')

    attr = misp.attributes()

    filter = {
        'category': 'Network activity',
        'event_id': '6',
        'to_ids': True
    }
    timefilter = {
        'timestamp': '=20200319'
    }
    misp.attr_filter(attr, filter=filter, timefilter=timefilter)
