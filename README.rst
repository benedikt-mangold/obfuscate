==========
obfuscator
==========

Package for
obfuscating text with sensitive information while
maintaining relevant information such as
- Order of tokens
- Identical mapping of identical tokens

Any human readible information is thus purged from the text. However,
token-based machine learning algorithm are stil able to pickup
the information provided by the tokens, see the jupyter-notebook example
provided in the `example` directory

# Text manipulations
The text is reformatted as follows:

- signs are left as is
- latin-alpha numeric tokens are exchanged by random latin-alpha
numeric tokens, while maintaining
the amount of alpha- and numeric- characters
- chinese characters are split into character groups using `jieba` and
each group is replaced by a random chinese character group
- the remaining tokens are transformed into a random latin-alpha numeric
string of length `N`

The mapping is stored internally and can be reverted.


TODO:
- reversible operation

### Who do I talk to? ###

* benedikt.mangold@mailbox.org
