# utf-8

import time


class IssueRecorder():
    def __init__(self):
        self.prefix = 'Z-L19'
        self.library = {}

    def init_entry(self, name, driver='paper'):
        entry = dict(name=name,
                     driver=driver,
                     create=None, deliver=None, destory=None)
        return entry

    def attr_entry(self, entry, opt, date):
        assert(opt in ['create', 'deliver', 'destory'])
        if entry[opt]:
            print(entry)
            raise ValueError('Entry already exists.')
        entry[opt] = date

    def append(self, paper_date, idx_list, opt, opt_date, driver='---'):
        if type(idx_list) is int:
            idx_list = [idx_list]

        for idx in idx_list:
            name = '%s-%s-%03d' % (self.prefix, paper_date, idx)
            if self.library.get(name, None) is None:
                assert(opt == 'create')
                # print('new entry: %s' % name)
                self.library[name] = self.init_entry(name, driver)

            # print('%s, %s, %s' % (name, opt, opt_date))
            self.attr_entry(self.library[name], opt, opt_date)

    def print_all(self):
        print('all:' + '-' * 80)
        for e in self.library.items():
            print('%s:' % e[0])
            for k in e[1].items():
                print('  %10s:  %s' % (k[0], k[1]))
            print()

    def print_close(self):
        print('close:' + '-' * 80)
        for e in self.library.items():
            if e[1]['deliver'] is not None and e[1]['destory'] is not None:
                continue
            if e[1]['deliver'] is None and e[1]['destory'] is None:
                continue
            print('%s:' % e[0])
            for k in e[1].items():
                print('  %10s:  %s' % (k[0], k[1]))
            print()

    def print_abnormal(self):
        print('abnormal:' + '-' * 80)
        for e in self.library.items():
            if e[1]['deliver'] is not None and e[1]['destory'] is not None:
                print('%s:' % e[0])
                for k in e[1].items():
                    print('  %10s:  %s' % (k[0], k[1]))
                if e[1]['destory'] < e[1]['deliver']:
                    print('  %10s: destory before deliver!!!' % 'warning')
                print()

    def print_open(self):
        print('open:' + '-' * 80)
        for e in self.library.items():
            if e[1]['deliver'] is None and e[1]['destory'] is None:
                print('%s:' % e[0])
                for k in e[1].items():
                    print('  %10s:  %s' % (k[0], k[1]))
                print()


ir = IssueRecorder()

####################################################
opt = 'create'

date = '20181229'
[ir.append(date, idxs, opt, date, driver)
 for idxs, driver in [[range(1, 7), 'paper'],
                      [range(7, 9), 'paper'],
                      [range(9, 11), 'paper'],
                      [range(11, 13), 'plant'],
                      [13, 'paper']]]

date = '20190102'
[ir.append(date, idxs, opt, date, driver)
 for idxs, driver in [[range(1, 7), 'paper'],
                      [range(7, 9), 'paper'],
                      [9, 'plant']]]

date = '20190103'
[ir.append(date, idxs, opt, date, driver)
 for idxs, driver in [[range(1, 3), 'paper'],
                      [3, 'plant']]]

date = '20190319'
[ir.append(date, idxs, opt, date, driver)
 for idxs, driver in [[range(1, 5), 'paper'],
                      [5, 'plant'],
                      [6, 'paper']]]

####################################################
opt = 'deliver'

opt_date = '20190612'
[ir.append('20181229', idxs, opt, opt_date)
 for idxs in [range(1, 7),
              range(7, 9),
              range(9, 11),
              12]]

opt_date = '20190320'
[ir.append('20190319', idxs, opt, opt_date)
 for idxs in [range(1, 5),
              5,
              6]]

####################################################
opt = 'destory'

opt_date = '20190424'
[ir.append('20190319', idxs, opt, opt_date)
 for idxs in [5]]

opt_date = '20190130'
[ir.append('20181229', idxs, opt, opt_date)
 for idxs in [range(11, 13),
              13,
              range(9, 11)]]
[ir.append('20190102', idxs, opt, opt_date)
 for idxs in [9,
              range(1, 7),
              range(7, 9)]]

#####################################################
opt = 'create'

opt_date = '20191025'
[ir.append('20191025', idxs, opt, opt_date)
for idxs in range(47, 51)]
[ir.append('20191025', idxs, opt, opt_date)
for idxs in range(51, 57)]

#####################################################
opt = 'destory'

opt_data = '20190125'
[ir.append('20191025', idxs, opt, opt_date)
for idxs in [47, 48]]

#####################################################
opt = 'deliver'

opt_date = '20191026'
[ir.append('20191025', idxs, opt, opt_date)
for idxs in [49, 50]]
[ir.append('20191025', idxs, opt, opt_date)
for idxs in range(51, 57)]

#####################################################
opt = 'create'

opt_date = '20191104'
[ir.append('20191104', idxs, opt, opt_date)
for idxs in [1, 2]]
[ir.append('20191104', idxs, opt, opt_date)
for idxs in range(3, 8)]

#####################################################
opt = 'deliver'

opt_date = '20191104'
[ir.append('20191104', idxs, opt, opt_date)
for idxs in [1, 2]]
[ir.append('20191104', idxs, opt, opt_date)
for idxs in range(3, 8)]

#####################################################
opt = 'deliver'

opt_date = '20190612'
[ir.append('20190103', idxs, opt, opt_date)
for idxs in range(1, 4)]

#####################################################
opt = 'create'

opt_date = '20191129'
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(2, 6)]
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(6, 18)]

#####################################################
opt = 'create'

opt_date = '20191129'
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(18, 22)]
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(22, 33)]

#####################################################
opt = 'destory'

opt_date = '20191129'
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(18, 22)]
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(22, 33)]

#####################################################
opt = 'deliver'

opt_date = '20191129'
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(2, 6)]
[ir.append('20191129', idxs, opt, opt_date)
for idxs in range(6, 18)]


#####################################################
opt = 'create'

opt_date = '20191206'
[ir.append('20191206', idxs, opt, opt_date)
for idxs in [2, 3, 4]]

#####################################################
opt = 'deliver'

opt_date = '20191209'
[ir.append('20191206', idxs, opt, opt_date)
for idxs in [2, 3, 4]]

print()

ir.print_all()
ir.print_close()
ir.print_open()
ir.print_abnormal()
