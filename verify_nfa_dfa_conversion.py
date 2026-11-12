from machine import Machine


m = Machine('machine.json')
m.to_dfa('dfa.json')

d = Machine('dfa.json')
for s in ['babababaaaa', 'babababaaaab', 'ba', '', 'a', 'b', 'baa', 'baba']:
    assert m.accepts(s) == d.accepts(s), s
print('NFA=DFA')