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
from threading import Thread 

namespace = globals()

def createOptionMenu(*instances, getGlobal=True, windowName='Options', sort=True, nonBlocking=False, **names):
    members = {}
    
    if 'Global' in names.keys():
        names['NoneType'] = names['Global']

    if getGlobal:
        instances += (None,)

    for i in instances:
        members[i] = getOptions(i)
        if sort:
            members[i].sort()

    if getGlobal:
        members[None] = getOptions(namespace=namespace)
        if sort:
            members[None].sort()

    className = lambda var: var.__class__.__name__

    # Tkinter is not (sorta) thread safe
    if nonBlocking and False:
        thread = Thread(target=lambda: OptionsMenu(tk.Tk(className=windowName), *[[className(i) if className(i) not in names.keys() else names[className(i)]] + members[i] for i in instances]).mainloop()) 
        thread.start()
        thread.join()
    else:
        OptionsMenu(tk.Tk(className=windowName), *[[className(i) if className(i) not in names.keys() else names[className(i)]] + members[i] for i in instances]).mainloop()

    time.sleep(.15) # Escape debouncing
