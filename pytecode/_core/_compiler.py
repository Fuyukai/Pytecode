"""
Represents the bytecode compiler.

.. currentmodule:: pytecode._core._compiler
"""
from typing import List, Tuple, Any

import types

import dis


def _simulate_stack(code: list) -> int:
    """
    Simulates the actions of the stack, to check safety.
    This returns the maximum needed stack.
    """

    max_stack = 0
    curr_stack = 0

    def _check_stack(ins):
        if curr_stack < 0:
            raise SystemError("Stack turned negative on instruction: {}".format(ins))
        if curr_stack > max_stack:
            return curr_stack

    # Iterate over the bytecode.
    for instruction in code:
        assert isinstance(instruction, dis.Instruction)
        if instruction.arg is not None:
            try:
                effect = dis.stack_effect(instruction.opcode, instruction.arg)
            except ValueError as e:
                raise SystemError("Invalid opcode `{}` when compiling"
                                   .format(instruction.opcode)) from e
        else:
            try:
                effect = dis.stack_effect(instruction.opcode)
            except ValueError as e:
                raise SystemError("Invalid opcode `{}` when compiling"
                                   .format(instruction.opcode)) from e
        curr_stack += effect
        # Re-check the stack.
        _should_new_stack = _check_stack(instruction)
        if _should_new_stack:
            max_stack = _should_new_stack

    return max_stack


def compile_raw_bytecode(
        bytecode: List[int],
        argcount: int,
        co_consts: Tuple[Any],
        co_names: Tuple[str],
        co_varnames: Tuple[str],
        co_flags: int = 67,
        f_globals: dict = None,
        f_name: str = "<unknown, compiled>",
        f_filename: str = "<unknown, compiled>",
        f_firstline: int = 0
):
    """
    Compiles raw bytecode. This performs zero safety checks when compiling.

    :param bytecode: The list of bytecode instructions to compile. This expects a list of integers.
    :param argcount: The number of arguments this code object takes.
    :param co_consts: The tuple of constants.
    :param co_names: The tuple of names.
    :param co_varnames: The tuple of varnames.
    :param co_flags: The flags for the new code object.
    :param f_globals: The function globals to compile in.
    :param f_name: The name for the function.
    :param f_filename: The filename for the function.
    :param f_firstline: The first line for the function.
    :return:
    """
    if f_globals is None:
        f_globals = globals()

    stack_size = _simulate_stack(dis._get_instructions_bytes(bytecode))
    bc = b"".join(x.to_bytes(1, "big") for x in bytecode)

    obb = types.CodeType(
        argcount,  # Varnames - used for arguments.
        0,  # Kwargs are not supported yet
        len(co_varnames),  # co_nlocals -> Non-argument local variables
        stack_size,  # Auto-calculated
        co_flags,  # 67 is default for a normal function.
        bc,  # co_code
        co_consts,  # co_consts
        co_names,  # co_names, used for global calls.
        co_varnames,  # arguments
        f_filename,  # use <unknown, compiled>
        f_name,  # co_name
        f_firstline,  # co_firstlineno, ignore this.
        b'',  # https://svn.python.org/projects/python/trunk/Objects/lnotab_notes.txt
        (),  # freevars - no idea what this does
        ()  # cellvars - used for nested functions - we don't use these yet.
    )

    fn_obb = types.FunctionType(obb, f_globals)
    return fn_obb