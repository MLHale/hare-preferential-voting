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
<preamble>
ballot 1
ballot 2
...
ballot k
end
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
start,<name of election title>,<number of open slots>,<candidate 1 name>,<candidate 2 name>,...<candidate N name>
<first candidate choice>,<second candidate choice>,...,<M-th candidate choice>
.
.
.
<first candidate choice>,<second candidate choice>,...,<M-th candidate choice>
end
```
