# %% Importing
# System
import os

# Local tools
from local_toolbox import IssueRecorder, IssueChecker
from long_files import batch_add_issues, batch_add_test_issues

# Settings
SAVE_PATH = 'C:\\Users\\liste\\Documents\\issue_counter\\reports'
QUIET = True
RECORDER_NAME = 'recorder.json'

# %% Main part
ir = IssueRecorder(save_path=SAVE_PATH, quiet=QUIET)

batch_add_test_issues(ir)

ir.pprint()
ir.save_recorder(RECORDER_NAME)

# %%
ic = IssueChecker(recorder_json_path=os.path.join(SAVE_PATH, RECORDER_NAME))
ic.check()
ic.frame

# %%
ic.bads

# %%
ic.creates

# %%
ic.delivers

# %%
ic.destroy

# %%
