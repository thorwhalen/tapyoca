
# Bar Chart Races (applied to covid-19 spread)

The module will show is how to make these:
- Confirmed cases (by country): https://public.flourish.studio/visualisation/1704821/
- Deaths (by country): https://public.flourish.studio/visualisation/1705644/
- US Confirmed cases (by state): https://public.flourish.studio/visualisation/1794768/
- US Deaths (by state): https://public.flourish.studio/visualisation/1794797/

## The script

If you just want to run this as a script to get the job done, you have one here: 
https://raw.githubusercontent.com/thorwhalen/tapyoca/master/covid/covid_bar_chart_race.py

Run like this
```
$ python covid_bar_chart_race.py -h
usage: covid_bar_chart_race.py [-h] {mk-and-save-covid-data,update-covid-data,instructions-to-make-bar-chart-race} ...

positional arguments:
  {mk-and-save-covid-data,update-covid-data,instructions-to-make-bar-chart-race}
    mk-and-save-covid-data
                        :param data_sources: Dirpath or py2store Store where the data is :param kinds: The kinds of data you want to compute and save :param
                        skip_first_days: :param verbose: :return:
    update-covid-data   update the coronavirus data
    instructions-to-make-bar-chart-race

optional arguments:
  -h, --help            show this help message and exit
 ```
 
 
## The jupyter notebook

The notebook (the .ipynb file) shows you how to do it step by step in case you want to reuse the methods for other stuff.



# Getting and preparing the data

Corona virus data here: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset (direct download: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset/download). It's currently updated daily, so download a fresh copy if you want.

Population data here: http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv

It comes under the form of a zip file (currently named `novel-corona-virus-2019-dataset.zip` with several `.csv` files in them. We use `py2store` (To install: `pip install py2store`. Project lives here: https://github.com/i2mint/py2store) to access and pre-prepare it. It allows us to not have to unzip the file and replace the older folder with it every time we download a new one. It also gives us the csvs as `pandas.DataFrame` already. 


```python
import pandas as pd
from io import BytesIO
from py2store import kv_wrap, ZipReader  # google it and pip install it
from py2store.caching import mk_cached_store
from py2store import QuickPickleStore
from py2store.sources import FuncReader

def country_flag_image_url():
    import pandas as pd
    return pd.read_csv(
        'https://raw.githubusercontent.com/i2mint/examples/master/data/country_flag_image_url.csv')

def kaggle_coronavirus_dataset():
    import kaggle
    from io import BytesIO
    # didn't find the pure binary download function, so using temp dir to emulate
    from tempfile import mkdtemp  
    download_dir = mkdtemp()
    filename = 'novel-corona-virus-2019-dataset.zip'
    zip_file = os.path.join(download_dir, filename)
    
    dataset = 'sudalairajkumar/novel-corona-virus-2019-dataset'
    kaggle.api.dataset_download_files(dataset, download_dir)
    with open(zip_file, 'rb') as fp:
        b = fp.read()
    return BytesIO(b)

def city_population_in_time():
    import pandas as pd
    return pd.read_csv(
        'https://gist.githubusercontent.com/johnburnmurdoch/'
        '4199dbe55095c3e13de8d5b2e5e5307a/raw/fa018b25c24b7b5f47fd0568937ff6c04e384786/city_populations'
    )

def country_flag_image_url_prep(df: pd.DataFrame):
    # delete the region col (we don't need it)
    del df['region']
    # rewriting a few (not all) of the country names to match those found in kaggle covid data
    # Note: The list is not complete! Add to it as needed
    old_and_new = [('USA', 'US'), 
                   ('Iran, Islamic Rep.', 'Iran'), 
                   ('UK', 'United Kingdom'), 
                   ('Korea, Rep.', 'Korea, South')]
    for old, new in old_and_new:
        df['country'] = df['country'].replace(old, new)

    return df


@kv_wrap.outcoming_vals(lambda x: pd.read_csv(BytesIO(x)))  # this is to format the data as a dataframe
class ZippedCsvs(ZipReader):
    pass
# equivalent to ZippedCsvs = kv_wrap.outcoming_vals(lambda x: pd.read_csv(BytesIO(x)))(ZipReader)
```


```python
# Enter here the place you want to cache your data
my_local_cache = os.path.expanduser('~/ddir/my_sources')
```


```python
CachedFuncReader = mk_cached_store(FuncReader, QuickPickleStore(my_local_cache))
```


```python
data_sources = CachedFuncReader([country_flag_image_url, 
                                 kaggle_coronavirus_dataset, 
                                 city_population_in_time])
list(data_sources)
```




    ['country_flag_image_url',
     'kaggle_coronavirus_dataset',
     'city_population_in_time']




```python
covid_datasets = ZippedCsvs(data_sources['kaggle_coronavirus_dataset'])
list(covid_datasets)
```




    ['COVID19_line_list_data.csv',
     'COVID19_open_line_list.csv',
     'covid_19_data.csv',
     'time_series_covid_19_confirmed.csv',
     'time_series_covid_19_confirmed_US.csv',
     'time_series_covid_19_deaths.csv',
     'time_series_covid_19_deaths_US.csv',
     'time_series_covid_19_recovered.csv']




```python
covid_datasets['time_series_covid_19_confirmed.csv'].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Province/State</th>
      <th>Country/Region</th>
      <th>Lat</th>
      <th>Long</th>
      <th>1/22/20</th>
      <th>1/23/20</th>
      <th>1/24/20</th>
      <th>1/25/20</th>
      <th>1/26/20</th>
      <th>1/27/20</th>
      <th>...</th>
      <th>3/24/20</th>
      <th>3/25/20</th>
      <th>3/26/20</th>
      <th>3/27/20</th>
      <th>3/28/20</th>
      <th>3/29/20</th>
      <th>3/30/20</th>
      <th>3/31/20</th>
      <th>4/1/20</th>
      <th>4/2/20</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td>Afghanistan</td>
      <td>33.0000</td>
      <td>65.0000</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>74</td>
      <td>84</td>
      <td>94</td>
      <td>110</td>
      <td>110</td>
      <td>120</td>
      <td>170</td>
      <td>174</td>
      <td>237</td>
      <td>273</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td>Albania</td>
      <td>41.1533</td>
      <td>20.1683</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>123</td>
      <td>146</td>
      <td>174</td>
      <td>186</td>
      <td>197</td>
      <td>212</td>
      <td>223</td>
      <td>243</td>
      <td>259</td>
      <td>277</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td>Algeria</td>
      <td>28.0339</td>
      <td>1.6596</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>264</td>
      <td>302</td>
      <td>367</td>
      <td>409</td>
      <td>454</td>
      <td>511</td>
      <td>584</td>
      <td>716</td>
      <td>847</td>
      <td>986</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>Andorra</td>
      <td>42.5063</td>
      <td>1.5218</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>164</td>
      <td>188</td>
      <td>224</td>
      <td>267</td>
      <td>308</td>
      <td>334</td>
      <td>370</td>
      <td>376</td>
      <td>390</td>
      <td>428</td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td>Angola</td>
      <td>-11.2027</td>
      <td>17.8739</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>3</td>
      <td>3</td>
      <td>4</td>
      <td>4</td>
      <td>5</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>8</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 76 columns</p>
</div>




```python
country_flag_image_url = data_sources['country_flag_image_url']
country_flag_image_url.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>region</th>
      <th>flag_image_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Angola</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/ao/flat/64.png</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Burundi</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bi/flat/64.png</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Benin</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bj/flat/64.png</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Burkina Faso</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bf/flat/64.png</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Botswana</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bw/flat/64.png</td>
    </tr>
  </tbody>
</table>
</div>




```python
from IPython.display import Image
flag_image_url_of_country = country_flag_image_url.set_index('country')['flag_image_url']
Image(url=flag_image_url_of_country['Australia'])
```




<img src="https://www.countryflags.io/au/flat/64.png"/>



## Update coronavirus data


```python
# To update the coronavirus data:
def update_covid_data(data_sources):
    """update the coronavirus data"""
    if 'kaggle_coronavirus_dataset' in data_sources._caching_store:
        del data_sources._caching_store['kaggle_coronavirus_dataset']  # delete the cached item
    _ = data_sources['kaggle_coronavirus_dataset']

# update_covid_data(data_sources)  # uncomment here when you want to update
```

## Prepare data for flourish upload


```python
import re

def print_if_verbose(verbose, *args, **kwargs):
    if verbose:
        print(*args, **kwargs)
        
def country_data_for_data_kind(data_sources, kind='confirmed', skip_first_days=0, verbose=False):
    """kind can be 'confirmed', 'deaths', 'confirmed_US', 'confirmed_US', 'recovered'"""
    
    covid_datasets = ZippedCsvs(data_sources['kaggle_coronavirus_dataset'])
    
    df = covid_datasets[f'time_series_covid_19_{kind}.csv']
    # df = s['time_series_covid_19_deaths.csv']
    if 'Province/State' in df.columns:
        df.loc[df['Province/State'].isna(), 'Province/State'] = 'n/a'  # to avoid problems arising from NaNs

    print_if_verbose(verbose, f"Before data shape: {df.shape}")

    # drop some columns we don't need
    p = re.compile('\d+/\d+/\d+')

    assert all(isinstance(x, str) for x in df.columns)
    date_cols = [x for x in df.columns if p.match(x)]
    if not kind.endswith('US'):
        df = df.loc[:, ['Country/Region'] + date_cols]
        # group countries and sum up the contributions of their states/regions/pargs
        df['country'] = df.pop('Country/Region')
        df = df.groupby('country').sum()
    else:
        df = df.loc[:, ['Province_State'] + date_cols]
        df['state'] = df.pop('Province_State')
        df = df.groupby('state').sum()

    
    print_if_verbose(verbose, f"After data shape: {df.shape}")
    df = df.iloc[:, skip_first_days:]
    
    if not kind.endswith('US'):
        # Joining with the country image urls and saving as an xls
        country_image_url = country_flag_image_url_prep(data_sources['country_flag_image_url'])
        t = df.copy()
        t.columns = [str(x)[:10] for x in t.columns]
        t = t.reset_index(drop=False)
        t = country_image_url.merge(t, how='outer')
        t = t.set_index('country')
        df = t
    else:    
        pass

    return df


def mk_and_save_country_data_for_data_kind(data_sources, kind='confirmed', skip_first_days=0, verbose=False):
    t = country_data_for_data_kind(data_sources, kind, skip_first_days, verbose)
    filepath = f'country_covid_{kind}.xlsx'
    t.to_excel(filepath)
    print_if_verbose(verbose, f"Was saved here: {filepath}")

```


```python
# for kind in ['confirmed', 'deaths', 'recovered', 'confirmed_US', 'deaths_US']:
for kind in ['confirmed', 'deaths', 'recovered', 'confirmed_US', 'deaths_US']:
    mk_and_save_country_data_for_data_kind(data_sources, kind=kind, skip_first_days=39, verbose=True)
```

    Before data shape: (262, 79)
    After data shape: (183, 75)
    Was saved here: country_covid_confirmed.xlsx
    Before data shape: (262, 79)
    After data shape: (183, 75)
    Was saved here: country_covid_deaths.xlsx
    Before data shape: (248, 79)
    After data shape: (183, 75)
    Was saved here: country_covid_recovered.xlsx
    Before data shape: (3253, 86)
    After data shape: (58, 75)
    Was saved here: country_covid_confirmed_US.xlsx
    Before data shape: (3253, 87)
    After data shape: (58, 75)
    Was saved here: country_covid_deaths_US.xlsx


## Upload to Flourish, tune, and publish

Go to https://public.flourish.studio/, get a free account, and play.

Got to https://app.flourish.studio/templates

Choose "Bar chart race". At the time of writing this, it was here: https://app.flourish.studio/visualisation/1706060/

... and then play with the settings


# Discussion of the methods


```python
from py2store import *
from IPython.display import Image
```

## country flags images

The manual data prep looks something like this.


```python
import pandas as pd

# get the csv data from the url
country_image_url_source = \
    'https://raw.githubusercontent.com/i2mint/examples/master/data/country_flag_image_url.csv'
country_image_url = pd.read_csv(country_image_url_source)

# delete the region col (we don't need it)
del country_image_url['region']

# rewriting a few (not all) of the country names to match those found in kaggle covid data
# Note: The list is not complete! Add to it as needed
# TODO: (Wishful) Using a general smart soft-matching algorithm to do this automatically.
# TODO:    This could use edit-distance, synonyms, acronym generation, etc.
old_and_new = [('USA', 'US'), 
               ('Iran, Islamic Rep.', 'Iran'), 
               ('UK', 'United Kingdom'), 
               ('Korea, Rep.', 'Korea, South')]
for old, new in old_and_new:
    country_image_url['country'] = country_image_url['country'].replace(old, new)

image_url_of_country = country_image_url.set_index('country')['flag_image_url']

country_image_url.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>flag_image_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Angola</td>
      <td>https://www.countryflags.io/ao/flat/64.png</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Burundi</td>
      <td>https://www.countryflags.io/bi/flat/64.png</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Benin</td>
      <td>https://www.countryflags.io/bj/flat/64.png</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Burkina Faso</td>
      <td>https://www.countryflags.io/bf/flat/64.png</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Botswana</td>
      <td>https://www.countryflags.io/bw/flat/64.png</td>
    </tr>
  </tbody>
</table>
</div>




```python
Image(url=image_url_of_country['Australia'])
```




<img src="https://www.countryflags.io/au/flat/64.png"/>



## Caching the flag images data

Downloading our data sources every time we need them is not sustainable. What if they're big? What if you're offline or have slow internet (yes, dear future reader, even in the US, during coronavirus times!)?

Caching. A "cache aside" read-cache. That's the word. py2store has tools for that (most of which are are caching.py). 

So let's say we're going to have a local folder where we'll store various datas we download. The principle is as follows:


```python
from py2store.caching import mk_cached_store

class TheSource(dict): ...
the_cache = {}
TheCacheSource = mk_cached_store(TheSource, the_cache)

the_source = TheSource({'green': 'eggs', 'and': 'ham'})

the_cached_source = TheCacheSource(the_source)
print(f"the_cache: {the_cache}")
print(f"Getting green...")
the_cached_source['green']
print(f"the_cache: {the_cache}")
print("... so the next time the_cached_source will get it's green from that the_cache")
```

    the_cache: {}
    Getting green...
    the_cache: {'green': 'eggs'}
    ... so the next time the_cached_source will get it's green from that the_cache


But now, you'll notice a slight problem ahead. What exactly does our source store (or rather reader) looks like? In it's raw form it would take urls as it's keys, and the response of a request as it's value. That store wouldn't have an `__iter__` for sure (unless you're Google). But more to the point here, the `mk_cached_store` tool uses the same key for the source and the cache, and we can't just use the url as is, to be a local file path. 

There's many ways we could solve this. One way is to add a key map layer on the cache store, so externally, it speaks the url key language, but internally it will map that url to a valid local file path. We've been there, we got the T-shirt!

But what we're going to do is a bit different: We're going to do the key mapping in the source store itself. It seems to make more sense in our context: We have a data source of `name: data` pairs, and if we impose that the name should be a valid file name, we don't need to have a key map in the cache store.

So let's start by building this `MyDataStore` store. We'll start by defining the functions that get us the data we want. 


```python
def country_flag_image_url():
    import pandas as pd
    return pd.read_csv(
        'https://raw.githubusercontent.com/i2mint/examples/master/data/country_flag_image_url.csv')

def kaggle_coronavirus_dataset():
    import kaggle
    from io import BytesIO
    # didn't find the pure binary download function, so using temp dir to emulate
    from tempfile import mkdtemp  
    download_dir = mkdtemp()
    filename = 'novel-corona-virus-2019-dataset.zip'
    zip_file = os.path.join(download_dir, filename)
    
    dataset = 'sudalairajkumar/novel-corona-virus-2019-dataset'
    kaggle.api.dataset_download_files(dataset, download_dir)
    with open(zip_file, 'rb') as fp:
        b = fp.read()
    return BytesIO(b)

def city_population_in_time():
    import pandas as pd
    return pd.read_csv(
        'https://gist.githubusercontent.com/johnburnmurdoch/'
        '4199dbe55095c3e13de8d5b2e5e5307a/raw/fa018b25c24b7b5f47fd0568937ff6c04e384786/city_populations'
    )
```

Now we can make a store that simply uses these function names as the keys, and their returned value as the values.


```python
from py2store.base import KvReader
from functools import lru_cache

class FuncReader(KvReader):
    _getitem_cache_size = 999
    def __init__(self, funcs):
        # TODO: assert no free arguments (arguments are allowed but must all have defaults)
        self.funcs = funcs
        self._func_of_name = {func.__name__: func for func in funcs}

    def __contains__(self, k):
        return k in self._func_of_name
    
    def __iter__(self):
        yield from self._func_of_name
        
    def __len__(self):
        return len(self._func_of_name)

    @lru_cache(maxsize=_getitem_cache_size)
    def __getitem__(self, k):
        return self._func_of_name[k]()  # call the func
    
    def __hash__(self):
        return 1
    
```


```python
data_sources = FuncReader([country_flag_image_url, kaggle_coronavirus_dataset, city_population_in_time])
list(data_sources)
```




    ['country_flag_image_url',
     'kaggle_coronavirus_dataset',
     'city_population_in_time']




```python
data_sources['country_flag_image_url']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>region</th>
      <th>flag_image_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Angola</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/ao/flat/64.png</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Burundi</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bi/flat/64.png</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Benin</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bj/flat/64.png</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Burkina Faso</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bf/flat/64.png</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Botswana</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bw/flat/64.png</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>210</th>
      <td>Solomon Islands</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/sb/flat/64.png</td>
    </tr>
    <tr>
      <th>211</th>
      <td>Tonga</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/to/flat/64.png</td>
    </tr>
    <tr>
      <th>212</th>
      <td>Tuvalu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/tv/flat/64.png</td>
    </tr>
    <tr>
      <th>213</th>
      <td>Vanuatu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/vu/flat/64.png</td>
    </tr>
    <tr>
      <th>214</th>
      <td>Samoa</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/ws/flat/64.png</td>
    </tr>
  </tbody>
</table>
<p>215 rows × 3 columns</p>
</div>




```python
data_sources['country_flag_image_url']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>region</th>
      <th>flag_image_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Angola</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/ao/flat/64.png</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Burundi</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bi/flat/64.png</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Benin</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bj/flat/64.png</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Burkina Faso</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bf/flat/64.png</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Botswana</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bw/flat/64.png</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>210</th>
      <td>Solomon Islands</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/sb/flat/64.png</td>
    </tr>
    <tr>
      <th>211</th>
      <td>Tonga</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/to/flat/64.png</td>
    </tr>
    <tr>
      <th>212</th>
      <td>Tuvalu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/tv/flat/64.png</td>
    </tr>
    <tr>
      <th>213</th>
      <td>Vanuatu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/vu/flat/64.png</td>
    </tr>
    <tr>
      <th>214</th>
      <td>Samoa</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/ws/flat/64.png</td>
    </tr>
  </tbody>
</table>
<p>215 rows × 3 columns</p>
</div>




```python
data_sources['city_population_in_time']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>group</th>
      <th>year</th>
      <th>value</th>
      <th>subGroup</th>
      <th>city_id</th>
      <th>lastValue</th>
      <th>lat</th>
      <th>lon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Agra</td>
      <td>India</td>
      <td>1575</td>
      <td>200.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>200.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Agra</td>
      <td>India</td>
      <td>1576</td>
      <td>212.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>200.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Agra</td>
      <td>India</td>
      <td>1577</td>
      <td>224.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>212.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Agra</td>
      <td>India</td>
      <td>1578</td>
      <td>236.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>224.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Agra</td>
      <td>India</td>
      <td>1579</td>
      <td>248.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>236.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6247</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1561</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6248</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1562</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6249</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1563</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6250</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1564</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6251</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1565</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
  </tbody>
</table>
<p>6252 rows × 9 columns</p>
</div>



But we wanted this all to be cached locally, right? So a few more lines to do that!


```python
from py2store.caching import mk_cached_store
from py2store import QuickPickleStore
    
my_local_cache = os.path.expanduser('~/ddir/my_sources')

CachedFuncReader = mk_cached_store(FuncReader, QuickPickleStore(my_local_cache))
```


```python
data_sources = CachedFuncReader([country_flag_image_url, kaggle_coronavirus_dataset, city_population_in_time])
list(data_sources)
```




    ['country_flag_image_url',
     'kaggle_coronavirus_dataset',
     'city_population_in_time']




```python
data_sources['country_flag_image_url']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>country</th>
      <th>region</th>
      <th>flag_image_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Angola</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/ao/flat/64.png</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Burundi</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bi/flat/64.png</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Benin</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bj/flat/64.png</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Burkina Faso</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bf/flat/64.png</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Botswana</td>
      <td>Africa</td>
      <td>https://www.countryflags.io/bw/flat/64.png</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>210</th>
      <td>Solomon Islands</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/sb/flat/64.png</td>
    </tr>
    <tr>
      <th>211</th>
      <td>Tonga</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/to/flat/64.png</td>
    </tr>
    <tr>
      <th>212</th>
      <td>Tuvalu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/tv/flat/64.png</td>
    </tr>
    <tr>
      <th>213</th>
      <td>Vanuatu</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/vu/flat/64.png</td>
    </tr>
    <tr>
      <th>214</th>
      <td>Samoa</td>
      <td>Oceania</td>
      <td>https://www.countryflags.io/ws/flat/64.png</td>
    </tr>
  </tbody>
</table>
<p>215 rows × 3 columns</p>
</div>




```python
data_sources['city_population_in_time']
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>group</th>
      <th>year</th>
      <th>value</th>
      <th>subGroup</th>
      <th>city_id</th>
      <th>lastValue</th>
      <th>lat</th>
      <th>lon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Agra</td>
      <td>India</td>
      <td>1575</td>
      <td>200.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>200.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Agra</td>
      <td>India</td>
      <td>1576</td>
      <td>212.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>200.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Agra</td>
      <td>India</td>
      <td>1577</td>
      <td>224.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>212.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Agra</td>
      <td>India</td>
      <td>1578</td>
      <td>236.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>224.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Agra</td>
      <td>India</td>
      <td>1579</td>
      <td>248.0</td>
      <td>India</td>
      <td>Agra - India</td>
      <td>236.0</td>
      <td>27.18333</td>
      <td>78.01667</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>6247</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1561</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6248</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1562</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6249</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1563</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6250</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1564</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
    <tr>
      <th>6251</th>
      <td>Vijayanagar</td>
      <td>India</td>
      <td>1565</td>
      <td>480.0</td>
      <td>India</td>
      <td>Vijayanagar - India</td>
      <td>480.0</td>
      <td>15.33500</td>
      <td>76.46200</td>
    </tr>
  </tbody>
</table>
<p>6252 rows × 9 columns</p>
</div>




```python
z = ZippedCsvs(data_sources['kaggle_coronavirus_dataset'])
list(z)
```
