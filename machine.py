import json

class Machine:
    def __init__(self,filepath):
        with open(filepath) as f:
            machine=json.load(f)
            self.alphabet=machine['alphabet']
            self.states=machine['states']
            self.endStates=machine['endStates']
            self.startState=machine['startState']
            self.table=machine['transitionTable']

        assert all((x in self.states) for x in self.endStates)
        assert self.startState in self.states

        # self.s2s[STATE1][LETTER] yields list of reachable STATES
        self.s2s = {s: {} for s in self.states}
        for state, letter, nxt in self.table:
            self.s2s[state].setdefault(letter, []).append(nxt)

        self.search_dump={}

    def epsilon_closure(self, states):
        #مجموعه تمامی حالاتی که با ـ رسیده میشود
        closure=set(states)
        stack=list(states)
        while stack:
            s=stack.pop()
            for ns in self.s2s[s].get('_',[]):
                if ns not in closure:
                    closure.add(ns)
                    stack.append(ns)
        return closure
    
    def accepts(self,string,instate=None,trace=None):
        # به صورت بازگشتی و با رکورد مسیر ماشین رشته را قبول میکند یا نه
        trace=trace if trace is not None else self.search_dump
        currentstate= instate or self.startState
        trace['state']=currentstate
        trace['string']=string
        closure=self.epsilon_closure({currentstate})

        if len(string)==0:
            return any(state in self.endStates for state in closure)
        
        letter=string[0]
        next_states_reachable_with_letter=set()
        for state in closure:
            next_states_reachable_with_letter.update(self.s2s[state].get(letter,[]))
        trace['next']={key:{} for key in next_states_reachable_with_letter}

        if not next_states_reachable_with_letter:
            return False

        return any(
            self.accepts(string[1:],ns,trace['next'][ns]) for ns in next_states_reachable_with_letter
            )
    
    def format_search_dump(self, tab=None,continue_=None):
        # به صورت بازگشتی مسیر رکورد شده در مرحله قبل را نمایش میدهیم
        tab= tab if tab is not None else ''
        continue_=continue_ if continue_ is not None else self.search_dump

        print(f"{tab}{continue_['state']}({continue_['string']})")
        if continue_.get('next') is None:
            if continue_['state'] in self.endStates:print(tab+'  '+'✓')
            else:print(tab+'  '+'x')
            return;
        for state,val in continue_['next'].items():
            if val: # {}
                self.format_search_dump(tab+'  ', val)
    
    def to_dfa(self, filepath='dfa.json'):
        # _ subset construction
        eps = {s: frozenset(self.epsilon_closure({s})) for s in self.states}
        def name(subset): # {S1,S2}
            return '{' + ','.join(sorted(subset)) + '}'
        start = eps[self.startState]
        dfa_states = [start]
        names = {start: name(start)}
        table = []
        i = 0
        while i < len(dfa_states):
            subset = dfa_states[i]
            i += 1
            for letter in self.alphabet:
                if letter == '_':continue
                nxt = set()
                for s in subset:
                    nxt.update(self.s2s[s].get(letter, []))
                if not nxt:
                    continue
                closed = frozenset(x for s in nxt
                                    for x in eps[s])
                if closed not in names:
                    names[closed] = name(closed)
                    dfa_states.append(closed)
                table.append([names[subset], letter, names[closed]])
        dfa = {
            'states':[names[s] for s in dfa_states],
            'alphabet':[c for c in self.alphabet if c != '_'],
            'startState':names[start],
            'endStates':[names[s] for s in dfa_states
                        if any(x in self.endStates for x in s)],
            'transitionTable': table,
        }
        with open(filepath, 'w') as f:
            json.dump(dfa, f, indent=2)
        return dfa