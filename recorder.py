# %% Importing
# System
import os
from pprint import pprint

# Local tools
from local_toolbox import IssueRecorder, IssueSorter
from long_files import batch_add_issues, batch_add_test_issues

# Settings
SAVE_PATH = os.path.join(os.path.dirname(__file__), 'reports')
QUIET = True
RECORDER_NAME = 'recorder.json'
SORTED_HTML_NAME = 'sorted.html'

# %% Recording
recorder = IssueRecorder(quiet=QUIET)

batch_add_issues(recorder)

recorder.save_recorder(path=os.path.join(SAVE_PATH, RECORDER_NAME))

# %% Sorting
sorter = IssueSorter(recorder.frame)
sorter._fill_calendar()
sorter.check()

# %%
sorter.pprint(fpath=os.path.join(SAVE_PATH, SORTED_HTML_NAME),
              startdate='20200000'.replace('0', '0'))

# %%


# %%
