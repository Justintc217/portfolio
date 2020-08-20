types = ["int", "char", "boolean"]
operators = list("+-*/&|<>=")
unary_ops = list("~-")
class_names = list()
subroutine_names = list()


def compile_to_xml(given_token_list, given_filename):
    global filename
    filename = given_filename
    global token_list
    token_list = given_token_list
    token_index = 0
    indentation_count = 0
    while token_index < len(token_list):
        token_index = compileClass(indentation_count, token_index)


def wrap_with_tags(func):
    def inner(indentation_count, token_index):
        writeXML_tag(indentation_count, getRoutineName(func), start=True)
        to_return = func(indentation_count + 1, token_index)
        writeXML_tag(indentation_count, getRoutineName(func), start=False)
        return to_return
    return inner


@wrap_with_tags
def compileClass(indentation_count, token_index):
    # class className { classVarDec* subRoutineDec* }
    class_names.append(token_list[token_index + 1][0])  # append className
    n1 = 3
    write_n_xml_elements(n1, indentation_count, token_index)
    token_index = token_index+n1
    next_token, next_identity = token_list[token_index]
    while next_token in ["field", "static"]:
        token_index = compileClassVarDec(indentation_count, token_index)
        next_token, next_identity = token_list[token_index]
    while next_token in ["constructor", "function", "method"]:
        token_index = compileSubroutineDec(indentation_count, token_index)
        next_token, next_identity = token_list[token_index]

    # end section
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileClassVarDec(indentation_count, token_index):
    # (static | field) type varName (, varName)* ;
    n1 = 3
    write_n_xml_elements(n1, indentation_count, token_index)
    token_index += n1
    next_token, next_identity = token_list[token_index]
    while next_token != ";":
        n2 = 2
        write_n_xml_elements(n2, indentation_count, token_index)
        token_index += n2
        next_token, next_identity = token_list[token_index]
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileSubroutineDec(indentation_count, token_index):
    # (constructor | function | method) (void | type) subroutineName '(' parameterList ')' subroutineBody
    subroutine_names.append(token_index + 2)
    n1 = 4
    write_n_xml_elements(n1, indentation_count, token_index)
    token_index += n1
    token_index = compileParameterList(indentation_count, token_index)
    writeXML_elements(indentation_count, token_index)  # )
    token_index = compileSubroutineBody(indentation_count, token_index+1)
    return token_index


@wrap_with_tags
def compileSubroutineBody(indentation_count, token_index):
    # subroutineBody: { varDec* statements }
    writeXML_elements(indentation_count, token_index)

    token_index += 1
    next_token, next_identity = token_list[token_index]
    while next_token == "var":
        token_index = compileVarDec(indentation_count, token_index)
        next_token, next_identity = token_list[token_index]
    token_index = compileStatements(indentation_count, token_index)

    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileVarDec(indentation_count, token_index):
    # varDec: var type varName (, varName)* ;
    n1 = 3
    write_n_xml_elements(n1, indentation_count, token_index)
    token_index += n1
    next_token, next_identity = token_list[token_index]
    while next_token != ";":
        n2 = 2
        write_n_xml_elements(n2, indentation_count, token_index)
        token_index += n2
        next_token, next_identity = token_list[token_index]
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileParameterList(indentation_count, token_index):
    # parameterList: (type varName (, type varName)*)?
    this_token, _ = token_list[token_index]
    if this_token in types + class_names:
        n1 = 2
        write_n_xml_elements(n1, indentation_count, token_index)
        token_index += n1
        next_token, next_identity = token_list[token_index]
        while next_token == ",":
            n2 = 3
            write_n_xml_elements(n2, indentation_count, token_index)
            token_index += n2
            next_token, next_identity = token_list[token_index]
    return token_index  # no +1 because doesn't end with additonal element


@wrap_with_tags
def compileStatements(indentation_count, token_index):
    # statements: statement*
    statement_token, _ = token_list[token_index]
    while statement_token in ["let", "do", "if", "while", "return"]:
        token_index = execute_compile_statement_x(
            statement_token, indentation_count, token_index)
        statement_token, _ = token_list[token_index]
    return token_index


@wrap_with_tags
def compileLetStatement(indentation_count, token_index):
    # letStatement: let varName ('[' expression ']')? = expression ;
    n1 = 2
    write_n_xml_elements(n1, indentation_count, token_index)
    token_index += n1
    next_token, _ = token_list[token_index]
    if next_token == "[":
        writeXML_elements(indentation_count, token_index)
        token_index = compileExpression(indentation_count, token_index + 1)
        writeXML_elements(indentation_count, token_index)
        token_index += 1
    writeXML_elements(indentation_count, token_index)
    token_index = compileExpression(indentation_count, token_index + 1)
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileIfStatement(indentation_count, token_index):
    # ifStatement: if '(' expression ')' '{' statements '}' (else '{' statements '}')?
    write_n_xml_elements(2, indentation_count, token_index)
    token_index = compileExpression(indentation_count, token_index + 2)
    write_n_xml_elements(2, indentation_count, token_index)
    token_index = compileStatements(indentation_count, token_index + 2)
    writeXML_elements(indentation_count, token_index)  # }
    next_token, next_identity = token_list[token_index + 1]
    if next_token == "else":
        write_n_xml_elements(2, indentation_count, token_index + 1)
        token_index = compileStatements(indentation_count, token_index + 3)
        writeXML_elements(indentation_count, token_index)  # }
    return token_index + 1


@wrap_with_tags
def compileWhileStatement(indentation_count, token_index):
    # whileStatement: while '{' expression '}' '{' statements '}'
    write_n_xml_elements(2, indentation_count, token_index)
    token_index = compileExpression(indentation_count, token_index + 2)
    write_n_xml_elements(2, indentation_count, token_index)
    token_index = compileStatements(indentation_count, token_index + 2)
    writeXML_elements(indentation_count, token_index)  # }
    return token_index + 1


@wrap_with_tags
def compileDoStatement(indentation_count, token_index):
    # doStatement: do subRoutineCall ;
    writeXML_elements(indentation_count, token_index)
    token_index = compileSubroutineCall(indentation_count, token_index + 1)
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileReturnStatement(indentation_count, token_index):
    # returnStatement: return expression? ;
    writeXML_elements(indentation_count, token_index)
    token_index += 1
    next_token, next_identity = token_list[token_index]
    if next_token != ";":
        token_index = compileExpression(indentation_count, token_index)
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileExpression(indentation_count, token_index):
    # expression: term (op term)*
    token_index = compileTerm(indentation_count, token_index)
    next_token, next_identity = token_list[token_index]
    while next_token in operators:
        writeXML_elements(indentation_count, token_index)
        token_index = compileTerm(indentation_count, token_index + 1)
        next_token, _ = token_list[token_index]
    return token_index  # no +1 since no end element


@wrap_with_tags
def compileTerm(indentation_count, token_index):
    look_ahead_token, _ = token_list[token_index + 1]
    this_token, _ = token_list[token_index]
    if look_ahead_token == "." or this_token in subroutine_names:
        # WARNING: subroutine_names may have the same name under different classes
        token_index = compileSubroutineCall(indentation_count, token_index)
        return token_index  # already did the +1 in subroutine
    elif look_ahead_token == "[":  # varName '[' expression ']'
        write_n_xml_elements(2, indentation_count, token_index)
        token_index = compileExpression(indentation_count, token_index + 2)
        writeXML_elements(indentation_count, token_index)
        return token_index + 1
    elif this_token == "(":  # '(' expression ')'
        writeXML_elements(indentation_count, token_index)
        token_index = compileExpression(indentation_count, token_index + 1)
        writeXML_elements(indentation_count, token_index)
        return token_index + 1
    elif this_token in unary_ops:  # unaryOp term
        writeXML_elements(indentation_count, token_index)
        token_index = compileTerm(indentation_count, token_index + 1)
        return token_index
    else:
        writeXML_elements(indentation_count, token_index)
        return token_index + 1


def compileSubroutineCall(indentation_count, token_index):
    # subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' same as first option
    next_token, _ = token_list[token_index + 1]
    if next_token == ".":
        write_n_xml_elements(2, indentation_count, token_index)
        token_index += 2
    write_n_xml_elements(2, indentation_count, token_index)
    token_index = compileExpressionList(indentation_count, token_index + 2)
    writeXML_elements(indentation_count, token_index)
    return token_index + 1


@wrap_with_tags
def compileExpressionList(indentation_count, token_index):
    # (expression (, expression)*)?
    if token_list[token_index][0] == ")":
        return token_index  # no +1 since doesn't end with an element
    token_index = compileExpression(indentation_count, token_index)
    while token_list[token_index][0] == ",":
        writeXML_elements(indentation_count, token_index)
        token_index = compileExpression(indentation_count, token_index + 1)
    return token_index  # no +1 since doesn't end with an element


def getRoutineName(func):
    fullname = func.__name__
    routineName = fullname[7].lower() + fullname[8:]
    return routineName


def indenter(indentation_count):
    return " " * indentation_count * 4


def writeXML(phrase):
    # global filename
    with open(filename, "a") as outfile:
        outfile.write(phrase + "\n")


def writeXML_elements(indentation_count, token_index):
    indentation = indenter(indentation_count)
    token, identity = token_list[token_index]
    if identity == "stringConstant":
        token = token.replace("\"", "")
    out = "{indentation}<{identity}> {token} </{identity}>".format(
        indentation=indentation,
        identity=identity,
        token=token
    )
    writeXML(out)


def writeXML_tag(indentation_count, identity, start):
    if start:
        slash = ""
    else:
        slash = "/"
    indentation = indenter(indentation_count)
    out = "{indentation}<{slash}{identity}>".format(
        indentation=indentation,
        identity=identity,
        slash=slash
    )
    writeXML(out)


def write_n_xml_elements(write_n, indentation_count, token_index):
    for n in range(write_n):
        writeXML_elements(indentation_count, token_index + n)


def execute_compile_statement_x(*args):
    statement_type = args[0][0].upper() + args[0][1:]
    compileXStatement = "compile{0}Statement({1}, {2})".format(
        statement_type, args[1], args[2])
    return eval(compileXStatement)
