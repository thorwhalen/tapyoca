# What do we think about other peoples?

This project is meant to get an idea of what people think of people for different nations, as seen by what they ask google about them. 

Here I use python code to acquire, clean up, and analyze the data. 

## Demonym

If you're like me and enjoy the false and fleeting impression of superiority that comes when you know a word someone else doesn't. If you're like me and go to parties for the sole purpose of seeking victims to get a one-up on, here's a cool word to add to your arsenal:

**demonym**: a noun used to denote the natives or inhabitants of a particular country, state, city, etc.
_"he struggled for the correct demonym for the people of Manchester"_

## Back-story of this analysis
 
During a discussion (about traveling in Europe) someone said "why are the swiss so miserable". Now, I wouldn't say that the swiss were especially miserable (a couple of ex-girlfriends aside), but to be fair he was contrasting with Italians, so perhaps he has a point. I apologize if you are swiss, or one of the two ex-girlfriends -- nothing personal, this is all for effect. 

We googled "why are the swiss so ", and sure enough, "why are the swiss so miserable" came up as one of the suggestions. So we got curious and started googling other peoples: the French, the Germans, etc.

That's the back-story of this analysis. This analysis is meant to get an idea of what we think of peoples from other countries. Of course, one can rightfully critique the approach I'll take to gauge "what we think" -- all three of these words should, but will not, be defined. I'm just going to see what google's *current* auto-suggest comes back with when I enter "why are the X so " (where X will be a noun that denotes the natives of inhabitants of a particular country; a *demonym* if you will). 

## Warning

Again, word of warning: All data and analyses are biased. Take everything you'll read here (and to be fair, what you read anywhere) with a grain of salt. For simplicitly I'll say "what we think of...", but I don't **really** mean that.

## Resources

* http://www.geography-site.co.uk/pages/countries/demonyms.html for my list of demonyms.
* google for my suggestion engine, using the url prefix: `http://suggestqueries.google.com/complete/search?client=chrome&q=`


# The results

## In a nutshell

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


## Who do we most talk/ask about?

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

## Who do we least talk/ask about?

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

## What do we think about people?

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

## Who is beautiful? Who is tall? Who is short? Who is smart?

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

# How did I do it?

I scraped a list of (country, demonym) pairs from a table in http://www.geography-site.co.uk/pages/countries/demonyms.html.

Then I diagnosed these and manually made a mapping to simplify some "complex" entries, 
such as mapping an entry such as "Irishman or Irishwoman or Irish" to "Irish".

Using the google suggest API (http://suggestqueries.google.com/complete/search?client=chrome&q=), I requested what the suggestions 
for `why are the $demonym so ` query pattern, for `$demonym` running through all 217 demonyms from the list above, 
storing the results for each if the results were non-empty. 

Then, it was just a matter of pulling this data into memory, formatting it a bit, and creating a pandas dataframe that I could then interrogate.
 