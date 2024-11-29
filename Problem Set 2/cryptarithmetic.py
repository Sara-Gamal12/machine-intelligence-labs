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
        # Reverse the strings to make it easier to work with
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
        #set for carry 
        carry_set = set(range(2))
      #set for carry + digit
        small_sum_set = set(range(20))
        #set for carry + 2 different digits
        medium_set = set(range(100))-{x * 11 for x in range(10)}
        #set for carry + 3 different digits
        large_sum_set = set(range(200))-{x * 11 for x in range(10)}-set(range(111, 200, 11))
        
        # Add "all-different" constraints
        problem.constraints.extend(
            [BinaryConstraint((var1, var2), lambda a, b: a != b) for var1, var2 in combinations(problem.variables, 2)]
        )
    
        # Assign domains to variables            
        for variable in problem.variables:
            # If the variable is the first letter of a word, it can't be 0
            if variable in (LHS0[-1], LHS1[-1], RHS[-1]):
                problem.domains[variable] = non_zero_digit_set
            else:
                problem.domains[variable] = digit_set

        
        max_len = max(len(LHS0), len(LHS1))
        min_len = min(len(LHS0), len(LHS1))
        max_lhs = LHS1 if len(LHS1) > len(LHS0) else LHS0

        # Add variables and domains for carry 
        problem.variables.extend([f"C{i}" for i in range(max_len)])
        problem.domains.update({f"C{i}": carry_set for i in range(max_len)})


        # Add variables and domains for sum(RHS[i] + carry[i])
        problem.variables.extend([f"{RHS[i]}C{i}" for i in range(max_len)])
        problem.domains.update({f"{RHS[i]}C{i}": small_sum_set for i in range(max_len)})
        

        # Add variables and domains for sum(LHS1[0] + LHS0[0])
        problem.variables.extend([f"{LHS1[0]}{LHS0[0]}"])
        problem.domains.update({f"{LHS1[0]}{LHS0[0]}": medium_set if LHS0[0] != LHS1[0] else {x * 11 for x in range(10)} })
        # Add variables and domains for sum(LHS1[i] + LHS0[i] + carry[i])
        problem.variables.extend([f"{LHS1[i+1]}{LHS0[i+1]}C{i}" for i in range(min_len-1)])
        problem.domains.update({f"{LHS1[i+1]}{LHS0[i+1]}C{i}": large_sum_set  if LHS0[i + 1] != LHS1[i + 1]   else {x * 11 for x in range(10)} | set(range(111, 200, 11))  for i in range(min_len-1)})
        # Add variables and domains for sum(max_lhs[i] + carry[i])  
        #where max_lhs is the longer of the two LHS strings(if they are of different lengths)
        problem.variables.extend([ f"{max_lhs[i+1]}C{i}" for i in range(min_len-1,len(max_lhs) - 1) ])
        problem.domains.update({f"{max_lhs[i+1]}C{i}": small_sum_set for i in range(min_len-1,len(max_lhs) - 1)})
        #add constraints for the first digit of the sum of the two LHS strings
        problem.constraints.extend([
        BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", LHS1[0]), lambda a, b: a // 10 == b),
        BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", LHS0[0]), lambda a, b: a % 10 == b)])                    
        #add constraints for the first digit of the sum of the two LHS strings and the RHS
        problem.constraints.append(BinaryConstraint((f"{LHS1[0]}{LHS0[0]}", f"{RHS[0]}C{0}"), lambda a, b: (a % 10 + a // 10) == b % 10 + 10 * (b // 10)  ))
      
        for i in range(max_len):
           
            carry_var = f"C{i}"
            sum_var = f"{RHS[i]}C{i}"
          #add constraints for the RHS and the carry with the sum of the strings
            problem.constraints.extend([
              BinaryConstraint((sum_var, carry_var), lambda a, b: a // 10 == b),
              BinaryConstraint((sum_var, RHS[i]), lambda a, b: a % 10 == b)])
            #when the strings both havn't ended
            if i < min_len - 1:
                combined_var = f"{LHS1[i+1]}{LHS0[i+1]}C{i}"

                problem.constraints.extend([
                    BinaryConstraint((combined_var, carry_var), lambda a, b: a // 100 == b),  #constraint for carry with combined variable
                    BinaryConstraint((combined_var, f"{RHS[i+1]}C{i+1}"), lambda a, b: (
                        a // 100 + (a % 100) // 10 + (a % 100) % 10 == b % 10 + 10 * (b // 10)
                    )),  #constraint for RHS with combined variable (to make sure the sum is correct)
               BinaryConstraint((combined_var, f"{LHS1[i+1]}"), lambda a, b: (a % 100)%10 ==b), #constraint for LHS1 with combined variable
               BinaryConstraint((combined_var, f"{LHS0[i+1]}"), lambda a, b: (a % 100)//10 ==b) #constraint for LHS0 with combined variable
                ])
            #when a string has ended but the longer string hasn't
            elif i < len(max_lhs) - 1:
                combined_var = f"{max_lhs[i+1]}C{i}"
                
                problem.constraints.extend([
             BinaryConstraint((combined_var, max_lhs[i+1]), lambda a, b: a % 10 == b), #constraint for the longer string with the combined variable
              BinaryConstraint((combined_var, carry_var), lambda a, b: a // 10 == b),  #constraint for carry with combined variable
              BinaryConstraint((combined_var, f"{RHS[i+1]}C{i+1}"), lambda a, b: (
                    a // 10 + a % 10 == b % 10 + 10 * (b // 10)  )) #constraint for RHS with combined variable (to make sure the sum is correct)
                    ])

        if len(RHS) > max_len :
            #update the domain for the last carry if the RHS is longer than the sum of the two LHS strings
            #because last digit can only be 1 and last carry=last digit
            problem.domains[RHS[-1]] = set([1])
            problem.domains[f"C{max_len-1}"] = set([1])
        else:
            #update the domain for the last carry if the RHS is not longer than the sum of the two LHS strings
            #last carry must be 0
            problem.domains[f"C{max_len-1}"] = set([0])
        return problem


    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
        


