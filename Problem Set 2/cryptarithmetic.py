from itertools import combinations
from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]
        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS
        LHS0=LHS0[::-1]
        RHS=RHS[::-1]
        LHS1=LHS1[::-1]
        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        problem.constraints = []
        problem.domains = {}
        problem.variables = list(set(LHS0 + LHS1 + RHS))
        
        #commonly used ranges for domains 
        digit_set = set(range(10))
        non_zero_digit_set = set(range(1, 10))
        carry_set = set(range(2))
        medium_set = set(range(100))-{x * 11 for x in range(10)}
        small_sum_set = set(range(20))

        large_sum_set = set(range(200))-{x * 11 for x in range(10)}-set(range(111, 200, 11))
        
        # Add "all-different" constraints
        problem.constraints.extend(
            [BinaryConstraint((var1, var2), lambda a, b: a != b) for var1, var2 in combinations(problem.variables, 2)]
        )
    
        # Assign domains to variables            
        for variable in problem.variables:
            if variable in (LHS0[-1], LHS1[-1], RHS[-1]):
                problem.domains[variable] = non_zero_digit_set
            else:
                problem.domains[variable] = digit_set

        
        max_len = max(len(LHS0), len(LHS1))
        min_len = min(len(LHS0), len(LHS1))
        max_lhs = LHS1 if len(LHS1) > len(LHS0) else LHS0


        problem.constraints.append(BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", f"{RHS[0]}C{0}"), lambda a, b: (a % 10 + a // 10) == b % 10 + 10 * (b // 10)  ))
        problem.variables.append(f"{LHS1[0]}{LHS0[0]}")
        problem.domains[f"{LHS1[0]}{LHS0[0]}"] = medium_set if LHS0[0] != LHS1[0] else {x * 11 for x in range(10)}
        problem.constraints.extend([
        BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", LHS1[0]), lambda a, b: a // 10 == b),
        BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", LHS0[0]), lambda a, b: a % 10 == b)])                    

        for i in range(max_len):
           
            # Handle carries
            carry_var = f"C{i}"
            problem.variables.append(carry_var)
            problem.domains[carry_var] = carry_set

            sum_var = f"{RHS[i]}C{i}"
            problem.variables.append(sum_var)
            problem.domains[sum_var] = small_sum_set
            problem.constraints.extend([
              BinaryConstraint((sum_var, carry_var), lambda a, b: a // 10 == b),
              BinaryConstraint((sum_var, RHS[i]), lambda a, b: a % 10 == b)])

            if i < min_len - 1:
                combined_var = f"{LHS1[i+1]}{LHS0[i+1]}"
                problem.variables.append(combined_var)
                problem.domains[combined_var] = medium_set if LHS0[i+1] != LHS1[i+1] else {x * 11 for x in range(10)}
                problem.constraints.extend([
               BinaryConstraint((combined_var, LHS1[i+1]), lambda a, b: a // 10 == b),
               BinaryConstraint((combined_var, LHS0[i+1]), lambda a, b: a % 10 == b)])                    

                next_combined_var = f"{LHS1[i+1]}{LHS0[i+1]}C{i}"
                problem.variables.append(next_combined_var)
                problem.domains[next_combined_var] = (
                    large_sum_set 
                    if LHS0[i + 1] != LHS1[i + 1] 
                    else {x * 11 for x in range(10)} | set(range(111, 200, 11))
                )

                problem.constraints.extend([
                    BinaryConstraint((next_combined_var, f"{LHS1[i+1]}{LHS0[i+1]}"), lambda a, b: a % 100 == b),
                    BinaryConstraint((next_combined_var, carry_var), lambda a, b: a // 100 == b),
                    BinaryConstraint((next_combined_var, f"{RHS[i+1]}C{i+1}"), lambda a, b: (
                        a // 100 + (a % 100) // 10 + (a % 100) % 10 == b % 10 + 10 * (b // 10)
                    ))
                ])
            elif i < len(max_lhs) - 1:
                max_var = f"{max_lhs[i+1]}C{i}"
                problem.variables.append(max_var)
                problem.domains[max_var] = small_sum_set
                problem.constraints.extend([
              BinaryConstraint((max_var, max_lhs[i+1]), lambda a, b: a % 10 == b),
              BinaryConstraint((max_var, carry_var), lambda a, b: a // 10 == b),
              BinaryConstraint((max_var, f"{RHS[i+1]}C{i+1}"), lambda a, b: (
                    a // 10 + a % 10 == b % 10 + 10 * (b // 10)
                ))])

        if len(RHS) > max_len :
            problem.constraints.append(BinaryConstraint((RHS[-1], f"C{max_len-1}"), lambda a, b: a == b))
       
        return problem


    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())