"""
Info about CMUdict: http://www.speech.cs.cmu.edu/cgi-bin/cmudict

Note: You may want to use cmudict instead (pip install cmudict -- https://github.com/prosegrinder/python-cmudict)
(Unless you want to parse the raw data yourself, in which case...)

Github where you can download the raw data: https://github.com/Alexir/CMUdict

Download raw data here:
https://github.com/Alexir/CMUdict/blob/master/cmudict-0.7b
or
http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict

Find an error? Please contact the maintainers! We will check it out. (See at bottom for contact information.)
Note: If you are looking for a dictionary for use with a speech recognizer,
this dictionary is not the one that you are looking for.
For that purpose, see http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/sphinxdict or use this tool.

The current phoneme set has 39 phonemes, not counting varia due to lexical stress.
This phoneme (or more accurately, phone) set is based on the ARPAbet symbol set developed for speech recognition uses.
You can find a description of the [ARPAbet on Wikipedia](https://en.wikipedia.org/wiki/ARPABET),
as well information on how it relates to the standard IPA symbol set.
"""

import os

url = 'https://github.com/Alexir/CMUdict/raw/master/cmudict-0.7b'


def fetch_zip_and_save(save_to_dir,
                       zip_filename='cmudict_raw_data.zip',
                       inner_zipfilename='decode_me_with_latin1.txt'):
    import requests

    r = requests.get(url)
    if r.status_code == 200:
        from py2store.slib.s_zipfile import ZipStore
        save_zipfilepath = os.path.join(save_to_dir, zip_filename)
        ZipStore(save_zipfilepath)[inner_zipfilename] = r.content
    else:
        raise ValueError(
            f"response status code was {r.status_code} and content {r.content}")
