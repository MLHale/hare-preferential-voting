# hare-preferential-voting
This is a simple pythonic implementation of the HARE preferential voting process. 

More information about HARE can be found here:
https://plato.stanford.edu/entries/voting-methods/
http://www.bikmort.com/dokuwiki/hare_voting_procedure

## Requirements
[Python 2.7](https://www.python.org/download/releases/2.7/)

## Getting started
```bash
git clone https://github.com/MLHale/hare-preferential-voting
cd hare-preferential-voting
python hare-pref-voting.py <path to csv file formatted as shown below>
```
That's it. Hit enter and watch the results roll in.

## Assumptions
The CSV file should follow the following structure:
```
<preamble 1>
ballot 1-1
ballot 1-2
...
ballot 1-k
end
<preamble 2>
ballot 2-1
ballot 2-2
...
ballot 2-j
end
...
<preamble n>
```
where
```bnf
<preamble> := start,<name of election title>,<number of open slots>,<candidate 1 name>,<candidate 2 name>,...<candidate N name>
```
and a ballot takes the form:
```
<first candidate choice>,<second candidate choice>,...,<M-th candidate choice>
```
where each candidate choice is one of the names in the preamble

## Example
```csv
start, a cool election,2,bob,alice,sue
sue, bob, alice
alice, bob, sue,
alice, sue, bob
end
start, another cool election, 1, linda, rohm, ling
ling, rohm, linda
linda, ling, rohm
linda, lina, rohm
ling, linda, rohm
rohm, linda, ling
end
```

# License
Simple Hare preferential voting in python
Copyright (C) 2018, Matt Hale

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
