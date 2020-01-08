import requests
import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os
import random
from collections import Counter

from py2store import QuickJsonStore

root = os.path.expanduser('~/ddir/demonym_adjectives/')
demonym_url = 'http://www.geography-site.co.uk/pages/countries/demonyms.html'

newline_p = re.compile('\n|\r')
word_p = re.compile('[\w\-\s]+')

# the dflt_demonyms are the only 73 that yielded suggestions results at the time of writing this.
dflt_demonyms = ('afghan', 'albanian', 'american', 'australian', 'belgian', 'bhutanese', 'brazilian', 'british',
                 'bulgarian', 'burmese', 'cambodian', 'canadian', 'chinese', 'colombian', 'cuban', 'czech', 'dominican',
                 'egyptian', 'english', 'eritrean', 'ethiopian', 'filipino', 'finn', 'french', 'german', 'greek',
                 'haitian', 'hungarian', 'indian', 'indonesian', 'iranian', 'israeli', 'italian', 'jamaican',
                 'japanese', 'kenyan', 'lebanese', 'malagasy', 'malaysian', 'maltese', 'mongolian', 'moroccan',
                 'nepalese', 'nigerian', 'north korean', 'norwegian', 'pakistani', 'peruvian', 'pole', 'portuguese',
                 'puerto rican', 'romanian', 'russian', 'samoan', 'saudi', 'scottish', 'senegalese', 'serbian',
                 'singaporean', 'somali', 'south african', 'south korean', 'sri lankan', 'sudanese', 'swiss', 'syrian',
                 'taiwanese', 'thai', 'tongan', 'ukrainian', 'vietnamese', 'welsh', 'zambian')

suggestions_rootdir = os.path.join(root, 'so')

# The following is a mapping done by hand to clean up raw acquired data

replacements = {'Azerbaijani - also Azeri': 'Azerbaijani',
                'Barbadian or Bajuns': 'Barbadian',
                'Cape Verdian or Cape Verdean': 'Cape Verdian',
                'Equatorial Guinean or Equatoguinean': 'Equatorial Guinean',
                'Grenadian or Grenadan': 'Grenadian',
                'Irishman or Irishwoman or Irish ': 'Irish ',
                'Lao or Laotian': 'Laotian',
                'Monegasque or Monacan': 'Monegasque',
                'Burmese or Myanmarese': 'Burmese',
                'Netherlander  or Dutch ': 'Dutch ',
                'New Zealander or Kiwi': 'New Zealander',
                'Sammarinese or San Marinese': 'San Marinese',
                'Saudi or Saudi Arabian': 'Saudi',
                'Serbian or Montenegrin': 'Serbian',
                'Tajik or Tadzhik': 'Tajik',
                'Trinidadian or Tobagonian': 'Trinidadian',
                'Uzbek or Uzbekistani': 'Uzbek',
                'Yemeni or Yemenite': 'Yemeni'}
replace = lambda x: replacements.get(x, x)


def _get_complicated_demonyms(demonyms):
    """Function to extract 'complicated' demonyms (to be able to then map them to simpler forms later.
    Namely, this is what was used to create the 'replacements' mapping above.
    """
    return list(filter(re.compile('\ or\ |\ \-\ |\ also\ ').findall, demonyms))


def mk_demonym_df_from_source():
    """
    Slurp the contents of the url containing the demonyms and create a dataframe with this information.

    Returns:

    """
    t = BeautifulSoup(requests.get(demonym_url).content)
    tt = t.find_all('table')
    tt = tt[-1]
    tt = tt.find_all('tr')

    df = list()
    for s in tt:
        s = s.text
        ss = list(filter(lambda x: len(x) > 1, newline_p.split(s)))
        if ss:
            df.append(ss)
    df = pd.DataFrame(df[1:], columns=list(map(str.lower, df[0])))
    df['demonym'] = list(map(lambda x: word_p.match(x).group(0).strip(), df.demonym))
    df['demonym'] = list(map(replace, df.demonym))
    return df


# Auto-suggest slurping #####################

p_filename_chars = re.compile('[^\w\-]')


def filename_of_demonym(demonym):
    t = demonym.strip().lower()
    t = p_filename_chars.sub('_', t)
    return f"{t}.json"


def google_auto_suggestions_response(q, user_agent='Chrome/79.0.3945.88',
                                     url_prefix='http://suggestqueries.google.com/complete/search?client=chrome&q='):
    url = f"{url_prefix}{q}"
    headers = {'User-agent': user_agent}
    return requests.get(url, headers=headers)


def google_auto_suggestions(q, user_agent='Chrome/79.0.3945.88',
                            url_prefix='http://suggestqueries.google.com/complete/search?client=chrome&q='):
    response = None
    try:
        response = google_auto_suggestions_response(q, user_agent, url_prefix)
        result = json.loads(response.content.decode('utf-8'))
        return result[1]
    except Exception as e:
        print(f"{e}")
        print("Returning raw response")
        return response


query_format_1 = "why are the {demonym} so "  # space after the "so" is important!
query_format_2 = "why are the {demonym} "  # more hits than so, but many not targeted to PEOPLE
query_format_3 = "why are {demonym} so "  # more hits than so, but many not targeted to PEOPLE

query_format = query_format_1


def demonym_adjectives_response(demonym):
    return google_auto_suggestions_response(q=query_format.format(demonym=demonym))


def demonym_adjectives_json(demonym):
    response = demonym_adjectives_response(demonym)
    return json.loads(response.content.decode('utf-8'))


def demonym_adjectives(demonym):
    return google_auto_suggestions(q=query_format.format(demonym=demonym))


def acquire_auto_suggestions(demonyms=dflt_demonyms):
    print(f"------ Acquiring suggestions for {len(demonyms)} demonyms --------")
    s = QuickJsonStore(suggestions_rootdir)

    for i, demonym in enumerate(demonyms):
        print(f"{i}: {demonym}")
        s[demonym] = demonym_adjectives_json(demonym)
        time.sleep(0.5 + 1.5 * random.random())


def suggestions_df():
    s = QuickJsonStore(suggestions_rootdir)
    if len(s) == 0:
        acquire_auto_suggestions()

    sdf = list()
    for demonym, r in s.items():
        suggestions = r[1]
        if len(suggestions) > 0:
            relevances = r[-1].get('google:suggestrelevance', [])
            assert len(suggestions) == len(relevances)
            sdf.extend(
                [{'demonym': demonym, 'suggestion': t, 'relevance': tt} for t, tt in zip(suggestions, relevances)])
    sdf = pd.DataFrame(sdf)
    sdf['demonym'] = list(map(str.lower, sdf['demonym']))

    prefix_templates_1 = 'why are the {demonym}'
    prefix_templates_2 = 'why are the {demonym}|why are {demonym}'
    prefix_templates_3 = 'why are the {demonym}|why are {demonym}|why {demonym}'

    def remove_query_prefix(demonym, query, prefix_template=prefix_templates_3):
        demonym = demonym.lower()
        t = re.sub(prefix_template.format(demonym=demonym), '', query)
        return t

    sdf['characteristic'] = list(map(lambda x: remove_query_prefix(*x), zip(sdf.demonym, sdf.suggestion)))
    lidx = list(map(lambda x: x[0] != x[1], zip(sdf.characteristic, sdf.suggestion)))
    sdff = sdf.iloc[lidx].reset_index(drop=True)
    # print(sdff.shape)

    so_p = re.compile('so\ ')

    def post_process_characteristics(t):
        t = t.strip()
        if t.startswith('s '):
            t = t[len('s '):]
        t = so_p.sub('', t)
        return t

    sdff['characteristic'] = [post_process_characteristics(t) for t in sdff['characteristic']]
    sdff = sdff.sort_values(by=['demonym', 'relevance'], ascending=[True, False]).reset_index(drop=True)
    return sdff


def mk_and_save_xls_of_demonym_stats(xls_file='what_we_think_about_demonyns.xlsx', sdff=None):
    if sdff is None:
        sdff = suggestions_df()

    xls_writer = pd.ExcelWriter(xls_file, engine='xlsxwriter')

    def write_sr_to_sheet(sr, index_name='demonym', val_name='count', sheet_name=None):
        sr.index.name = index_name
        sr.name = val_name
        sheet_name = sheet_name or f"{index_name}_{val_name}"
        sr.reset_index().to_excel(xls_writer, sheet_name=sheet_name, index=False)

    # Who do we talk/ask about?
    demonym_count = pd.Series(Counter(sdff.demonym)).sort_values(ascending=False)
    write_sr_to_sheet(demonym_count, index_name='demonym', val_name='count')
    print(f"{len(demonym_count)} 'demonyms' covered")

    # What words do we use to talk/ask about them?
    feature_count = pd.Series(Counter(sdff['characteristic'])).sort_values(ascending=False)
    write_sr_to_sheet(feature_count, index_name='characteristic', val_name='count')
    print(f"The data shows that people use a set of {len(feature_count)}",
          "words or expressions when asking google why such and such is so...")

    def whois(characteristic):
        return list(sdff[sdff['characteristic'] == characteristic]['demonym'])

    # Who is what?
    whois_sr = dict()
    for characteristic in feature_count.index.values:
        whois_sr[characteristic] = ', '.join(whois(characteristic))
    whois_sr = pd.Series(whois_sr)
    write_sr_to_sheet(whois_sr, index_name='characteristic', val_name='demonyms')

    # for characteristic, demonyms in whois_sr.head(12).items():
    #     print(f"{characteristic:<15}: {demonyms}")

    # Top what about each who
    t = sdff[['demonym', 'characteristic']].groupby('demonym').apply(lambda x: x.iloc[0])['characteristic']
    write_sr_to_sheet(t, index_name='demonym', val_name='top characteristic')

    xls_writer.save()


if __name__ == '__main__':
    mk_and_save_xls_of_demonym_stats()