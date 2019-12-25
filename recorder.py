from local_toolbox import IssueRecorder

ir = IssueRecorder('C:\\Users\\liste\\Documents\\issue_counter\\reports')

####################################################
# Append: date, idxs, opt, opt_date, material='--'):
# date: date of ID
# idxs: list of ID index
# opt: operation: create, deliver, destory
# opt_date: operating date

####################################################
opt = 'create'

date = '20181229'
[ir.append(date, idxs, opt, date, material)
 for idxs, material in [[range(1, 7), 'paper'],
                        [range(7, 9), 'paper'],
                        [range(9, 11), 'paper'],
                        [range(11, 13), 'cd'],
                        [13, 'paper']]]

date = '20190102'
[ir.append(date, idxs, opt, date, material)
 for idxs, material in [[range(1, 7), 'paper'],
                        [range(7, 9), 'paper'],
                        [9, 'cd']]]

date = '20190103'
[ir.append(date, idxs, opt, date, material)
 for idxs, material in [[range(1, 3), 'paper'],
                        [3, 'cd']]]

date = '20190319'
[ir.append(date, idxs, opt, date, material)
 for idxs, material in [[range(1, 5), 'paper'],
                        [5, 'cd'],
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

######################################################
opt = 'create'

opt_date = '20191223'
[ir.append('20191223', idxs, opt, opt_date)
 for idxs in [1]]

######################################################
opt = 'deliver'

opt_date = '20191223'
[ir.append('20191223', idxs, opt, opt_date)
 for idxs in [1]]

print('done')

ir.check()

ir.report_finish()
ir.report_bugs()