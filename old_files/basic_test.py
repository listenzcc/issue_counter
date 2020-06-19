from local_toolbox import IssueRecorder

ir = IssueRecorder('C:\\Users\\liste\\Documents\\issue_counter\\basic_test')

####################################################
# Append: date, idxs, opt, opt_date, material='--'):
# date: date of ID
# idxs: list of ID index
# opt: operation: create, deliver, destory
# opt_date: operating date

####################################################
# create
record = dict(
    opt='create',
    date='20200406',
    idxs=[1, 3, 5, 7, 9],
    opt_date='20200406',
    material='example'
)

ir.append(**record)

####################################################
# deliver 1
record = dict(
    opt='deliver',
    date='20200406',
    idxs=1,
    opt_date='20200501',
    material='example'
)

ir.append(**record)

####################################################
# destory 3
record = dict(
    opt='destory',
    date='20200406',
    idxs=3,
    opt_date='20200503',
    material='example'
)

ir.append(**record)

####################################################
# deliver before create 5
record = dict(
    opt='deliver',
    date='20200406',
    idxs=5,
    opt_date='20200303',
    material='example'
)

ir.append(**record)

####################################################
# destory before create 7
record = dict(
    opt='destory',
    date='20200406',
    idxs=7,
    opt_date='20200313',
    material='example'
)

ir.append(**record)

####################################################
# destory twice 7
# destory not created 13
record = dict(
    opt='destory',
    date='20200406',
    idxs=[7, 13],
    opt_date='20200803',
    material='example'
)

ir.append(**record)

print('done')

########################################################
# check
ir.check()

ir.report_finish()
ir.report_bugs()
