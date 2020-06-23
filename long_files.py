
def batch_add_issues(ir):
    ####################################################
    # Append: date, idxs, opt, opt_date, material='--'):
    # date: date of ID
    # idxs: list of ID index
    # opt: operation: create, deliver, destroy
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
    opt = 'destroy'

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
    opt = 'destroy'

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
    opt = 'deliver'

    opt_date = '20190911'
    [ir.append('20181229', idxs, opt, opt_date)
     for idxs in [6]]

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
     for idxs in range(22, 34)]

    #####################################################
    opt = 'destroy'

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

    ######################################################
    opt = 'create'

    opt_date = '20200401'
    [ir.append('20200401', idxs, opt, opt_date)
     for idxs in [1, 2]]
    [ir.append('20200402', idxs, opt, opt_date)
     for idxs in [1, 2]]

    ######################################################
    opt = 'destroy'

    opt_date = '20200402'
    [ir.append('20200401', idxs, opt, opt_date)
     for idxs in [1, 2]]


def batch_add_test_issues(ir):
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
    # create repeat 9
    record = dict(
        opt='create',
        date='20200406',
        idxs=9,
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
    # destroy 3 (conflict)
    record = dict(
        opt='destroy',
        date='20200406',
        idxs=3,
        opt_date='20200503',
        material='example'
    )

    ir.append(**record)

    ####################################################
    # deliver 3 (conflict)
    record = dict(
        opt='deliver',
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
    # destroy before create 7
    record = dict(
        opt='destroy',
        date='20200406',
        idxs=7,
        opt_date='20200313',
        material='example'
    )

    ir.append(**record)

    ####################################################
    # destroy twice 7
    # destroy not created 13
    record = dict(
        opt='destroy',
        date='20200406',
        idxs=[7, 13],
        opt_date='20200803',
        material='example'
    )

    ir.append(**record)
