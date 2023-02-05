from production.cti.classes import *


def result_to_cti(result_list: List[Tuple[str, Any]]):
    out_tokens = list([])

    for ltoken in result_list:
        name = ltoken[0]

        instruction = ltoken_to_instruction(name, ltoken[1:])

        if len(out_tokens) == 0:
            out_tokens.append(instruction)
            continue

        if not out_tokens[-1].can_combine(instruction):
            out_tokens.append(instruction)
            continue

        old_instruction = out_tokens.pop(-1)
        new_instruction = old_instruction.combine(instruction)

        out_tokens += new_instruction

    return out_tokens
