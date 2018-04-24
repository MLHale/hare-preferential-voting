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
ballot 2-k
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
