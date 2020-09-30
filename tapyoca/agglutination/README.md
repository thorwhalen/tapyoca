

Inspired from a [tweet](https://twitter.com/raymondh/status/1311003482531401729) from Raymond Hettinger this morning:

_Resist the urge to elide the underscore in multiword function or method names_

So I wondered...

# Gluglus

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


# How many standard library names have gluglus at last 2?

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

# Details

## Dictionary

Really it depends on what dictionary we use. 
Here, I used a very conservative one. 
The intersection of two lists: The [corncob](http://www.mieliestronk.com/corncob_lowercase.txt) 
and the [google10000](https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt) word lists.
Additionally, I only kept of those, those that had at least 2 letters, and had only letters (no hyphens or disturbing diacritics).

Diacritics. Look it up. Impress your next nerd date.

Im left with 8116 words. You can find them [here](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/words_8116.csv).

## Standard Lib Names

Surprisingly, that was the hardest part. I know I'm missing some, but that's enough rabbit-holing. 

What I did (modulo some exceptions I won't look into) was to walk the standard lib modules (even that list wasn't a given!) 
extracting (recursively( the names of any (non-underscored) attributes if they were modules or callables, 
as well as extracting the arguments of these callables (when they had signatures).

You can find the code I used to extract these names [here](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/py_names.py) 
and the actual list [there](https://github.com/thorwhalen/tapyoca/blob/master/tapyoca/agglutination/standard_lib_module_names.csv).
