from typing import Dict, Set, Optional, List, Tuple, Any
from common.datatypes import *
from dataclasses import dataclass

from common.iterator.named_result import NamedResult
from common.iterator.rule import Rule


@dataclass
class Frame:
    # The frame contains all external information, like expose and include
    exposed_variables: Optional[Value_List[Token]]
    exposing_conditions: Optional[Value_List[int]]
    linked_files: Dict[Token, Name]

    def __init__(self):
        self.exposed_variables = None
        self.exposing_conditions = None
        self.linked_files = dict()


@dataclass
class Bottle:
    start: NamedResult
    variables: Dict[Name, Value]
    match_groups: Dict[Token, Value_List[Token]]
    context_ignore: Set[Token]
    frame: Frame
    rule_assignments: Set[Name]
    rule_list: List[Rule]
    named_results: List[NamedResult]

    def __init__(self):
        self.rule_list = list()
        self.named_results = list()
        self.rule_assignments = set()
        self.context_ignore = set()
        self.variables = dict()
        self.match_groups = dict()
        self.frame = Frame()

    def add_variable(self, variable_name: Name, variable_value: Value):
        if variable_name in self.variables:
            raise ValueError(f"Variable {variable_name} already defined.")

        self.variables[variable_name] = variable_value

    def token_already_exists(self, ltoken: Token):
        if ltoken in self.match_groups.keys():
            return True

        if ltoken in self.frame.linked_files.keys():
            return True

        return False
