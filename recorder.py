# %% Importing

from local_toolbox import IssueRecorder
from long_files import add_issues

# %% Main part
ir = IssueRecorder(save_path='C:\\Users\\liste\\Documents\\issue_counter\\reports',
                   quiet=True)

add_issues(ir)

ir.pprint()

ir.save_recorder('recoder.json')
