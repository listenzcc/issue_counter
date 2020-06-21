# %% Importing
import os
import pandas as pd
from pprint import pprint

# %% Class


class IssueChecker():
    def __init__(self, recorder_json_path):
        # Init frame by reading from [recorder_json_path]
        frame = pd.read_json(recorder_json_path)
        self.frame = frame.transpose()

        # Init bads
        self.bads = []

    def _prompt(self, msg):
        print(f'>> {msg}')

    def _get_lines(self, frame, column, target, return_mismatch=False):
        # Get lines by column name ------------------------------
        # Get match_lines
        match_idx = frame[column] == target
        match_lines = frame.loc[match_idx]

        # Report
        num_matches = len(match_lines)
        self._prompt(f'Match lines {num_matches}, [{column}] is [{target}].')

        # If return_mismatch, return mismatch lines
        if return_mismatch:
            # Find non target lines
            mismatch_idx = frame[column] != target

            # Mismatch lines
            mismatch_lines = frame.loc[mismatch_idx]
            mismatch_lines.index = range(len(mismatch_lines))

            # Report
            num_mismatches = len(mismatch_lines)
            self._prompt(f'Mismatch lines: {num_mismatches}.')

        # Re-index and Return
        match_lines.index = range(len(match_lines))

        if not return_mismatch:
            return match_lines
        else:
            return match_lines, mismatch_lines

    def _bad_collection(self, obj, reason='', name='--'):
        # Record bads
        # Convert obj into DataFrame if it is Series
        if isinstance(obj, pd.Series):
            obj = pd.DataFrame(obj).transpose()
            obj.index = [0]

        # Set up State and Reason
        obj['State'] = name
        obj['Reason'] = reason

        # Record
        self.bads.append(dict(name=name,
                              reason=reason,
                              value=obj))

        # Report
        self._prompt(f'New bad added: {name}: {reason}')
        self._prompt(f'    {len(self.bads)} bads in total.')

    def _check_repeat(self, lines, reason='Repeat ID in same operation', name='Repeat'):
        # Check the wrong recording of repeat ID in same operation
        # Count IDs
        ID_counts = lines['ID'].value_counts()

        # For repeated IDs
        for _id in ID_counts[ID_counts > 1].index:
            # Remove the repeated lines,
            # and record them in bads
            bad_lines, lines = self._get_lines(lines,
                                               column='ID',
                                               target=_id,
                                               return_mismatch=True)

            # Record bad lines
            self._bad_collection(bad_lines, reason=reason, name=name)

        # Return
        return lines

    def _check_end_before_create(self, lines, reason='Ending without create', name='Invalid ending'):
        # Check had been created
        # Find bad IDs
        bad_ids = []
        for _id in lines['ID']:
            if not _id in self.creates['ID'].values:
                bad_ids.append(_id)

        # Remove lines with bad IDs
        for _id in bad_ids:
            # Remove bad lines
            bad_lines, lines = self._get_lines(lines,
                                               column='ID',
                                               target=_id,
                                               return_mismatch=True)

            # Record bad lines
            self._bad_collection(bad_lines,
                                 reason=reason,
                                 name=name)

        # Return
        return lines

    def _check_creates(self):
        # Get creates
        creates = self._get_lines(self.frame,
                                  column='Opt',
                                  target='Create')

        # Check repeat ID
        creates = self._check_repeat(creates,
                                     reason='Repeat Create')

        # Return
        return creates

    def _check_deliver(self):
        # Get delivers
        delivers = self._get_lines(self.frame,
                                   column='Opt',
                                   target='Deliver')

        # Check repeat ID
        delivers = self._check_repeat(delivers,
                                      reason='Repeat Deliver')

        # Check not in creates
        delivers = self._check_end_before_create(delivers,
                                                 reason='Deliver that has not been creates',
                                                 name='Invalid Deliver')

        # Return
        return delivers

    def _check_destroy(self):
        # Get destroy
        destroy = self._get_lines(self.frame,
                                  column='Opt',
                                  target='Destroy')

        # Check repeat ID
        destroy = self._check_repeat(destroy,
                                     reason='Repeat Destroy')

        # Check not in creates
        destroy = self._check_end_before_create(destroy,
                                                reason='Destory that has not been creates',
                                                name='Invalid Destory')

        # Return
        return destroy

    def _check_close_creates(self):
        # Setup new columns of creates,
        # State refers the operation state of the ID

        # Init new columns
        self.creates['Deliver'] = '--'
        self.creates['Destroy'] = '--'
        self.creates['State'] = 'Open'
        self.creates['Reason'] = '--'

        # For delivers and destroy,
        # obj is delivers or destroy,
        # name is operation name
        for obj, name in [(self.delivers, 'Deliver'),
                          (self.destroy, 'Destroy')]:
            # Walk through all lines
            for j in obj.index:
                # Get ID and Date
                series = obj.loc[j]
                _id = series['ID']
                _date = series['Date']

                # Update columns in creates
                self.creates.loc[_id][name] = _date

                # Change State
                # If current state is 'Closed',
                # switch into Error state of 'Double',
                # meaning 'Invalid operation: Double endings'
                if self.creates.loc[_id]['State'] == 'Closed':
                    self.creates.loc[_id]['State'] = 'Double'
                    self.creates.loc[_id]['Reason'] = 'Invalid operation: Double endings'
                    continue

                # If current state is 'Open',
                # switch into 'Closed'
                if self.creates.loc[_id]['State'] == 'Open':
                    self.creates.loc[_id]['State'] = 'Closed'

                # If operation date is in advance of creating date,
                # switch into 'Invalid',
                # meaning 'Invalid operation: {name} before creating'
                if _date < self.creates.loc[_id]['Date']:
                    self.creates.loc[_id]['State'] = 'Invalid'
                    self.creates.loc[_id]['Reason'] = f'Invalid operation: {name} before create'
                    continue

        # Get opens and closes,
        # remaining is bads
        self.opens, mix = self._get_lines(self.creates,
                                          column='State',
                                          target='Open',
                                          return_mismatch=True)

        self.closes, bads = self._get_lines(mix,
                                            column='State',
                                            target='Closed',
                                            return_mismatch=True)

        # Record red light lines as bad lines
        for _id in bads.index:
            se = bads.loc[_id]
            self._bad_collection(se,
                                 reason=se['Reason'],
                                 name=se['State'])

    def check(self):
        self.creates = self._check_creates()
        self.delivers = self._check_deliver()
        self.destroy = self._check_destroy()

        self.creates = self.creates.set_index('ID', drop=False)
        self.creates.index = [e for e in self.creates.index]

        self._check_close_creates()

    def save_checked(self, dirpath):
        self.delivers = self.closes[self.closes.Destroy == '--']
        self.destroy = self.closes[self.closes.Deliver == '--']

        self.delivers.transpose().to_json(
            os.path.join(dirpath, 'delivers.json'))
        self.destroy.transpose().to_json(
            os.path.join(dirpath, 'destroy.json'))
        self.opens.transpose().to_json(
            os.path.join(dirpath, 'opens.json'))

    def save_creates(self, dirpath):
        creates = self.creates.copy()
        creates.pop('ID')
        creates.to_json(os.path.join(dirpath, 'creates.json'))
        creates.to_html(os.path.join(dirpath, 'creates.html'))

    def save_bads(self, dirpath):
        bads = pd.concat([e['value'] for e in self.bads])
        bads.index = [e for e in range(len(bads))]
        bads.transpose().to_json(os.path.join(dirpath, 'bads.json'))

    def pprint(self):
        # Print using pprint
        pprint(self.frame)


class IssueRecorder():
    # Record issues into frame
    def __init__(self, quiet=False):
        # Init -------------------------------------
        # Prefix for ID
        self.prefix = 'Z-L19'

        # Init frame
        self.frame = pd.DataFrame(columns=['Date', 'ID', 'Opt', 'Material'])

        # Quiet switcher
        self.quiet = quiet

    def _prompt(self, msg, force_print=False):
        # Print method,
        # print if not quiet,
        # print if force_print
        if any([force_print,
                not self.quiet]):
            print(f'>> {msg}')

    def _add_row_in_place(self, obj):
        # Add obj into frame in-place
        # Add in-place with ignore_index=True
        self.frame = self.frame.append(pd.Series(obj), ignore_index=True)

        # Report current state
        num_lines = len(self.frame)
        self._prompt(f'Added new line into frame, {num_lines} lines in all.')

    def append(self, date, idxs, opt, opt_date, material='--'):
        # Append new line based on inputs
        # date: Date of ID
        # idxs: indexes of ID
        # opt: Operation name of ID
        # opt_date: Operation date
        # material: Material name, only valid when opt is 'Create'

        # Covert idxs from {int} to {list}
        if isinstance(idxs, int):
            idxs = [idxs]

        # Iterate over idxs
        for idx in idxs:
            # Make dict obj
            new_item = dict(
                Date=opt_date,
                Material=material,
                Opt=opt.title(),
                ID=f'{self.prefix}-{date}-{idx:03d}'
            )

            # Add new line based on obj
            self._add_row_in_place(new_item)

        # Report
        self._prompt(f'Added {len(idxs)} lines.')

    def save_recorder(self, path):
        # Save frame into json file
        # Regulate fname
        if not path.endswith('.json'):
            path = path + '.json'

        # Save
        # Transpose frame to human readable,
        # and save
        self.frame.transpose().to_json(path)

        # Report
        self._prompt(f'Save frame into {path}', force_print=True)

    def pprint(self):
        # Print using pprint
        pprint(self.frame)
