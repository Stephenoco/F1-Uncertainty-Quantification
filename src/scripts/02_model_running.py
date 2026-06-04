# Source - https://stackoverflow.com/a/68728574
# Posted by amicitas, modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-04, License - CC BY-SA 4.0

from json import load

filename = '../notebooks/03_training.ipynb'
with open(filename) as fp:
    nb = load(fp)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(line for line in cell['source'] if not line.startswith('%'))
        exec(source, globals(), locals())


filename = '../notebooks/04_evaluation.ipynb'
with open(filename) as fp:
    nb = load(fp)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(line for line in cell['source'] if not line.startswith('%'))
        exec(source, globals(), locals())
