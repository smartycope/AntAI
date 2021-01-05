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
# from TkOptionMenu import *
from threading import Thread 

namespace = globals()

# nonBlocking does not work
def createOptionMenu(*instances, getGlobal=True, windowName='Options', sort=True, nonBlocking=False, trackers=True, **names):
    members = {}
    trackers = {}
    
    #* Rename the Global key from **name, to be more human readable
    if 'Global' in names.keys():
        names['NoneType'] = names['Global']

    #* Mark global as something to get
    if getGlobal:
        instances += (None,)

    #* Go through the classes passed in, get all the options from them, and add them to members under their key (and sort them)
    for i in instances:
        members[i] = getOptions(i)
        if sort:
            members[i].sort()

    #* Do the same with global variables
    if getGlobal:
        members[None] = getOptions(namespace=namespace)
        if sort:
            members[None].sort()

    #* Go through the classes passed in, get all the trackers from them, and add them to trackers under their key (and sort them)
    for i in instances:
        trackers[i] = getTrackers(i)
        if sort:
            trackers[i].sort()

    #* Do the same with global variables
    if getGlobal:
        trackers[None] = getTrackers(namespace=namespace)
        if sort:
            trackers[None].sort()

    #* A quick function to make it more readable
    className = lambda var: var.__class__.__name__

    # Tkinter is not (sorta) thread safe
    if nonBlocking and False:
        thread = Thread(target=lambda: OptionsMenu(tk.Tk(className=windowName), 
                    *[[className(i) if className(i) not in names.keys() else names[className(i)]] + members[i] for i in instances]
                ).mainloop()) 

        thread.start()
        thread.join()
    else:
        #* For everything in instances, if the instance name is in names, use it. Otherwise, use it's classname. 
        #   Then add that to the beginning of the list of Options stored at the appropriate key in members
        lists    = [[className(i) if className(i) not in names.keys() else names[className(i)]] + members[i]  for i in instances]
        trackers = [[className(i) if className(i) not in names.keys() else names[className(i)]] + trackers[i] for i in instances]
        OptionsMenu(tk.Tk(className=windowName), *lists, *trackers).mainloop()

    # Escape debouncing
    time.sleep(.15)
