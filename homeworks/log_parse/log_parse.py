# -*- encoding: utf-8 -*-
import re
from datetime import datetime


def parse(
        ignore_files: bool=False,
        ignore_urls: list=[],
        start_at: str=None,
        stop_at: str=None,
        request_type: str=None,
        ignore_www: bool=False,
        slow_queries: bool=False
) -> list:
    with open('log.log', 'r') as log:
        reg = r'\[(?P<timestamp>[^\]]+)\] \"(?P<request>[^\"]+)\" (?P<status>\d+) (?P<bytes>\d+).*$'
        stats = dict()

        for line in log.readlines():
            matches = re.match(reg, line)

            if matches:
                date_raw, url_info, code, time = matches.groups()
                type, request, version = url_info.split(' ')
                url = clean_url(request, ignore_www)
                date = datetime.strptime(date_raw, '%d/%b/%Y %H:%M:%S')

                if start_at and date <= date.strptime(start_at, '%d.%m.%Y %H:%M'):
                    continue
                if stop_at and date >= date.strptime(stop_at, '%d.%m.%Y %H:%M'):
                    continue
                if url in ignore_urls:
                    continue
                if request_type and type != request:
                    continue

                if stats.get(url):
                    stats[url]['count'] += 1
                    stats[url]['time'] += int(time)
                else:
                    stats[url] = {
                        'count': 1,
                        'request_type': request_type,
                        'time': int(time)
                    }

    if slow_queries:
        sorted_results = sorted(stats.items(), key=lambda t: t[1]['time'], reverse=True)[:5]
        times = map(lambda result: int(result[1]['time'] / result[1]['count']), sorted_results)
        sorted_times = list(sorted(times, key=lambda t: -t))
        return sorted_times

    elif ignore_files:
        filtered = list(filter(lambda item: '.' not in item[0].split('/')[-1], stats.items()))
        sorted_results = sorted(filtered, key=lambda t: t[1]['count'], reverse=True)[:5]
        counts = list(map(lambda result: result[1]['count'], sorted_results))
        return counts
    else:
        sorted_results = sorted(stats.items(), key=lambda t: t[1]['count'], reverse=True)[:5]
        counts = list(map(lambda result: result[1]['count'], sorted_results))
        return counts


def clean_url(url: str, ignore_www: bool):
    url = url.split('://')[1]

    if '#' in url:
        url = url.split('#')[0]
    if '?' in url:
        url = url.split('?')[0]

    if ignore_www and url.startswith('www'):
        url = url.replace('www.', '')

    return url