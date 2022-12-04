import inspect
import os


def ltrace(stack_limit: int = -1) -> str:
    if stack_limit > -1:
        stack_limit += 1

    frames = inspect.getouterframes(inspect.currentframe(), 3)[2:]
    out_str = [f"-debug <error_origin>: "]
    max_1, max_2, max_3 = (0, 0, 0)
    # This gets the things for inline formatting {text:{index}}
    for frame in frames[:stack_limit]:
        if len(os.path.basename(frame[1])) > max_1:
            max_1 = len(os.path.basename(frame[1]))
        if len(frame[3]) > max_2:
            max_2 = len(frame[3])
        if len(str(frame[2])) > max_3:
            max_3 = len(str(frame[2]))

    for frame in frames:
        out_str.append(f"{os.path.basename(frame[1]):{max_1}} │ "
                       f"{frame[3] + '()':{max_2 + 2}} │ "
                       f"Line {frame[2]:{max_3}}")

    if stack_limit > -1:
        return "\n\t".join(out_str[:stack_limit])
    else:
        return "\n\t".join(out_str)
