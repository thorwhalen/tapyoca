# tapyoca
A medley of small projects


# parquet_deformations

I'm calling these [Parquet deformations](https://www.theguardian.com/artanddesign/alexs-adventures-in-numberland/2014/sep/09/crazy-paving-the-twisted-world-of-parquet-deformations#:~:text=In%20the%201960s%20an%20American,the%20regularity%20of%20the%20tiling.) but purest would lynch me. 

Really, I just wanted to transform one word into another word, gradually, as I've seen in some of [Escher's](https://en.wikipedia.org/wiki/M._C._Escher) work, so I looked it up, and saw that it's called parquet deformations. The math looked enticing, but I had no time for that, so I did the first way I could think of: Mapping pixels to pixels (in some fashion -- but nearest neighbors is the method that yields nicest results, under the pixel-level restriction). 

Of course, this can be applied to any image (that will be transformed to B/W (not even gray -- I mean actual B/W), and there's several ways you can perform the parquet (I like the gif rendering). 

The main function (exposed as a script) is `mk_deformation_image`. All you need is to specify two images (or words). If you want, of course, you can specify:
- `n_steps`: Number of steps from start to end image
- `save_to_file`: path to file to save too (if not given, will just return the image object)
- `kind`: 'gif', 'horizontal_stack', or 'vertical_stack'
- `coordinate_mapping_maker`: A function that will return the mapping between start and end. 
This function should return a pair (`from_coord`, `to_coord`) of aligned matrices whose 2 columns are the the 
`(x, y)` coordinates, and the rows represent aligned positions that should be mapped. 



## Examples

### Two words...


```python
fit_to_size = 400
start_im = image_of_text('sensor').rotate(90, expand=1)
end_im = image_of_text('meaning').rotate(90, expand=1)
start_and_end_image(start_im, end_im)
```




![png](tapyoca/parquet_deformations/img/outputs/output_5_0.png)




```python
im = mk_deformation_image(start_im, end_im, 15, kind='h').resize((500,200))
im
```




![png](tapyoca/parquet_deformations/img/outputs/output_6_0.png)




```python
im = mk_deformation_image(start_im.transpose(4), end_im.transpose(4), 5, kind='v').resize((200,200))
im
```




![png](tapyoca/parquet_deformations/img/outputs/output_7_0.png)




```python
f = 'sensor_meaning_knn.gif'
mk_deformation_image(start_im.transpose(4), end_im.transpose(4), n_steps=20, save_to_file=f)
display_gif(f)
```




<img src="sensor_meaning_knn.gif?76128495">




```python
f = 'sensor_meaning_scan.gif'
mk_deformation_image(start_im.transpose(4), end_im.transpose(4), n_steps=20, save_to_file=f, 
                     coordinate_mapping_maker='scan')
display_gif(f)
```




<img src="sensor_meaning_scan.gif?76996026">




```python
f = 'sensor_meaning_random.gif'
mk_deformation_image(start_im.transpose(4), end_im.transpose(4), n_steps=20, save_to_file=f, 
                     coordinate_mapping_maker='random')
display_gif(f)
```




<img src="sensor_meaning_random.gif?80233280">



### From a list of words


```python
start_words = ['sensor', 'vibration', 'tempature']
end_words = ['sense', 'meaning', 'detection']
start_im, end_im = make_start_and_end_images_with_words(
    start_words, end_words, perm=True, repeat=2, size=150)
start_and_end_image(start_im, end_im).resize((600, 200))
```




![png](tapyoca/parquet_deformations/img/outputs/output_12_0.png)




```python
im = mk_deformation_image(start_im, end_im, 5)
im
```




![png](tapyoca/parquet_deformations/img/outputs/output_13_0.png)




```python
f = 'bunch_of_words.gif'
mk_deformation_image(start_im, end_im, n_steps=20, save_to_file=f)
display_gif(f)
```




<img src="bunch_of_words.gif?7402792">



## From files


```python
start_im = Image.open('sensor_strip_01.png')
end_im = Image.open('sense_strip_01.png')
start_and_end_image(start_im.resize((200, 500)), end_im.resize((200, 500)))
```




![png](tapyoca/parquet_deformations/img/outputs/output_16_0.png)




```python
im = mk_deformation_image(start_im, end_im, 7)
im
```




![png](tapyoca/parquet_deformations/img/outputs/output_17_0.png)




```python
f = 'medley.gif'
mk_deformation_image(start_im, end_im, n_steps=20, save_to_file=f)
display_gif(f)
```




<img src="medley.gif?39255021">




```python
mk_deformation_image(start_im, end_im, n_steps=20, save_to_file=f, coordinate_mapping_maker='scan')
display_gif(f)
```




<img src="sensor_meaning.gif?41172115">



## an image and some text


```python
start_im = 'img/waveform_01.png'  # will first look for a file, and if not consider as text
end_im = 'makes sense'

mk_gif_of_deformations(start_im, end_im, n_steps=20, 
                               save_to_file='image_and_text.gif')
display_gif('image_and_text.gif')  
```




<img src="image_and_text.gif?92524789">






# demonys

## What do we think about other peoples?

This project is meant to get an idea of what people think of people for different nations, as seen by what they ask google about them. 

Here I use python code to acquire, clean up, and analyze the data. 

### Demonym

If you're like me and enjoy the false and fleeting impression of superiority that comes when you know a word someone else doesn't. If you're like me and go to parties for the sole purpose of seeking victims to get a one-up on, here's a cool word to add to your arsenal:

**demonym**: a noun used to denote the natives or inhabitants of a particular country, state, city, etc.
_"he struggled for the correct demonym for the people of Manchester"_

### Back-story of this analysis
 
During a discussion (about traveling in Europe) someone said "why are the swiss so miserable". Now, I wouldn't say that the swiss were especially miserable (a couple of ex-girlfriends aside), but to be fair he was contrasting with Italians, so perhaps he has a point. I apologize if you are swiss, or one of the two ex-girlfriends -- nothing personal, this is all for effect. 

We googled "why are the swiss so ", and sure enough, "why are the swiss so miserable" came up as one of the suggestions. So we got curious and started googling other peoples: the French, the Germans, etc.

That's the back-story of this analysis. This analysis is meant to get an idea of what we think of peoples from other countries. Of course, one can rightfully critique the approach I'll take to gauge "what we think" -- all three of these words should, but will not, be defined. I'm just going to see what google's *current* auto-suggest comes back with when I enter "why are the X so " (where X will be a noun that denotes the natives of inhabitants of a particular country; a *demonym* if you will). 

### Warning

Again, word of warning: All data and analyses are biased. 
Take everything you'll read here (and to be fair, what you read anywhere) with a grain of salt. 
For simplicitly I'll saying things like "what we think of..." or "who do we most...", etc.
But I don't **really** mean that.

### Resources

* http://www.geography-site.co.uk/pages/countries/demonyms.html for my list of demonyms.
* google for my suggestion engine, using the url prefix: `http://suggestqueries.google.com/complete/search?client=chrome&q=`


## The results

### In a nutshell

Below is listed 73 demonyms along with words extracted from the very first google suggestion when you type. 

`why are the DEMONYM so `

```text
afghan    	                eyes beautiful
albanian  	                     beautiful
american  	          girl dolls expensive
australian	                          tall
belgian   	                    fries good
bhutanese 	                         happy
brazilian 	              good at football
british   	     full of grief and despair
bulgarian 	              properties cheap
burmese   	             cats affectionate
cambodian 	                   cows skinny
canadian  	                          nice
chinese   	                       healthy
colombian 	                  avocados big
cuban     	                   cigars good
czech     	                          tall
dominican 	  republic and haiti different
egyptian  	                gods important
english   	                      reserved
eritrean  	                     beautiful
ethiopian 	                     beautiful
filipino  	                         proud
finn      	               shoes expensive
french    	                       healthy
german    	                          tall
greek     	                gods messed up
haitian   	                parents strict
hungarian 	                    words long
indian    	            tv debates chaotic
indonesian	                         smart
iranian   	                     beautiful
israeli   	           startups successful
italian   	                         short
jamaican  	                sprinters fast
japanese  	                        polite
kenyan    	                  runners good
lebanese  	                          rich
malagasy  	                    names long
malaysian 	                   drivers bad
maltese   	                          rude
mongolian 	                  horses small
moroccan  	                rugs expensive
nepalese  	                     beautiful
nigerian  	                          tall
north korean	                      hats big
norwegian 	                 flights cheap
pakistani 	                          fair
peruvian  	               blueberries big
pole      	                  vaulters hot
portuguese	                         short
puerto rican	       and cuban flags similar
romanian  	                     beautiful
russian   	                  good at math
samoan    	                           big
saudi     	                      arrogant
scottish  	                        bitter
senegalese	                          tall
serbian   	                          tall
singaporean	                          rude
somali    	                parents strict
south african	                     plugs big
south korean	                          tall
sri lankan	                          dark
sudanese  	                          tall
swiss     	        good at making watches
syrian    	                families large
taiwanese 	                        pretty
thai      	                        pretty
tongan    	                           big
ukrainian 	                     beautiful
vietnamese	        fiercely nationalistic
welsh     	                          dark
zambian   	                emeralds cheap
```


Notes:
* The queries actually have a space after the "so", which matters so as to omit suggestions containing words that start with so.
* Only the tail of the suggestion is shown -- minus prefix (`why are the DEMONYM` or `why are DEMONYM`) as well as the `so`, where ever it lands in the suggestion. 
For example, the first suggestion for the american demonym was "why are american dolls so expensive", which results in the "dolls expensive" association. 


### Who do we most talk/ask about?

The original list contained 217 demonyms, but many of these yielded no suggestions (to the specific query format I used, that is). 
Only 73 demonyms gave me at least one suggestion. 
But within those, number of suggestions range between 1 and 20 (which is probably the default maximum number of suggestions for the API I used). 
So, pretending that the number of suggestions is an indicator of how much we have to say, or how many different opinions we have, of each of the covered nationalities, 
here's the top 15 demonyms people talk about, with the corresponding number of suggestions 
(proxy for "the number of different things people ask about the said nationality). 

```text
french         20
singaporean    20
german         20
british        20
swiss          20
english        19
italian        18
cuban          18
canadian       18
welsh          18
australian     17
maltese        16
american       16
japanese       14
scottish       14
```

### Who do we least talk/ask about?

Conversely, here are the 19 demonyms that came back with only one suggestion.

```text
somali          1
bhutanese       1
syrian          1
tongan          1
cambodian       1
malagasy        1
saudi           1
serbian         1
czech           1
eritrean        1
finn            1
puerto rican    1
pole            1
haitian         1
hungarian       1
peruvian        1
moroccan        1
mongolian       1
zambian         1
```

### What do we think about people?

Why are the French so...

How would you (if you're (un)lucky enough to know the French) finish this sentence?
You might even have several opinions about the French, and any other group of people you've rubbed shoulders with.
What words would your palette contain to describe different nationalities?
What words would others (at least those that ask questions to google) use?

Well, here's what my auto-suggest search gave me. A set of 357 unique words and expressions to describe the 72 nationalities. 
So a long tail of words use only for one nationality. But some words occur for more than one nationality. 
Here are the top 12 words/expressions used to describe people of the world. 

```text
beautiful         11
tall              11
short              9
names long         8
proud              8
parents strict     8
smart              8
nice               7
boring             6
rich               5
dark               5
successful         5
```

### Who is beautiful? Who is tall? Who is short? Who is smart?

```text
beautiful      : albanian, eritrean, ethiopian, filipino, iranian, lebanese, nepalese, pakistani, romanian, ukrainian, vietnamese
tall           : australian, czech, german, nigerian, pakistani, samoan, senegalese, serbian, south korean, sudanese, taiwanese
short          : filipino, indonesian, italian, maltese, nepalese, pakistani, portuguese, singaporean, welsh
names long     : indian, malagasy, nigerian, portuguese, russian, sri lankan, thai, welsh
proud          : albanian, ethiopian, filipino, iranian, lebanese, portuguese, scottish, welsh
parents strict : albanian, ethiopian, haitian, indian, lebanese, pakistani, somali, sri lankan
smart          : indonesian, iranian, lebanese, pakistani, romanian, singaporean, taiwanese, vietnamese
nice           : canadian, english, filipino, nepalese, portuguese, taiwanese, thai
boring         : british, english, french, german, singaporean, swiss
rich           : lebanese, pakistani, singaporean, taiwanese, vietnamese
dark           : filipino, senegalese, sri lankan, vietnamese, welsh
successful     : chinese, english, japanese, lebanese, swiss
```

## How did I do it?

I scraped a list of (country, demonym) pairs from a table in http://www.geography-site.co.uk/pages/countries/demonyms.html.

Then I diagnosed these and manually made a mapping to simplify some "complex" entries, 
such as mapping an entry such as "Irishman or Irishwoman or Irish" to "Irish".

Using the google suggest API (http://suggestqueries.google.com/complete/search?client=chrome&q=), I requested what the suggestions 
for `why are the $demonym so ` query pattern, for `$demonym` running through all 217 demonyms from the list above, 
storing the results for each if the results were non-empty. 

Then, it was just a matter of pulling this data into memory, formatting it a bit, and creating a pandas dataframe that I could then interrogate.
 
## Resources you can find here

The code to do this analysis yourself, from scratch here: `data_acquisition.py`.

The jupyter notebook I actually used when I developed this: `01 - Demonyms and adjectives - why are the french so....ipynb`
 
Note you'll need to pip install py2store if you haven't already.

In the `data` folder you'll find
* country_demonym.p: A pickle of a dataframe of countries and corresponding demonyms
* country_demonym.xlsx: The same as above, but in excel form
* demonym_suggested_characteristics.p: A pickle of 73 demonyms and auto-suggestion information, including characteristics. 
* what_we_think_about_demonyns.xlsx: An excel containing various statistics about demonyms and their (perceived) characteristics
 





# Agglutinations

Inspired from a [tweet](https://twitter.com/raymondh/status/1311003482531401729) from Raymond Hettinger this morning:

_Resist the urge to elide the underscore in multiword function or method names_

So I wondered...

## Gluglus

The gluglu of a word is the number of partitions you can make of that word into words (of length at least 2 (so no using a or i)).
(No "gluglu" isn't an actual term -- unless everyone starts using it from now on. 
But it was inspired from an actual [linguistic term](https://en.wikipedia.org/wiki/Agglutination).)

For example, the gluglu of ``newspaper`` is 4:

```
newspaper
    new spa per
    news pa per
    news paper
```

Every (valid) word has gluglu at least 1.


## How many standard library names have gluglus at last 2?

108

Here's [the list](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/standard_lib_gluglus.txt) of all of them.

The winner has a gluglu of 6 (not 7 because formatannotationrelativeto isn't in the dictionary)

```
formatannotationrelativeto
	for mat an not at ion relative to
	for mat annotation relative to
	form at an not at ion relative to
	form at annotation relative to
	format an not at ion relative to
	format annotation relative to
```

## Details

### Dictionary

Really it depends on what dictionary we use. 
Here, I used a very conservative one. 
The intersection of two lists: The [corncob](http://www.mieliestronk.com/corncob_lowercase.txt) 
and the [google10000](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt) word lists.
Additionally, I only kept of those, those that had at least 2 letters, and had only letters (no hyphens or disturbing diacritics).

Diacritics. Look it up. Impress your next nerd date.

Im left with 8116 words. You can find them [here](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/words_8116.csv).

### Standard Lib Names

Surprisingly, that was the hardest part. I know I'm missing some, but that's enough rabbit-holing. 

What I did (modulo some exceptions I won't look into) was to walk the standard lib modules (even that list wasn't a given!) 
extracting (recursively( the names of any (non-underscored) attributes if they were modules or callables, 
as well as extracting the arguments of these callables (when they had signatures).

You can find the code I used to extract these names [here](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/py_names.py) 
and the actual list [there](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/standard_lib_module_names.csv).



# covid

## Bar Chart Races (applied to covid-19 spread)

The module will show is how to make these:
- Confirmed cases (by country): https://public.flourish.studio/visualisation/1704821/
- Deaths (by country): https://public.flourish.studio/visualisation/1705644/
- US Confirmed cases (by state): https://public.flourish.studio/visualisation/1794768/
- US Deaths (by state): https://public.flourish.studio/visualisation/1794797/

### The script

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
 
 
### The jupyter notebook

The notebook (the .ipynb file) shows you how to do it step by step in case you want to reuse the methods for other stuff.



## Getting and preparing the data

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



### Update coronavirus data


```python
# To update the coronavirus data:
def update_covid_data(data_sources):
    """update the coronavirus data"""
    if 'kaggle_coronavirus_dataset' in data_sources._caching_store:
        del data_sources._caching_store['kaggle_coronavirus_dataset']  # delete the cached item
    _ = data_sources['kaggle_coronavirus_dataset']

# update_covid_data(data_sources)  # uncomment here when you want to update
```

### Prepare data for flourish upload


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


### Upload to Flourish, tune, and publish

Go to https://public.flourish.studio/, get a free account, and play.

Got to https://app.flourish.studio/templates

Choose "Bar chart race". At the time of writing this, it was here: https://app.flourish.studio/visualisation/1706060/

... and then play with the settings


## Discussion of the methods


```python
from py2store import *
from IPython.display import Image
```

### country flags images

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



### Caching the flag images data

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
