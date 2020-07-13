import os


def pprint(d):
    print('-------------------')
    for key in d:
        print(f'{key}: {d[key]}')
    print('')


if __name__ == '__main__':
    Record = dict(OptDate=None,
                  Opt=None,
                  ID=None)
    for key in Record:
        pprint(Record)
        s = input(f'{key}: ')
        Record[key] = s

    pprint(Record)
