# Override the debug parameters and display the file/function for each debug call 
#   (useful for finding debug calls you left laying around and forgot about)
debugCount = 0

DISPLAY_FILE = False
DISPLAY_FUNC = False

def debug(var=None, *more_vars, prefix: str='', name=None, merge: bool=False, repr: bool=False, calls: int=0, 
          color: int=1, background: bool=False, itemLimit: int=6, showFunc: bool=False, showFile: bool=False) -> None: # pylint: disable=redefined-builtin
    """Print variable names and values for easy debugging. 

    Call with no parameters to tell if its getting called at all, and call with a only a string to just display the string

    The format goes: Global_debug_counter[file->function()->line_number]: prefix data_type variable_name = variable_value

    Args:
        var: The variable or variables to print
        prefix: An additional string to print for each line
        merge: Put all the variables on the same line
        repr: Use __repr__() instead of __str__()
        calls: If you're passing in a return from a function, say calls=1
        color: 0-5. 5 different preset colors for easy distinction
        background: Use the background color instead of the forground color
        showFunc: Display what function you're calling from
        showFile: Display waht file you're calling from
    """

    #* Make sure to always reset the color back to normal, in case we have an error inside this function
    try:
        from varname import nameof, VarnameRetrievingError
        from inspect import stack
        from os.path import basename

        global debugCount, DISPLAY_FUNC, DISPLAY_FILE
        debugCount += 1

        #* Colors
        # none, blue, green, orange, purple, cyan, alert red
        colors = ['0', '34', '32', '33', '35', '36', '31']
        
        if background:
            color += 10

        c = f'\033[{colors[color]}m'

        if var is None and color != 0:
            print(f'\033[{colors[-1]}m', end='')
        else:
            print(c, end='')


        #* Shorten var if var is a list or a tuple
        variables = ()
        for v in (var, *more_vars):
            if type(v) in (tuple, list, set) and len(v) > itemLimit:
                variables += (str(v[0:round(itemLimit/2)])[:-1] + f', \033[0m...{c} ' + str(v[-round(itemLimit/2):-1])[1:],)
            else:
                variables += (v,)


        #* Get the function, file, and line number of the call
        s = stack()[1]
        stackData = str(s.lineno)

        if DISPLAY_FUNC or showFunc:
            stackData = s.function + '()->' + stackData
        if DISPLAY_FILE or showFile:
            stackData = basename(s.filename) + '->' + stackData

        if var is None:
            print(f'{debugCount}[{stackData}]: HERE! HERE!')
            print('\033[0m', end='')

        try:
            if name is None:
                var_names = nameof(*variables, caller=2+calls)
            else:
                # This should work for tuples too
                if type(name) is list:
                    name = tuple(name)
                var_names = name
        except VarnameRetrievingError as err:
            #* If only a string literal is passed in, display it
            if type(var) is str:
                print(f"{debugCount}[{stackData}]: {prefix} {var}")
                print('\033[0m', end='')
                return
            else:
                raise err

        if not isinstance(var_names, tuple):
            var_names = (var_names, )

        # variables = (var, *more_vars)
        name_and_values = [f"{var_name} = {variables[i]!r}" if repr
                        else f"{var_name} = {variables[i]}"
                        for i, var_name in enumerate(var_names)]

        if merge:
            print(f"{debugCount}[{stackData}]: {prefix}{', '.join(name_and_values)}")
        else:
            for cnt, name_and_value in enumerate(name_and_values):
                print(f"{debugCount}[{stackData}]: {prefix}{type(variables[cnt]).__name__} {name_and_value}")
                debugCount += 1

        print('\033[0m', end='')
    finally:
        print('\033[0m', end='')

#* Set the __repr__ function to the __str__ function of a class. Useful for custom classes with overloaded string functions 
def reprise(obj, *args, **kwargs):
    obj.__repr__ = obj.__str__
    return obj


def percent(percentage):
    ''' Usage: 
        if (percent(50)):
            <has a 50% chance of running>
    '''
    return randint(1, 100) < percentage


def closeEnough(a, b, tolerance):
    return a <= b + tolerance and a >= b - tolerance

