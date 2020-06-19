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

    def _get_lines(self, frame, column, target, return_mismatch=False):
        # Get lines by column name ------------------------------
        # Get match_lines
        match_idx = frame[column] == target
        match_lines = frame.loc[match_idx]

        # Report
        num_matches = len(match_lines)
        print(f'Match lines {num_matches}, [{column}] is [{target}].')

        # If return_mismatch, return mismatch lines
        if return_mismatch:
            # Find non target lines
            mismatch_idx = frame[column] != target

            # Mismatch lines
            mismatch_lines = frame.loc[mismatch_idx]
            mismatch_lines.index = range(len(mismatch_lines))

            # Report
            num_mismatches = len(mismatch_lines)
            print(f'Mismatch lines: {num_mismatches}.')

        # Re-index and Return
        match_lines.index = range(len(match_lines))

        if not return_mismatch:
            return match_lines
        else:
            return match_lines, mismatch_lines

    def _bad_collection(self, obj, reason='', name='--'):
        self.bads.append(dict(name=name,
                              reason=reason,
                              value=obj))
        print(f'New bad added: {name}: {reason}')
        print(f'    {len(self.bads)} in total.')

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
            self._bad_collection(bad_lines, reason=reason, name=name)

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

        # Check had been created
        bad_ids = []
        for _id in destroy['ID']:
            if not _id in self.creates['ID'].values:
                bad_ids.append(_id)

        for _id in bad_ids:
            bad_lines, destroy = self._get_lines(destroy,
                                                 column='ID',
                                                 target=_id,
                                                 return_mismatch=True)
            self._bad_collection(bad_lines,
                                 reason='Destory that has not been created',
                                 name='Invalid Destory')

        # Return
        return destroy

    def check(self):
        self.creates = self._check_creates()
        self.delivers = self._check_deliver()
        self.destroy = self._check_destroy()
        pass

    def pprint(self):
        # Print using pprint
        pprint(self.frame)


class IssueRecorder():
    # Record issues into frame
    def __init__(self, save_path='.', quiet=False):
        # Init -------------------------------------
        # Prefix for ID
        self.prefix = 'Z-L19'

        # Save path
        self.save_path = save_path

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

    def save_recorder(self, fname):
        # Save frame into json file
        # Regulate fname
        if not fname.endswith('.json'):
            fname = fname + '.json'

        # Prepare full path
        path = os.path.join(self.save_path, fname)

        # Save
        # Transpose frame to human readable
        self.frame.transpose().to_json(path)

        # Report
        self._prompt(f'Save frame into {path}', force_print=True)

    def pprint(self):
        # Print using pprint
        pprint(self.frame)
