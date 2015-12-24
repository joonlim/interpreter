# Joon Lim 109558002
# HW 6
# main.py
# StonyBrookPython

import sys
import tpg
import copy


# This stack of tables will store all variables and their bindings.
# Each entry on the stack represents a layer of scope.
# At the start, the program is in the main scope and starts with
# a stack of one empty table.

scope = []
scope.append(dict())

# stack functions
# scope[-1]                         peek()
# scope.pop()                       pop()

# To add a new scope:
# layer = scope[-1]
# scope.append(copy.deepcopy(layer))

# This table will store all functions and their definitions ()
# name -> (list_of_args, definition)

functionsTable = {}


class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """


# These are the nodes of our abstract syntax tree.
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """

    def execute(self):
        """
        Executes this node.
        """
        raise SemanticError()

    def evaluate(self):
        """
        Evaluates this node for an r-value. R-value
        """
        raise SemanticError()

    def location(self):
        """
        Evaluates this node for a location. L-value
        """
        raise SemanticError()


class Variable(Node):
    """
    A node representing access to a variable.
    """

    def __init__(self, name):
        self.name = str(name)
        table = scope[-1]
        table[self.name] = None

    def evaluate(self):
        # print(scope)
        table = scope[-1]
        if self.name in table:
            return table[self.name]

        raise SemanticError()

    def location(self):
        return self.name


class FunctionCall(Node):
    """
    A node representing a call to a funtion.
    """
    def __init__(self, name, args):
        self.name = name
        try:
            l = list(args)
        except TypeError:
            l = list((args,))

        self.args = []
        for v in l:
            self.args.append(v)

    def evaluate(self):

        name = self.name.location()
        if self.name.location() in functionsTable:

            function = functionsTable[name]   # tuple
            args = function[0]
            definition = function[1]

            # if the number of arguments does not match, throw error.
            if len(args) != len(self.args):
                raise SemanticError()

            # hard copy dict onto stack
            scope.append(copy.deepcopy(scope[-1]))
            table = scope[-1]

            # set arguments in dict
            for i in range(0, len(args)):
                table[args[i]] = self.args[i].evaluate()

            return definition.execute()

        # if name is not in table, error
        raise SemanticError()


class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value


class StringLiteral(Node):
    """
    A node representing string literals.
    """

    def __init__(self, value):
        self.value = str(value).strip('\"')

    def evaluate(self):
        return self.value


class ListLiteral(Node):
    """
    A node representing list literals.
    """

    def __init__(self, value):
        l = []
        try:
            l = list(value)
        except TypeError:
            l = list((value,))

        self.value = []
        for v in l:
            self.value.append(v.evaluate())

    def evaluate(self):
        return self.value


# Expressions


class Index(Node):
    """
    A node representing indexing.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, str) and not isinstance(left, list):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if len(left) <= right:
            raise SemanticError()
        return left[right]

    def location(self):
        # return a tuple with name and index
        return (self.left.name, self.right.evaluate())


class Add(Node):
    """
    A node representing addition and string concatentation.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if isinstance(left, int) and not isinstance(right, int):
            raise SemanticError()
        if isinstance(right, int) and not isinstance(left, int):
            raise SemanticError()
        if isinstance(left, str) and not isinstance(right, str):
            raise SemanticError()
        if isinstance(right, str) and not isinstance(left, str):
            raise SemanticError()
        return left + right


class Subtract(Node):
    """
    A node representing subtraction.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left - right


class Multiply(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left * right


class Divide(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if right == 0:
            raise SemanticError()
        return (int)(left / right)


class Modulo(Node):
    """
    A node representing modulo.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if right == 0:
            raise SemanticError()
        return (int)(left % right)


class Xor(Node):
    """
    A node representing bitwise XOR.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left ^ right


class LessThan(Node):
    """
    A node representing <.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if left < right:
            return 1
        else:
            return 0


class GreaterThan(Node):
    """
    A node representing >.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if left > right:
            return 1
        else:
            return 0


class Equals(Node):
    """
    A node representing ==.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if left == right:
            return 1
        else:
            return 0


class Not(Node):
    """
    A node representing NOT.
    """

    def __init__(self, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.right = right

    def evaluate(self):
        right = self.right.evaluate()
        if not isinstance(right, int):
            raise SemanticError()
        if right == 0:
            return 1
        else:
            return 0


class Or(Node):
    """
    A node representing OR.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if left == 0 and right == 0:
            return 0
        else:
            return 1


class And(Node):
    """
    A node representing AND.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if left != 0 and right != 0:
            return 1
        else:
            return 0


# Statements


class Execute(Node):
    def __init__(self, value):
        l = []
        try:
            l = list(value)
        except TypeError:
            l = list((value,))

        self.value = []
        for v in l:
            self.value.append(v)

    def execute(self):
        for s in self.value:
            s.execute()


class Block(Node):
    """
    A node representing the block statement.
    """
    def __init__(self, value):
        try:
            l = list(value)
        except TypeError:
            l = list((value,))

        self.value = []
        for v in l:
            self.value.append(v)

    def execute(self):
        for s in self.value:
            # if this statement is return, return
            retval = s.execute()
            if retval is not None:
                return retval


class Return(Node):
    """
    A node representing returning from a function.
    """
    def __init__(self, value):
        self.value = value

    def execute(self):
        value = self.value.evaluate()

        # pop dict from stack
        scope.pop()

        return value


class If(Node):
    """
    A node representing the if statement.
    """
    def __init__(self, expression, statement):

        self.expression = expression
        self.statement = statement

    def execute(self):

        if self.expression.evaluate() != 0:
            retval = self.statement.execute()
            if retval is not None:
                return retval


class IfElse(Node):
    """
    A node representing the if statement.
    """
    def __init__(self, expression, statement1, statement2):
        self.expression = expression
        self.statement1 = statement1
        self.statement2 = statement2

    def execute(self):
        if self.expression.evaluate() != 0:
            retval = self.statement1.execute()
            if retval is not None:
                return retval
        else:
            retval = self.statement2.execute()
            if retval is not None:
                return retval


class While(Node):
    """
    A node representing the while statement.
    """
    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement

    def execute(self):
        while self.expression.evaluate() != 0:
            retval = self.statement.execute()
            if retval is not None:
                return retval


class Assign(Node):
    """
    A node representing the assignment statement.
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        # left is the location
        # right is the expression

        # var = var
        # var = expression
        # var = index
        # index = var
        # index = expression
        # index = index
        location = self.left.location()
        table = scope[-1]

        if (isinstance(location, tuple)):
            name = location[0]
            index = location[1]
            array = table[name]
            array[index] = self.right.evaluate()
            table[name] = array

        else:
            table[location] = self.right.evaluate()


class FunctionDeclare(Node):
    """
    A node representing a delcaration of a funtion.
    """

    def __init__(self, name, args, definition):
        self.name = name.location()
        try:
            l = list(args)
        except TypeError:
            l = list((args,))

        self.args = []
        for v in l:
            self.args.append(v.location())

        self.definition = definition

    def execute(self):
        # add a new function to the functionsTable dict
        location = self.name
        # map name to a tuple containing a list of args and definition
        functionsTable[location] = (self.args, self.definition)


class Print(Node):
    """
    A node representing the print statement.
    """
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        print (repr(self.expression.evaluate()))


# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    r"""
    token int '\d+' IntLiteral;
    token string '"[^\"]*"' StringLiteral;
    token var '[A-Za-z]\w*' Variable;

    separator space "\s+";

    START/a -> $ a = [] $
    ( CODE/s $ a.append(s) $ )*
    $ a = Execute(a) $
    ;

    CODE/a -> FUNCTIONDECLARE/a | STATEMENT/a
    ;

    STATEMENT/a -> BLOCK/a
    | "if" "\(" VALUE/e "\)" STATEMENT/s
    "else" STATEMENT/t $ a = IfElse(e, s, t) $
    |"if" "\(" VALUE/e "\)" STATEMENT/s $ a = If(e, s) $
    | "while" "\(" VALUE/e "\)" STATEMENT/s $ a = While(e, s) $
    | VALUE/l "=(?!=)" VALUE/r ";" $ a = Assign(l, r) $
    | "print" "\(" VALUE/e "\)" ";" $ a = Print(e) $
    | "return" VALUE/v ";" $ a = Return(v) $
    | "return" ";" $ a = Return(None) $
    ;

    BLOCK/a -> '\{'
    $ a = [] $
    ( STATEMENT/s $ a.append(s) $ )*
    '\}'
    $ a = Block(a) $
    ;

    VALUE/a -> OR/a
    ;

    FUNCTIONCALL/a -> var/a "\(" "\)" $ a = FunctionCall(a, []) $
    | var/a "\("
    $ l = [] $
    ( VALUE/v $ l.append(v) $ )
    ( "," VALUE/v $ l.append(v) $ )*
    "\)"
    $ a = FunctionCall(a, l) $
    ;

    FUNCTIONDECLARE/a -> var/a "\(" "\)" BLOCK/b
    $ a = FunctionDeclare(a, [], b) $
    | var/a "\("
    $ l = [] $
    ( var/v $ l.append(v) $ )
    ( "," var/v $ l.append(v) $ )*
    "\)" BLOCK/b
    $ a = FunctionDeclare(a, l, b) $
    ;

    OR/a -> AND/a
    ( "or" AND/b $ a = Or(a, b) $
    )*
    ;

    AND/a -> NOT/a
    ( "and" NOT/b $ a = And(a,b) $
    )*
    ;

    NOT/a -> COMPARISON/a |
    ( "not" COMPARISON/a $ a = Not(a) $
    )
    | "not" NOT/a $ a = Not(a) $
    ;

    COMPARISON/a -> XOR/a
    ( "[<]" XOR/b $ a = LessThan(a, b) $
    | "[>]" XOR/b $ a = GreaterThan(a, b) $
    | "==" XOR/b $ a = Equals(a, b) $
    )*
    ;

    XOR/a -> EXPRESSION/a
    ( "xor" EXPRESSION/b $ a = Xor(a, b) $
    )*
    ;

    EXPRESSION/a -> TERM/a
    ( "[+]" TERM/b $ a = Add(a, b) $
    | "[-]" TERM/b $ a = Subtract(a, b) $
    )*
    ;

    TERM/a -> FACT/a
    ( "[*]" FACT/b $ a = Multiply(a, b) $
    | "[/]" FACT/b $ a = Divide(a, b) $
    | "[%]" FACT/b $ a = Modulo(a, b) $
    )*
    ;

    FACT/a -> ( LIST/a | PAREN/a )
    ( '\[' VALUE/b '\]' $ a = Index(a, b) $
    )*
    ;

    LIST/a -> '\[' $ a = [] $
    ( VALUE/b $ a.append(b) $ )
    ( "," ( VALUE/c $ a.append(c) $ )
    )*
    '\]' $ a = ListLiteral(a) $
    ;

    PAREN/a -> '\(' VALUE/a '\)' | LITERAL/a
    ;

    LITERAL/a -> FUNCTIONCALL/a | int/a | string/a | var/a
    ;
    """

# Make an instance of the parser. This acts like a function.
parse = Parser()

# This is the driver code, that reads in lines, deals with errors, and
# prints the output if no error occurs.

# Open the file containing the input.
f = open(sys.argv[1], "r")
code = f.read()
f.close()

try:
    # Try to parse the expression.
    node = parse(code)

    # Try to get a result.
    result = node.execute()

    # Print the representation of the result.
    # print(repr(result))

# If an exception is thrown, print the appropriate error.
except tpg.Error:
    print("SYNTAX ERROR")
    # Uncomment the next line to re-raise the syntax error,
    # displaying where it occurs. Comment it for submission.
    # raise

except SemanticError:
    print("SEMANTIC ERROR")
    # Uncomment the next line to re-raise the semantic error,
    # displaying where it occurs. Comment it for submission.
    # raise

f.close()
