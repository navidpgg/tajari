from machine import Machine

m=Machine(input('machine file path: '))
while True:
    s=input('enter string to check: ')
    print('پذیرفته شد' if m.accepts(s) else 'پذیرفتته نشد')
    m.format_search_dump()
    m.search_dump={}