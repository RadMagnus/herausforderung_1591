#!/usr/bin/python3

import argparse

# from crawlers.crawlerExample import CrawlerExample
from crawlers.crawlerRKICaseData import CrawlerRKICaseData
from crawlers.crawlerDemography1 import CrawlerDemography1
from crawlers.crawlerDensity import CrawlerDensity
from crawlers.crawlerDistancesLK import CrawlerDistancesLK


class MainCrawler:
    crawler_dict = [
        {
            'class':     CrawlerRKICaseData,
            'frequency': 'daily'
        },
        {
            'class':     CrawlerDemography1,
            'frequency': 'once'
        },
        {
            'class':     CrawlerDensity,
            'frequency': 'once'
        },
        {
            'class':     CrawlerDistancesLK,
            'frequency': 'once'
        },
    ]

    def __init__(self):
        pass

    def crawl(self, frequency=''):
        nr_crawlers = 0
        nr_errors = 0
        for crawler in self.crawler_dict:
            if frequency == '' or crawler['frequency'] == frequency:
                nr_crawlers += 1
                cc = crawler['class']()
                print('Running {}...'.format(cc.name))
                if cc.crawl():
                    print('Running {} done w/o errors'.format(cc.name))
                else:
                    print('{} stopped with errors'.format(cc.name))
                    nr_errors += 1

        if nr_crawlers == 0:
            print('No crawler to run')
        else:
            print('==========')
            print('{} crawlers ran. {} crawlers ran with errors'.format(nr_crawlers, nr_errors))

        return True if nr_errors == 0 else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl all (or specific) data sources. ' +
                                                 'Choose one of the corresponding flags.')
    parser.add_argument('-a', '--all', action='store_true',
                        help='crawl ALL data sources')
    parser.add_argument('-d', '--daily', action='store_true',
                        help='only crawl data sources that need to be updated daily')
    parser.add_argument('-o', '--once', action='store_true',
                        help='only crawl data sources that need to be accessed rarely or only once')
    args = parser.parse_args()

    mc = MainCrawler()
    if args.all:
        mc.crawl()
    elif args.daily:
        mc.crawl('daily')
    elif args.once:
        mc.crawl('once')
    else:
        parser.print_help()
