import sys,json

startState=None
states=set()
alphabet=set()
endstates=set()
transitionTable=[]

with open(sys.argv[1],'r') as f:
    rg=f.read()
    for line in rg.split('\n'):
        print(line.split('->'))
        leftState,right = line.split('->')
        isends=False
        for transition in right.split('|'):
            letter=transition[0]
            if letter=='λ':isends=True;continue
            ns=transition[1:]
            startState=leftState if startState is None else None
            states.add(leftState)
            states.add(ns)
            alphabet.add(letter)
            transitionTable.append((leftState,letter,ns))
        if isends:endstates.add(leftState)

with open(sys.argv[1]+'.json','w+') as f:
    import json
    json.dump({
        'states':list(states),
        'alphabet':list(alphabet),
        'startState':[startState],
        'endStates':list(endstates),
        'transitionTable':transitionTable
    },f,indent=2)