import sys
import argparse

data = []
info = {'seen': 0, 'nseen': 0, 'Сериал': 0,
        'OVA': 0, 'Спешл': 0, 'Фильм': 0, 'ONA': 0}


def dataInit():
    with open('data.txt', 'r') as inp:
        a = inp.readlines()

    a = [i.strip() for i in a]
    for i in range(len(a)):
        data.append(a[i].split('\t'))


def dataStore():
    o = []
    for string in data:
        string = [str(i) for i in string]
        temp = '\t'.join(string)
        temp += '\n'
        o.append(temp)

    with open('data.txt', 'w') as out:
        for el in o:
            out.write(el)


def dataPrint(inp):
    ret = []
    for string in inp:
        temp = ''
        if string[1] == 'true':
            temp = '[x] '
        elif string[1] == 'false':
            temp = '[ ] '
        temp += string[0]
        temp += '\t('
        temp += string[2]
        temp += ')'
        ret.append(temp)
    ret.sort()
    return ret


def dataSearch(string, source):
    ret = []
    for el in source:
        if string.lower() in el[0].lower():
            ret.append(el)
    ret.sort()
    return ret


def refreshInfo(source):
    info = {'seen': 0, 'nseen': 0, 'Сериал': 0,
            'OVA': 0, 'Спешл': 0, 'Фильм': 0, 'ONA': 0}
    for el in source:
        if el[1] == 'true':
            info['seen'] += 1
        elif el[1] == 'false':
            info['nseen'] += 1
        info[el[2]] += 1
    return info


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--filter', choices=['seen', 'nseen'])
    parser.add_argument('-s', '--search', nargs='+')
    parser.add_argument('-i', '--imp', type=open)
    parser.add_argument('-p', '--print', action='store_true')
    parser.add_argument('-a', '--add', nargs='+')
    return parser


def main():
    dataInit()

    parser = createParser()
    params = parser.parse_args(sys.argv[1:])

    if params.imp:  # -i / --imp
        addition = (params.add.readlines())
        addition = [i.strip() for i in addition]
        addition = [i.split('\t') for i in addition]
        data.extend(addition)

    if params.add:  # -a / --add
        addition = params.add
        name = ' '.join(addition[:-2])
        request = [name, addition[-2], addition[-1]]
        data.append(request)
        data.sort()

    copy = data.copy()

    if params.filter:
        request = params.filter
        if request == 'nseen':
            request = 'false'
        else:
            request = 'true'
        copy = []
        for anime in data:
            if anime[1] == request:
                copy.append(anime)

    if params.search:  # -s / --s
        request = ' '.join(params.search)
        temp = dataSearch(request, copy)
        temp = dataPrint(temp)
        for el in temp:
            print(el)

    if params.print:  # -p / --print
        info = refreshInfo(copy)
        o = dataPrint(copy)
        for el in o:
            print(el)
        print('Всего: {}  Просмотрено: {}  Запланировано: {}'.format(
            len(o) - 1, info['seen'], info['nseen']))
        print('Сериалы: {}  Фильмы: {}  Спешиалы: {}  OVA: {}  ONA: {}'.format(
            info['Сериал'], info['Фильм'], info['Спешл'], info['OVA'], info['ONA']))

    dataStore()


main()
