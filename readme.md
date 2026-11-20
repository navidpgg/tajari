## پروژه ۱

run:
```
git clone https://github.com/navidpgg/tajari.git ./navid/
cd ./navid/
python interactive.py
```

تبدیل nfaبه dfa:

`python verify_nfa_dfa_conversion.py`

input machine with string (+trace):

`python interactive.py`

code in [machine.py](./machine.py)

![nfa](92d952a5-86fc-45e0-8aff-4ef228647441.png)
![dfa](DFA_example_multiplies_of_3.svg)

## پروژه ۲ 

- [تبدیل dfa به گرامر منظم](./to_rg.py)
- [تبدیل گرامر منظم به dfa](./convert_rg_to_nfa.py)