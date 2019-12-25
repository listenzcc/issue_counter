import os
import pandas as pd

class IssueRecorder():
    def __init__(self, report_path='.'):
        # ID prefix
        self.prefix = 'Z-L19'
        self.report_path = report_path
        if not os.path.exists(self.report_path):
            os.mkdir(self.report_path)
        # Main dataframe
        self.df = pd.DataFrame(columns=['create', 'deliver', 'destory', 'material'])

    def append(self, date, idxs, opt, opt_date, material='paper'):
        # Append new issue
        # date: date of ID
        # idxs: list of ID index
        # opt: operation: create, deliver, destory
        # opt_date: operating date

        # idxs should be a list
        if type(idxs) is int:
            idxs = [idxs]

        # For each index
        for idx in idxs:
            # Issue name
            name = '{prefix}-{date}-{idx:03d}'.format(prefix=self.prefix, date=date, idx=idx)
            print(name)
            # Build series
            se = pd.Series(name=name, data={opt: opt_date, 'material': material})
            print(se)
            # Append series into main dataframe
            self.df = self.df.append(se)

    def check(self):
        # Walk throught main dataframe, and check issues
        self.df = self.df.fillna('--')
        # Init bug list
        self.bugs = []
        self.checked = pd.DataFrame(columns=['create', 'deliver', 'destory'])
        # For each issue name
        for name in self.df.index.unique():
            # There should be several records for certain issue name
            ses = self.df.loc[name]
            print(ses)
            # If closed well, print pass,
            # if not, print bug and record into bug list
            if self.check_finish(ses):  # len(ses) == 2:
                print('Pass.')
            else:
                print('Bug.')
                self.bugs.append(name)

    def check_finish(self, ses):
        # Check if the session closed
        # ses: a series of certain issue name
        
        # name: Issue name
        name = ses.index.unique()
        if len(name) > 1:
            return False
        name = name[0]
        
        # A closed session should contain exactly 2 records
        if not len(ses) == 2:
            return False
        
        # a, b: two records
        a = ses.iloc[0].to_dict()
        b = ses.iloc[1].to_dict()
        
        # The issue in a closed session should not be created twice
        if all([a['create'] == '--', b['create'] == '--']):
            return False
        
        # data: data of circle report of the issue
        data = dict(
            create = '--',
            deliver = '--',
            destory = '--',
        )
        # Fill data using a and b
        if a['create'] == '--':
            data['create'] = b['create']
            if a['destory'] == '--':
                data['deliver'] = a['deliver']
            else:
                data['destory'] = a['destory']
        else:
            data['create'] = a['create']
            if b['destory'] == '--':
                data['deliver'] = b['deliver']
            else:
                data['destory'] = b['destory']
        
        # Check if creating date is in front of delivering or destorying.
        d = 'deliver'
        if data['deliver'] == '--':
            d = 'destory'
            if data['create'] > data[d]:
                return False
            
        # The issue is fine, record it into checked
        self.checked = self.checked.append(pd.Series(name=name, data=data))
        return True
    
    def logging(self, message, fp, to_html=False):
        print(message)
        if to_html:
            message = message.to_html()
        print('\n'.join(['<div>', message, '</div>']), file=fp)
    
    def report_finish(self):
        with open(os.path.join(self.report_path, 'finish.html'), 'w') as fp:
            self.checked.to_html(fp, index=True)

    def report_bugs(self):
        with open(os.path.join(self.report_path, 'bugs.html'), 'w') as fp:
            self.logging('=' * 80, fp)
            self.logging('Bugs report.', fp)
            for name in self.bugs:
                self.logging('-' * 80, fp)
                self.logging(self.df.loc[name], fp, to_html=True)