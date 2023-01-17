# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 18:22:43 2019

@author: kevinstrickler
"""

import re
import pandas as pd


FILE = '/Users/kevinstrickler/Documents/Udacity/data_wrangling/cities.csv'

x = pd.read_csv(FILE)

# Pandas has a quick regex shortcut, very helpful, use as mask!
# Some values were empty, cannot index on NaN, so fillna with False.
mask = x['country_label'].str.contains('^I').fillna(False)

# Now, have all the country values that start with I.
z = x[mask]

# For pure python, instead instatiate a class for regular expression and then
# call methods on that regular expression.  This is a RegEx Object, which is a 
# compiled regular expression.

# There is also a compile object, which is the regex pattern (in bytecode)
pattern = re.compile('^I')

# Now that we have a pattern in bytecode, we can do things with it like match.
pattern.match('India') # compile pattern then see if it matches

# Raw text can be used if there are many escape characters (easier).
b = re.compile(r"\b") # not backspace now, just backslash and b.

x = b.match("\\")

pattern = re.compile(r'<HTML>')
pattern.match("<HTML>")

# Can skip separate compiling, and just use shortcut for compile methods.
re.match(r'<HTML>', "<HTML>")

# HOWEVER - if you use regex object (compile) then can limit the region to be searched.

# Match only looks at beginning of string, but search looks inside string.
pattern.match(" <HTML>")  # No match
pattern.search(" <HTML>")  # Match
pattern.match(" <HTML>", 1) # But, can change start position for match.

# ^ and $ are the start and end of a string, FYI

# Can slice string being searched.
pattern.match(" <HTML>"[1:])  # Match

# Search is for any place in the string (like str.contains in Pandas).
pattern.search("  <HTML>")  # Match

# Can complie with multiline indicator, then search beginning of each line.
pattern = re.compile(r'^<HTML>', re.MULTILINE)

pattern.search('  \n<HTML>') # Match of second line starting.
pattern.search('  \n <HTML>') # No match, second line starts with space.

# Python has search and match.  match searches at beg of string (can change where
# it starts) and search is anywhere in string.  Pandas has similar regeg methods
# (str.contains and str.match)

# search returns a regex object.
pattern = re.compile(r'<HTML>')
pattern.search("  \n<HTML>")
pattern.findall(',<HTML>,dd<HTML>')
pattern = re.compile(r"\w+")
item = pattern.finditer("hello world")  # Get more info with finditer (returns interator)
for item in pattern.finditer("hello world") :
    print(item) # prints start, stop and, match word.

# Can use split, and split on regular expressions!  Much more powerful!
#  NOTE: Pandas lets you split on regex too!!!!

x = re.split('\n', 'The dog is a hog.\nNext up.\nCat dog!') # Splits into three lines!


# Can return matched pattern after replacement is made.
pattern = re.compile(r"[0-9]+") # all digits
pattern.sub("-", "order0 order1 order2")

# Can use a function in the sub replace argument.
def normalize_orders(matchobj):
    if matchobj.group(1) == '-': return "A"
    else: return "B"

# Below replaces ones starting with dash with A, the rest with B.
re.sub('([-|A-Z])', normalize_orders, '-1234 A193 B123')

# Try out syntax, can findall and return matches in a list, then can access
# results like accessing a list.
x = re.findall('[0-9]','2341dog')
x[0]
x[1]
for item in x:
    print(item)

# There are both character literals and metacharacters.  To use metacharcaters such as
# parenthesis as literals, need to excape them wiht backslash, use r'' raw
# string, or use re.escape.
x = re.search('\(dog\)', '(dog)')

# Can get match object text using group! (not for findall though, this is list)
x.group(0) # shows (dog)

# 12 metacharacters to escape to use literally: ^$.|?()*+[{\

# CHARACTER CLASSES!
# Use brackets to define options for literal characters.
# Put in single options without dash, e.g. cs is c or s.
x = re.findall('licen[cs]e', 'American license, British licence')
x[0] # American spelling
x[1] # British spelling

# To match a set, use a dash, can use for numbers or letters.
x = re.search('[0-9]', 'dog2')
x.group(0)

x = re.search('[A-Za-z]', 'a Dog')  # Any letter upper or lower.
x.group(0)

# Like Pandas, can negate meaning using ^ caret symbol (if not letter).
x = re.findall('fish[^e]s', 'fishes fishas fishos')  # Returns second and third.
x[0]
x[1]
x[2]

# Predefined character classes in regex!  Check out the following:
# Recommend use below if you can!  Shorter, easier to read!
 # lowercase matches, uppercase negates
# . matches any charcater except newline \n
# \d any decimal digit [0-9]
# \D any non digit charachter, [^0-9]
# \s any whitespace character
# \S Any non-whitespace character.
# \w Any alphanumeric character [a-zA-Z0-9]
# \W Any non-alphanumeric character [^a-zA-Z0-9]

re.search('...', 'd $cat')  # Any three characters in a row.
re.search('\d', 'dog1')  # any digit
re.search('\D', 'dog1')  # Any non digit
re.search('\s', 'dog dog')  # Any whitespace character.
re.search('\S', 'dog dog')  # Any non whitespace character.
re.search('\w', 'a1$$')  # Any alphanumeric
re.search('\w', 'a1$$')  # Any nonalphanumeric


# NOTE: Don't overuse dot, better to concisely express what you are looking for.
# Example, to match any character except Windows and unix filepath separators.
# Note no dots are necessary.
x = re.findall("[^\\\\]", 'file\path') # Need to put in four backslashes,
# (because the string parser will remove two of them when "de-escaping" it for
# the string, and then the regex needs two for an escaped regex backslash).
for i in x:
    print(i)  # Excludes slash!

# Use | pipe as or, like pandas.
x = re.search('yes|no|maybe', 'And maybe so')
x.group(0)

#  If alternation is part of larger expression, wrap in PARENTHESIS (not brackets, 
# which are for character sets instead [yes|no] means y, or e, or s, etc.).
x = re.search('License: (yes|no)', 'License: yes')  # Only matches if parens.
x.group(0)

# QUANTIFIERS!  For repeated characters or character sets!
# ? 0 or 1 repetetion
# * 0 or more times
# + 1 or more times
# {0,3} curly braces, between 0 and three times.

x = re.findall('cars?', 'car and cars')  # optionally matches the s.
x[0]  # car
x[1]  # cars 'car' would have not returned the s.

# Finds all phone numbers with area code, regardless if dash, spaces, or together.
x = re.findall('\d{3}?[-\s]?\d{4}[-\s]?\d{3}', '000-1234-456 000 0001 123 4444444444')
x[2]

# To designate up to and minimum times to repeat, use {,x} or {x,}
# Up to x times or minimum of x times.


# Greedy and reluctant quantifiers!  Greedy is default!
# Greedy will try to match as much as possible to get biggest result possible
# Non-greedy behavior can be requested by adding an extra question mark to the
# quantifier.  This will try to have smallest match possible.
x = re.search('".+"', 'English "hello", Spanish "hola"')
x.group(0)   # Greedy, returns all after hello.
x = re.findall('".+?"', 'English "hello", Spanish "hola"')  # Add extra quesiton mark.
x[0]  # Non greedy, returns only hello and hola.
x[1]

# Boundry matchers!
# ^ beginning of a line
# $ end of a line
