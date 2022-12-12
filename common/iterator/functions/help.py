import func_list
from colorama import Fore, Style


def list_all_functions():
    callables = [fn for fn in dir(func_list) if not fn.startswith("__")]
    callables.sort()

    # callables = [call for call in callables if not isinstance(getattr(func_list, call), module)]
    for call_name in callables:
        call = getattr(func_list, call_name)

        # If its not a directory
        if call.__annotations__:
            # If call is a class
            call_name = Fore.BLUE + call_name + Style.RESET_ALL

            key_type_pair_list = [f'{Fore.GREEN + key + Style.RESET_ALL}: {type_hint.__name__}'
                                  for key, type_hint in call.__annotations__.items()]

            if type(call) == type:
                key_type_pairs = '\n\t'.join(key_type_pair_list)
                print(f"{call_name}:\n\t{key_type_pairs}")

            # If call is a function
            else:
                key_type_pairs = ", ".join(key_type_pair_list)
                print(f"{call_name}({key_type_pairs})")

            if call.__doc__:
                print(Fore.GREEN + '"' +
                      call.__doc__.strip("\n ") +
                      '"' + Style.RESET_ALL)
            print("")


if __name__ == '__main__':
    list_all_functions()
