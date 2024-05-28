	#production rules
    # 1. AssignmentStmt → Identifier = Expression;
	# 2. Identifier → Letter (Letter | Digit|_)*
	# 3. Expression → Factor (Operator Factor)*
	# 4. Factor → Identifier | Number | ( Expression )
	# 5. Operator → + | - | * | /
	# 6. Letter → a | b | ... | z | A | B | ... | Z
	# 7. Digit → 0 | 1 | ... | 9
    # 8. Number → Digit Digit*
    # 9. If_statement -> if(Expression) {Statement*}
    #10. While_statement -> while(Expression) {Statement*}
    #12. Statement -> AssignmentStmt | If_statement | while_statement
import re

class RecursiveDescentParser:
    def __init__(self, input_string):
        input_string = re.sub(r'\s+', '', input_string)
        self.input_string = input_string  # The string to be parsed.
        self.index = 0                   # The current position in the input string.
        self.length = len(input_string)  # The total length of the input string for bounds checking.


     
        
        # # Remove all whitespace from the input string.
        # re.sub(r'\s+', '', self.input_string)
        
      

    #helper functions for digit, alphabet, operator, underscore,equal sign, semicolon
    def  match_digit(self):
        # checks for digit
        if self.index < self.length and self.input_string[self.index].isdigit():
            return True
        else:
            return False
        
    def match_alphabet(self):
        #checks for alphabet        
        if self.index < self.length and self.input_string[self.index].isalpha():
            return True           
        else:           
            return False
        
    def match_operator(self):
        #note -- final self.index already consumes the operator        
        #checks for each operator
        operators = {'+', '-', '*', '/'}
        logical_operators = {'and','AND','OR','or'}
    
        
        if self.index < self.length:
            if self.input_string[self.index] in operators:
                self.index +=1
                # self.index = self.index + len (operator)
                return True
            for op in logical_operators:
                op_length = len (op)
                if self.index + op_length <= self.length and self.input_string[self.index:self.index + op_length] == op:
                    self.index += op_length  
                    return True
        return False  
        
    def match_underscore(self):     
        if self.index < self.length and self.input_string[self.index] == "_":
            return True
        else:
            return False
        
    def match_equal_sign(self):
        #checks for equal sign 
        if self.index < self.length and self.input_string[self.index]== "=":
            return True
        else:
            return False 
            
    def match_semicolon(self):
        #checks fo rsemi colon
        if self.index < self.length and self.input_string[self.index] == ";":
            return True
        else:
            return False 

    def match_conditional(self):
        #note -- final self.index already consumes the conditional
        
        conditional= {'if','while'}
        if self.index < self.length:
            for condition in conditional:
                condition_length = len(condition)
                if self.index + condition_length <= self.length and self.input_string[self.index:self.index + condition_length] == condition:
                    # print (condition)
                    self.index += condition_length 
                    # if self.index:self.index + condition_length == 'if':
                    #     specific_condition = 'if'

                    return True,condition
        return False
         
    def parse_number(self):
        if not self.match_digit():
            return False
        while self.index < self.length -1  and (self.input_string[self.index+1].isdigit()):
            self.index += 1
        return True
        # print (self.index)
        # if self.index +1 == self.length:
        #     return True
        # else:
        #     return False 
        
    def parse_identifier(self):
        # Identifier → Letter (Letter | Digit|_)*
        # identifier_start_index = self.index
        if not self.match_alphabet():
            # print ("Syntax Error: Identifier must always start with a letter")
            return False
        else: 
            previous = self.index
            self.index +=1 
        
            while self.index<self.length and (self.match_alphabet () or self.match_digit () or self.match_underscore()):
                self.index +=1
                previous +=1
            if not (self.match_alphabet () or self.match_digit () or self.match_underscore()):
                self.index = previous

            return True
    
    def parse_factor(self):
        # print ("index before factor = ",self.index)
        identifier_bool = self.parse_identifier()
        number_bool = self.parse_number()
        # expression_bool,expression_end= self.parse_expression()
        if identifier_bool:
            # print ("identifier not number")
            return True
        elif number_bool:
            # print ("number not identifier")
            return number_bool
        # elif expression_bool:
        #     print ("expression, neither  number nor identifier")
        #     return expression_bool,self.index
        else:
            return False
        
    def parse_expression(self):
        #Expression → Factor (Operator Factor)*
        factor_bool = self.parse_factor()
        if not factor_bool:
            return False      
        # print ("starting index befor checking for operator", self.index)
        # print ("length of string", self.length)
        while self.index < self.length: 
            self.index +=1            
            if self.match_operator():
                # self.index+=1
                factor_bool= self.parse_factor()
                if factor_bool and self.index == self.length-1:                    
                    return True
                if factor_bool and self.index < self.length:
                    continue 
                else:
                    self.index-=1
                    # print ("Syntax error: the expression is not finished (hanging operator) ",self.index)
                    return False
            if not (self.match_operator()):
                self.index -=1
                # print ("expression ends at index",self.index)
                return  True
            
    def parse_AssignmentStmt(self):
        # 1. AssignmentStmt → Identifier = Expression;
        identifier_bool = self.parse_identifier()
        if not identifier_bool:
            print ("Syntax Error: Assignmet statement does not start with an identifier ",self.index)
            return False
        if identifier_bool:
            self.index +=1
            if self.match_equal_sign():
                self.index+=1
                expression_bool = self.parse_expression()
                if expression_bool:
                    self.index+=1
                    if self.match_semicolon():

                        # print ("Assignment statement has syntax")
                        # print(self.index)
                        return True
                    else:
                        print("Semicolon expected at the end of line but found something else")
                        return False

                else:
                    print("Syntax Error: Not appropriate expression after = at index",self.index)
                    return False
            else:
                print ("Syntax error: Assignemt statement missing '=' at index ", self.index)
                return False


    def parse_variableDeclaration (self):
        is_assignment = False 
        is_identifier = False 
       
        if self.parse_identifier:      
            initial_index = self.index             
            self.parse_identifier()
            check_asg_index = self.index 
            self.index += 1
            # print (self.index)
            if self.match_equal_sign(): 
                # print ('if statement with equal sign')
                self.index = initial_index
                if self.parse_AssignmentStmt:
                    self.parse_AssignmentStmt()
                    is_assignment = True                    
            else:
                self.index = check_asg_index 
                is_identifier  = True 
                
        if is_assignment or is_identifier: 
            return True
        else:
            return False  
        
    def parse_nonArithmetic_expression (self):
        is_expression = self.parse_expression()
        is_number = self.parse_number()
        is_identifier = self.parse_identifier()
        if is_expression or is_identifier or is_number:
            return True 
        else: 
            return False
        
    def parse_returnStmt (self):
        if "return" not in self.input_string:
            return False
        else: 
            self.index+=6
            
            is_nonArthimetic_expression = self.parse_nonArithmetic_expression()

            if not is_nonArthimetic_expression:
                return False
            elif is_nonArthimetic_expression:
                self.index +=1
                if  self.match_semicolon ():
                    # self.index+=1
                    return True
                else:
                    self.index-=1
                    return False

        
    def parse_condtion_loop(self):        
        if not self.match_conditional():
            return False
        else:
            # print ("at first",self.index)
            if (self.input_string[self.index]=="("):
                self.index+=1                
                is_expression,_ =  self.parse_expression()
                if is_expression:
                    # print ("there is a conditional here")
                    # print(self.index)
                    self.index+=1
                    if (self.input_string[self.index]==")"):
                        # print ("has untill )")
                        print ("closing ",self.index)

                        self.index+=1
                        if (self.input_string[self.index]=="{"):
                            self.index+=1
                            x = 0
                            while self.input_string[self.index]!='}' and self.index < self.length:
                                # x += 1
                                # print("while loop for conditions",x)

                                # isassignment,_ = 
                                if self.parse_condtion_loop() or self.parse_AssignmentStmt() == True:
                                    self.index+=1
                                    continue
                            # print(self.index)
                            if self.input_string[self.index]=='}':

                                # print(self.index)
                                print ("Successful loop")
                                return True                            
                            # print(self.index)
                            # print ("has until opening {")
                        else: #put condtion if it is not {
                            return False
                    else: #put condtion if it is not a closing bracket
                        return False
                else: # put condtion if it is not an expression
                    return False

            else: # put condtion if it is not open bracket 
                return False
            

    def parse_for_loop (self):
        if "for" not in self.input_string: 
            return False
        else:
            self.index +=3
            if self.input_string[self.index] == "(":
                 self.index +=1
                 is_variable = self.parse_variableDeclaration()
                 if is_variable:
                     self.index +=1
                     if self.input_string[self.index] == ";" :
                         self.index +=1                         
                         is_expression = self.parse_nonArithmetic_expression()
                         if is_expression: 
                             self.index +=1
                             if self.input_string[self.index] == ";" :
                                 self.index+=1
                                 is_arithmeticexp = self.parse_expression()
                                 if is_arithmeticexp:
                                     self.index +=1
                                     if  self.input_string[self.index] == ")":
                                        self.index+=1
                                        if self.input_string[self.index] == "{":
                                            self.index+= 1

                                            if self.input_string[self.index] == "}":
                                                print ("For Loop: nothing in the for loop statement")
                                                return True
                                            
                                            else:                                                
                                                while self.input_string[self.index] != "}" and self.index < self.length:
                                                    begining_while_index = self.index                                                     
                                                    is_assignment = False
                                                    is_condition_loop = False 

                                                    if self.parse_AssignmentStmt():                                             
                                                        self.index +=1
                                                        # print ("in if assignment in while loop" , self.index)
                                                        is_assignment = True
                                                        continue
                                                    else:
                                                        self.index = begining_while_index
                                                        if self.parse_condtion_loop():
                                                            self.index+=1
                                                            # print ("in if condition loop in while loop ",self.index)
                                                            is_condition_loop = True 
                                                            continue                                                     
                                                    break
                                                if is_assignment or is_condition_loop:
                                                    return True
                                                elif not is_assignment:
                                                    return False                                             
                                   
                                        else: # if there is no "{"  after  closing bracket ) 
                                            print ("For Loop: there is no   { after  closing bracket )")
                                            return False
                                     else: # if there is no ")", at the end to the for loop declaration
                                        print ("For Loop: there is no ), at the end to the for loop declaration ")
                                        return False
                                 else: # if there is not  arithmetic exp after ";"
                                     print ("For Loop: there is not  arithmetic exp after ;")
                                     return False
                             else: #if there is not semicolon after  the expression
                                 print ("For Loop: there is no semicolon after  the expression ")
                                 return False
                         else: # if there is no expression after  semicolon
                             print ("For Loop: there is no expression after  semicolon ")
                             return False
                         
                     else: # if there is no ";" between variable declaration and expression
                        print("For Loop: there is no ; between variable declaration and expression")
                        return False
                     
                       
                 else: # if is_variable is false (there is no variable after the for loop)
                    print ("For Loop: is_variable is false (there is no variable after the for loop)")
                    return False

            else: # if there is no opening bracked "(" after the for string
                print ("For Loop: there is no opening bracke ( after the for string")
                return False    

    
    
    def parse_function_definition(self):
        # print (self.input_string)
        if "function" not in self.input_string:
            return False
        else:
            self.index+=8
            try: 
                while self.index < self.length:
                    if self.parse_identifier():
                        self.index+=1
                        print (self.index)
                        if self.input_string[self.index] == '(':
                            self.index +=1
                            if self.parse_variableDeclaration():
                                self.index +=1
                                if self.input_string[self.index] == ",":
                                    self.index+=1
                                    if self.parse_variableDeclaration():
                                        self.index+=1
                                        if self.input_string[self.index] == ")":
                                            self.index+=1
                                            if self.input_string[self.index] == "{":
                                                self.index+=1
                                                is_assignment = True
                                                is_condition_loop = True                                         
                                                while  self.input_string[self.index]!= "r" and  self.index < self.length:
                                                            begining_while_index = self.index                                                     
                                                            is_assignment = self.parse_AssignmentStmt()
                                                            is_condition_loop = self.parse_condtion_loop() 

                                                            if is_assignment:
                                                                # self.parse_AssignmentStmt() 
                                                                                                        
                                                                self.index +=1
                                                                # print ("in if assignment in while loop" , self.index)
                                                                is_assignment = True
                                                                continue
                                                            else:
                                                                self.index = begining_while_index
                                                                if is_condition_loop:
                                                                    # self.parse_condtion_loop()
                                                                    self.index+=1
                                                                    # print ("in if condition loop in while loop ",self.index)
                                                                    is_condition_loop = True 
                                                                    continue                                                     
                                                            break
                                                if is_assignment or is_condition_loop:
                                                    # print ("before return statement",self.index)
                                                    # self.index +=1
                                                    if self.parse_returnStmt():
                                                        self.index+=1
                                                        # print ("after return statement ",self.index)
                                                        if self.input_string[self.index] == "}":
                                                            return True                                                   
                                                        else: # no closing } after the return statement
                                                            print("Function definition: no closing } after the return statement")
                                                            return False
                                                    else: # no return statement 
                                                        print("Function definition: no return statement in function")
                                                        return False  
                                            else: # not an opening { after closing )
                                                print("Function definition: not an opening { after closing )")
                                                return False
                                        else: # not a closing ) after the second variable declaration
                                            print ("Function definition: not a closing ) after the second variable declaration")
                                            return False
                                    else: # not a second variable declaration after ,
                                        print("Function definition: not a valid second variable declaration after ,")
                                        return False
                                else: #not a , after variable declaration
                                    print("Function definition: not a , after variable declaration")
                                    return False
                            else: # not a variable declaratioin  after (
                                print("Function definition: not a variable declaratioin  after (")
                                return False                    
                        else: # not an ( after an identifier 
                            print("not an ( after an identifier")
                            return False
                    else: # not an identifier after the function statement
                        print("Function definition: not an identifier after the function statement", self.index) 
                        return False  
            except IndexError:
                print ("Expecting a finished code") #change the print statement
                print (self.index)

    def parse(self):

        while self.index < self.length -1:
            if self.parse_function_definition() or self.parse_AssignmentStmt() or self.parse_condtion_loop() or self.parse_for_loop():
                return "Syntax is correct"
                
                # if self.index >= self.length: 
                    
                # else:
                #     continue
            else: 
                return "Code has syntax errors check the statements above"

                
            # if self.index == self.length -1:
                
            # else:
            #     return "Code has syntax errors check the statements above" 


               
        
    def is_balanced(expression):
        balance = 0  # Initialize a counter to zero

        # Iterate through each character in the expression
        for char in expression:
            if char == '(':
                balance += 1  # Increment the counter for an opening parenthesis
            elif char == ')':
                balance -= 1  # Decrement the counter for a closing parenthesis
            
            # If balance goes negative, we have a closing parenthesis without an opening match
            if balance < 0:
                return False

        # If balance is zero, all parentheses are balanced
        return balance == 0
 

string = r'if(x+y){asg = 1+2;}'
string2 = "num=identiy_1+2;"
string3 = "x=2;"
function = """x = 2;
function (x , y)
{
sum = x + 3;
return sum;a

"""
function_string = r'functionvariable_1(num1,num2){x=1+2;y=3+4;returnnum1;}'
string_for_loop = r"for(x;num;x+1){num=identiy_1+2;num=identiy_1+2;while(num1){x=9;}not}"
parser = RecursiveDescentParser (string_for_loop)
print (parser.parse())
