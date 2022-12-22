import func_list
from colorama import Fore, Style


def list_all_functions():
    callables = [fn for fn in dir(func_list) if not fn.startswith("__")]
    callables.sort()

    # callables = [call for call in callables if not isinstance(getattr(func_list, call), module)]
    for call_name in callables:
        call = getattr(func_list, call_name)

        # If it's not a directory
        if call.__annotations__:
            # If call is a class
            call_name = Fore.BLUE + call_name + Style.RESET_ALL

            key_type_pair_list = [f'{Fore.GREEN + key + Style.RESET_ALL}: {type_hint.__name__}'
                                  for key, type_hint in call.__annotations__.items() if key != "return"]

            if type(call) == type:
                call_name = Fore.RED + "class " + Style.RESET_ALL + call_name
                key_type_pairs = '\n\t'.join(key_type_pair_list)
                print(f"{call_name}:\n\t{key_type_pairs}")

            # If call is a function
            else:
                call_name = Fore.RED + "function " + Style.RESET_ALL + call_name
                key_type_pairs = ", ".join(key_type_pair_list)
                print(f"{call_name}({key_type_pairs}) -> {call.__annotations__.pop('return').__name__}")

            if call.__doc__:
                print(Fore.GREEN + '"' +
                      call.__doc__.strip("\n ") +
                      '"' + Style.RESET_ALL)
            else:
                print(Fore.RED + "<Documentation missing>" + Style.RESET_ALL)
            print("")


if __name__ == '__main__':
    list_all_functions()
