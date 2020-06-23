# %% Importing
import os
import pandas as pd
from pprint import pprint

# %% Class


class IssueSorter():
    def __init__(self, frame):
        self.frame = frame
        self.calendar = dict()

    def _empty_page(self):
        return pd.DataFrame(columns=['ID', 'Material', 'Options', 'Notes', 'State'])

    def _append_page(self, date, ID, material, option, note=''):
        page = self.calendar.get(date, self._empty_page())

        if ID in page['ID'].values:
            page.loc[page['ID'] == ID]['Options'].iloc[0].append(option)
            page.loc[page['ID'] == ID]['Notes'].iloc[0].append(note)
            if '--' == page.loc[page['ID'] == ID]['Material'].iloc[0]:
                page.loc[page['ID'] == ID]['Material'].iloc[0] = material
        else:
            page = page.append(dict(ID=ID,
                                    Material=material,
                                    Options=[option],
                                    Notes=[note]), ignore_index=True)

        self.calendar[date] = page

    def _fill_calendar(self):
        for j in self.frame.index:
            line = self.frame.loc[j]
            date = line['ID'].split('-')[2]
            opt_date = line['Date']

            self._append_page(date=date,
                              ID=line['ID'],
                              material=line['Material'],
                              option=(line['Opt'], opt_date),
                              note=f'{j}')

    def pprint(self, fpath=None):
        for date in self.calendar:
            print(f'---- {date} ----')
            try:
                display(self.calendar[date])
            except:
                pprint(self.calendar[date])

        if fpath is not None:
            with open(fpath, 'w') as f:
                for date in self.calendar:
                    f.write(f'<h2> {date} </h2>\n\n')
                    f.writelines(self.calendar[date].to_html())
                    f.write('\n\n')

    def check(self):
        # Check all the calendar
        # For all date
        for date in self.calendar:
            # Reset nan values
            self.calendar[date][self.calendar[date].isna()] = '--'

            # For every line
            for j in self.calendar[date].index:
                # Check options
                options = self.calendar[date].loc[j]['Options']

                # Only have Create:
                # Open case
                if all([len(options) == 1,
                        options[0][0] == 'Create']):
                    self.calendar[date].loc[j]['State'] = 'Open'
                    continue

                # Only have one option and it is not Create:
                # Error case
                if len(options) == 1:
                    self.calendar[date].loc[j]['State'] = 'Error'
                    continue

                # Have more than two options:
                # Error case
                if len(options) != 2:
                    self.calendar[date].loc[j]['State'] = 'Error'
                    continue

                # Complicate check
                create_count = 0
                for k, opt in enumerate(options):
                    if opt[0] == 'Create':
                        create_count += 1
                        create_idx = k

                # Have 0 or 2 Create options:
                # Error case
                if create_count != 1:
                    self.calendar[date].loc[j]['State'] = 'Error'
                    continue

                # Create after non-create option:
                # Error case
                non_create_idx = (create_idx + 1) % 2
                if options[non_create_idx][1] < options[create_idx][1]:
                    self.calendar[date].loc[j]['State'] = 'Error'
                    continue

                # Finally,
                # Closed case
                self.calendar[date].loc[j]['State'] = 'Closed'


# %% IssueRecorder


class IssueRecorder():
    # Record issues into frame
    def __init__(self, frame_path=None, quiet=False):
        # Init -------------------------------------
        # Prefix for ID
        self.prefix = 'Z-L19'

        # Init frame
        if frame_path is None:
            self.frame = pd.DataFrame(
                columns=['Date', 'ID', 'Opt', 'Material'])
        else:
            self.frame = pd.read_json(frame_path).transpose()

        # Quiet switcher
        self.quiet = quiet

    def summary(self):
        return self.frame.describe()

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
