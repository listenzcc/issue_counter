# %% Importing
import os
import pandas as pd
from pprint import pprint

# %% Class


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
        pprint(self.frame)
