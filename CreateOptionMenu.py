#* Import everything

# import glob
# import importlib
# files = glob.glob('*')
# files.remove('main.py')
# files.remove('Game.py')

# for i in files:
#     if i.endswith('.py'):
#         importlib.import_module(i[:-3])

from TkOptionMenu import *
from TkOptions import *
from Ant import *
from AntScene import *
from TkOptionMenu import *

namespace = globals()

def createOptionMenu(*classes, getGlobal=True, windowName='Options', sort=True, **names):
    members = {}
    
    if 'Global' in names.keys():
        names['NoneType'] = names['Global']

    if getGlobal:
        classes += (type(None),)

    for i in classes:
        members[i] = getOptions(i)
        if sort:
            members[i].sort()

    if getGlobal:
        members[type(None)] = getOptions(namespace=namespace)
        if sort:
            members[type(None)].sort()

    # print(getOptions(namespace=namespace))

    OptionsMenu(tk.Tk(className=windowName), *[[i.__name__ if i.__name__ not in names.items() else names[i.__name__]] + members[i] for i in classes]).mainloop()
    time.sleep(.15) # Escape debouncing
