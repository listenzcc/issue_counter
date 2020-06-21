# %% Importing
# System
import os

# Local tools
from local_toolbox import IssueRecorder, IssueChecker
from long_files import batch_add_issues, batch_add_test_issues

# Settings
SAVE_PATH = os.path.join(os.path.dirname(__file__), 'reports')
QUIET = True
RECORDER_NAME = 'recorder.json'
CREATES_NAME = 'creates'

# %% Main part
ir = IssueRecorder(quiet=QUIET)

# batch_add_test_issues(ir)
batch_add_issues(ir)

ir.pprint()
ir.save_recorder(path=os.path.join(SAVE_PATH, RECORDER_NAME))

# %%
ic = IssueChecker(recorder_json_path=os.path.join(SAVE_PATH, RECORDER_NAME))
ic.check()
ic.save_creates(name=os.path.join(SAVE_PATH, CREATES_NAME))
ic.save_checked(dirpath=SAVE_PATH)

# %%
ic.bads

# %%
ic.creates

# %%
ic.closes

# %%
ic.opens

# %%
