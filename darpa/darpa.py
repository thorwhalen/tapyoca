import pandas as pd
from bs4 import BeautifulSoup
from glom import Spec
from dateutil.parser import parse as dateutil_parse
import re
from i2.util import inject_method
from py2misc.py2request.py2request import Py2Request, UrlMethodSpecsMaker
from functools import lru_cache


def parse_tag_list_page(response):
    t = BeautifulSoup(response.content, features="lxml")
    tt = t.find('div', {'id': 'sidr'})
    tag_of_tag_id = {ttt.text: ttt.find('a').get('href') for ttt in tt.find_all('li')}
    tag_of_tag_id = {k: int(v[len('/tag-list?tt='):]) for k, v in tag_of_tag_id.items()}
    tag_of_tag_id = pd.Series(tag_of_tag_id)
    return tag_of_tag_id


def listings_from_html(html):
    def mk_extractor_for(k):
        def extractor(x):
            t = x.find(name='div' if k != 'link' else 'h2',
                       attrs={'class': f'listing__{k}'})
            if t is not None:
                return t.text
            else:
                return t

        extractor.__name__ = f"{k}_extractor"
        return extractor

    def tags_extractor(x):
        return [t.text for t in x.find_all(name='a', attrs={'class': 'listing__tag-item'})]

    spec = {a: mk_extractor_for(a) for a in ['date', 'link', 'position', 'office', 'copy']}
    spec['tags'] = tags_extractor

    extractor = Spec(spec).glom

    t = BeautifulSoup(html, features="lxml")
    tt = t.find('section', {'id': 'content'})
    if tt is not None:
        w = tt.find_all('tr')

        def listings_info_gen(w):
            for ww in w:
                yield extractor(ww)

        yield from listings_info_gen(w)


def listings_from_response(response):
    yield from listings_from_html(response.content)


listings_um = UrlMethodSpecsMaker(url_root='https://www.darpa.mil/', output_trans=listings_from_response)

method_specs = {
    'tag_list': {
        'url': 'https://www.darpa.mil/tag-list',
        'output_trans': parse_tag_list_page,
        'method_wrap': lru_cache(maxsize=1)
    },
    'opportunities': listings_um(route='work-with-us/opportunities', PP='page_num'),
    'listings_for_tag_id': listings_um(route='tag-list', tt='tag_id', PP='page_num'),
}
dacc = Py2Request(method_specs)


def all_opportunities(dacc, max_n_pages=20):
    for page_num in range(max_n_pages):
        yield from dacc.opportunities(page_num)


def all_tag_listings(dacc, tag_id, max_n_pages=99):
    for page_num in range(max_n_pages):
        yield from dacc.listings_for_tag_id(tag_id, page_num)


inject_method(dacc, all_opportunities)
inject_method(dacc, all_tag_listings)

########################################################################################################################
# Data postprocess utils

date_re = re.compile('\d{1,2}/\d{1,2}/\d{4}')


def parse_date(s: str):
    if isinstance(s, str):
        m = date_re.search(s)
        if m:
            return dateutil_parse(m.group(0), dayfirst=False, yearfirst=False)
    return s  # return the string as is if you can't find a date!


def transform_dates_to_datetime(a):
    for x in a:
        if 'date' in x:
            yield dict(x, date=parse_date(x['date']))

# tag_list_url = 'https://www.darpa.mil/tag-list'
# current_listings_url = 'https://www.darpa.mil/work-with-us/opportunities?'
# listing_for_tag_id_format = tag_list_url + '?tt={tag_id}&'
#
#
# def get_tags_and_tag_ids():
#     parse_tag_list_page(requests.get('https://www.darpa.mil/tag-list'))
#
#
# def listings_from_all_pages(max_n_pages=20, prefix_url=current_listings_url):
#     for page_num in range(max_n_pages):
#         yield from listings_from_page(page_num, prefix_url)
#
#
# all_current_listings = partial(listings_from_all_pages,
#                                max_n_pages=20,
#                                prefix_url=current_listings_url)
#
#
# def all_listings_for_tag_id(tag_id):
#     url = listing_for_tag_id_format.format(tag_id=tag_id)
#     return listings_from_all_pages(max_n_pages=99, prefix_url=url)
#
#
# def listings_from_page(page_num=0, prefix_url=current_listings_url):
#     url = f'{prefix_url}PP={page_num}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         return list(listings_from_html(response.content))
#     else:
#         error_dump_file = 'debug_dump.p'
#         pickle.dump(response, open(error_dump_file, 'wb'))
#         raise ValueError('Oops, I got response.status != 200. Dumping the response to {error_dump_file}')
#
#
# def tag_item_triples_df(tag_item_triples):
#     """Deprecated"""
#     import pandas as pd
#
#     t = pd.Series(tag_item_triples)
#     t = t.reset_index()
#     t.columns = ['tag', 'href', 'long_name', 'count']
#     t = t.set_index('tag').sort_values('count', ascending=False)
#     return t
