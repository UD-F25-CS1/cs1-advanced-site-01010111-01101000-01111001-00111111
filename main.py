from bakery import assert_equal
from drafter import *
from dataclasses import dataclass


set_site_information(
    author = 'rmdang@udel.edu',
    description = 'A simple calculator that replaces Microsoft calculator because it sucks.',
    sources = [''],
    planning = [''],
    links = ['https://github.com/UD-F25-CS1/cs1-website-f25-01010111-01101000-01111001-00111111', '']
)
hide_debug_information()
set_website_title("Minhisoft Calculator")
set_website_framed(False)


@dataclass
class Side:
    pass

@dataclass
class Pemdas(Side):
    operator: str
    left: Side
    right: Side
    
@dataclass
class PemdasNum(Side):
    value: float

@dataclass
class Storage:
    full_equation: str
    operations: list[str]
    steps: list[str]

@dataclass
class State:
    option: str
    last_equation: str
    last_answer: str
    operators: list[str]
    steps: list[str]
    keep_answer: bool
    history: list[Storage]


@route
def index(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page

    This start page allows the user to choose an operation that leads to their respective pages.
    If an answer exists from a previous operation,
        the page will show the last computation and its answer.
    Otherwise it will show either the default starting string or an error string.
    '''
    state.keep_answer = False
    return Page(state, [
        Header('Choose operation mode:', 3),
        'Simple:',
        Row(Button('+', add_page), Button('−', sub_page), Button('×', mul_page), Button('÷', div_page)),
        Row(Button('xª', exp_page), Button('ª√x', roo_page)),
        'Advanced:',
        Button('Write your own!', pemdas_page),
        HorizontalRule(),
        'History:',
        state.history[-1].full_equation,
        Button('History Page', history_page)
        ])

@route
def history_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
        
    Adds all instances of Storage.full_equation other than the initial default,
        into a list that is organized into a numbered list where
        the most recent calculation is first and the rest cascade down.
    If there are no calculations done, then there will be a string saying so.
    '''
    content = [
        Header('History page:', 3),
        HorizontalRule()
    ]
    for history_index in range(len(state.history)-1, 0, -1):
        storage = state.history[history_index]
        content.append(Row(
            storage.full_equation,
            Button('Info', info_page, [('history_index', history_index)]) 
            ))
            
    if len(state.history) <= 1:
         content.append('There\'s nothing here yet, come back once you\'ve done an operation!') 
    
    content.append(HorizontalRule())
    content.append(Button('Back to start', index))
    
    return Page(state, content)

@route
def info_page(state: State, history_index: int)-> Page:
    '''
    Args:
        State, int
    Returns:
        Page
        
    Shows details for a specific calculation.
    '''
    storage = state.history[history_index]
    if storage.operations:
        opps_used = ", ".join(storage.operations)
    else:
        opps_used = "None"

    return Page(state, [
        Header('Calculation Details', 3),
        "Equation:",
        storage.full_equation,
        HorizontalRule(),
        "Operations performed (in order):",
        opps_used,
        "Steps taken:",
        BulletedList(storage.steps),
        HorizontalRule(),
        Button('Back to History', history_page)
    ])

@route
def add_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '+' for combined_calc().
    The left / right textboxes correspond to first_str / second_str used in combined_calc().
    The first textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '+'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Addition:', 4),
        Row(TextBox('first_str', default_value), '+', TextBox('second_str', None)),
        Button('Calculate!', combined_calc)
        ])

@route
def sub_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '−' for combined_calc().
    The left / right textboxes correspond to first_str / second_str used in combined_calc().
    The first textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '−'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Subtraction:', 4),
        Row(TextBox('first_str', default_value), '−', TextBox('second_str', None)),
        Button('Calculate!', combined_calc)
        ])

@route
def mul_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '×' for combined_calc().
    The left / right textboxes correspond to first_str / second_str used in combined_calc().
    The first textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '×'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Multiplication:', 4),
        Row(TextBox('first_str', default_value), '×', TextBox('second_str', None)),
        Button('Calculate!', combined_calc)
        ])

@route
def div_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '÷' for combined_calc().
    The left / right textboxes correspond to first_str / second_str used in combined_calc().
    The first textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '÷'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Division:', 4),
        Row(TextBox('first_str', default_value), '÷', TextBox('second_str', None)),
        Button('Calculate!', combined_calc)
        ])

@route
def exp_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '^' for combined_calc().
    The left / right textboxes correspond to first_str / second_str used in combined_calc().
    The first textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '^'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Exponential:', 4),
        Row(TextBox('first_str', default_value), '^', TextBox('second_str', None)),
        Button('Calculate!', combined_calc)
        ])

@route
def roo_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Sets State.option to '√' for combined_calc().
    The left / right textboxes correspond to second_str / first_str used in combined_calc().
        /\ /\ /\ Note it is reversed from the previous pages /\ /\ /\
    The second textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous calculated answer.
        Otherwise, default_value is set to None.
    '''
    state.option = '√'
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_answer
    else:
        default_value = None
    
    return Page(state, [
        Header('Root:', 4),
        Row(TextBox('second_str', None), '√(', TextBox('first_str', default_value), ')'),
        Button('Calculate!', combined_calc)
        ])

@route
def pemdas_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
        
    Displays a page with an input textbox and text indicating free expressions.
    The textbox has a default_value that may change.
        If State.keep_answer is True, then it will be set False and
        updates default_value to the previous equation used.
        Otherwise, default_value is set to None.
    '''
    if state.keep_answer:
        state.keep_answer = False
        default_value = state.last_equation.replace('−','-').replace('×','*').replace('÷','/')
    else:
        default_value = None
    
    return Page(state, [
        Header('Enter an expression:', 4),
        TextBox('input_str', default_value),
        'Please use these signs for your expression!',
        '+, -, *, /, ^, (, )',
        'Other characters are ignored',
        Button('Calculate!', pemdas_order)
        ])


def comma_format(number: float)-> str:
    '''
    Args:
        float
    Returns:
        string
        
    Separates the incoming float by its decimal and considers the numbers on the left side.
    Commas are added to those numbers for every three integers.
    Then, the string is recombined with the decimal and returned.
    '''
    num_str = str(number)
    number_split = num_str.split('.')
    num_list = []
    format_list = []
    for value in number_split[0]:
        if value != '-':
            num_list.insert(0, value)
    
    for index, value in enumerate(num_list):
        if index % 3 == 0 and index:
            format_list.insert(0, ',')
        format_list.insert(0, value)
    
    if number < 0:
        return '-' + ''.join(format_list) + '.' + number_split[1]
    else:
        return ''.join(format_list) + '.' + number_split[1]


def has_value(input_str: str)-> bool:
    '''
    Args:
        string
    Returns:
        bool
        
    Returns True only if there is a value in the string.
    '''
    for character in input_str:
        if character in ['1','2','3','4','5','6','7','8','9']:
            return True
    return False


def filter_characters(input_str: str)-> str:    
    '''
    Args:
        string
    Returns:
        float
        
    Attempts to turn any string into one that can convert to a float.
    Should the string have:
        any character other than the integers and negative sign,
        or duplicate decimals/division signs,
        these characters will be ignored.
    '''
    decimal_possible = True
    sign_possible = True
    e_possible = True
    num_list = ['0','1','2','3','4','5','6','7','8','9']
    num_str = ''
    if has_value(input_str):
        if input_str[0] == '-':
            sign_possible = False
            num_str += '-'
            
        for character in input_str:
            if character in num_list:
                num_str += character
                
            elif character in ['e','+','-']:
                if character == 'e' and e_possible:
                    e_possible = False
                    sign_possible = True
                    num_str += 'e'
                
                elif sign_possible and num_str[-1] not in num_list:
                    sign_possible = False
                    num_str += character
            
            elif character == '.' and decimal_possible:
                num_str += '.'
                decimal_possible = False
                
            elif character == '/' and '/' not in num_str:
                num_str += '/'
                decimal_possible = True
                
        return num_str
    else:
        return '0.0'
    
    
def eval_float(state: State, num_str: str)-> float:
    '''
    Args:
        State, string
    Returns:
        float
        
    Separates the incoming string by '/' or 'e' and turns each side into floats.
    The divided value is returned unless the denominator is zero.
        In such case an error message is saved and goes to results_page().
    '''
    if '/' in num_str:    
        num_split = num_str.split('/')
        numerator = float(num_split[0])
        denominator = float(num_split[1])
        if denominator:
            return numerator / denominator
        else:
            raise ZeroDivisionError(comma_format(numerator))
    
    elif 'e' in num_str:
        num_split = num_str.split('e')
        base = float(num_split[0])
        exponent = float(num_split[1])
        return base ** exponent
    
    else:
        return float(num_str)

@route
def combined_calc(state: State, first_str: str, second_str: str)-> Page:
    '''
    Args:
        State, string(1), string(2)
    Returns:
        Page
        
    This is the bulk of the calculations.
    Based on State.option, it will calculate the first and second numbers
        after those numbers are filtered for valid characters.
    The calculation used is put into State.last_equation with comma format.
    The result is then formatted with commas, but if it doesn't exist
        it will set State.last_answer to an error message instead of the result.
    The calculation used and the result is saved in Storage, which is inserted
        into State.history as the first item.
    '''
    try:
        first = eval_float(state, filter_characters(first_str))
        second = eval_float(state, filter_characters(second_str))
        first_formatted = comma_format(first)
        second_formatted = comma_format(second)
        result = 'DNE'
        if state.option == '+':
            if second < 0:
                state.last_equation = first_formatted + ' − ' + second_formatted[1:]
            else:
                state.last_equation = first_formatted + ' + ' + second_formatted
            
            result = first + second
            state.operators.append('+')
            state.steps.append(f"{first_formatted} + {second_formatted} = {comma_format(result)}")
        
        elif state.option == '−':
            if second < 0:
                state.last_equation = first_formatted + ' + ' + second_formatted[1:]
            else:
                state.last_equation = first_formatted + ' − ' + second_formatted
            
            result = first - second
            state.operators.append('−')
            state.steps.append(f"{first_formatted} − {second_formatted} = {comma_format(result)}")
        
        elif state.option == '×':
            state.last_equation = first_formatted + ' × ' + second_formatted
            result = first * second
            state.operators.append('×')
            state.steps.append(f"{first_formatted} × {second_formatted} = {comma_format(result)}")
        
        elif state.option == '÷':
            state.last_equation = first_formatted + ' ÷ ' + second_formatted
            state.operators.append('÷')
            if second:
                result = first / second
                state.steps.append(f"{first_formatted} ÷ {second_formatted} = {comma_format(result)}")
            else:
                state.steps.append(f"{first_formatted} ÷ {second_formatted} = DNE")
        
        elif state.option == '^':
            state.last_equation = '(' + first_formatted + ') ^ ' + second_formatted
            result = first ** second
            state.operators.append('^')
            state.steps.append(f"{first_formatted} ^ {second_formatted} = {comma_format(result)}")
            
        elif state.option == '√':
            state.last_equation = '(' + first_formatted + ') ^ (1/' + second_formatted + ')'
            state.operators.append('√')
            if first >= 0 and second:
                result = first ** (1 / second)
                state.steps.append(f"{first_formatted} ^ (1/{second_formatted}) = {comma_format(result)}")
            else:
                state.steps.append(f"{first_formatted} ^ (1/{second_formatted}) = DNE")
        
        if result == 'DNE':
            state.last_answer = 'DNE'
        else:
            state.last_answer = comma_format(result)
            
    except ZeroDivisionError as error:
        state.last_equation = error.args[0] + ' ÷ 0.0'
        state.last_answer = 'DNE'
    except Exception:
        state.last_answer = 'Error!'
    
    return results_page(state)


def filter_expression(input_str: str)-> list[str]:    
    '''
    Args:
        string
    Returns:
        list of strings
        
        
    Attempts to turn any string into a list of strings.
    Should the string have
        any character other than the integers and allowed operators,
        or duplicate decimals,
        these characters will be ignored.
    Then, the string is translated into a list of numbers and operators.
        Sequential integers are grouped up, then appended.
        Operators are immediately appended.
    Lastly, the list is checked for
        implicit multiplication, consecutive operators, and negatives.
    '''
    decimal_possible = True
    special_negative = 0
    opps_list = ['+','-','*','/','^']
    filtered_list = []
    expression_list = []
    num_str = ''
    for character in input_str.replace(' ', ''):
        if character in ['0','1','2','3','4','5','6','7','8','9']:
            num_str += character
            
        elif character == '.' and decimal_possible:
            decimal_possible = False
            num_str += '.'
            
        elif character in ['+','-','*','/','^','(',')']:
            decimal_possible = True
            if num_str:
                filtered_list.append(num_str)
                num_str = ''
            
            filtered_list.append(character)
    
    if num_str:
        filtered_list.append(num_str)
    
    for item in filtered_list:
        if expression_list:
            past_item = expression_list[-1]
            if item == '(' and past_item not in opps_list:
                if past_item != '(':
                    expression_list.append('*')
                    
                expression_list.append('(')
                
            elif past_item == ')' and item not in opps_list:
                expression_list.append(')')
                expression_list.append('*')
            
            elif item in opps_list and past_item in opps_list:
                if item == '-':
                    special_negative += 1
                    expression_list.append('(')
                    expression_list.append('-')
            
            elif special_negative and item not in opps_list:
                expression_list.append(item)
                while special_negative:
                    special_negative -= 1
                    expression_list.append(')')
                    
            else:
                expression_list.append(item)
        else:
            expression_list.append(item)

    return expression_list


def check_parentheses(expression_list: list[str])-> bool:
    '''
    Args:
        list of strings
    Returns:
        bool
    
    Checks if parentheses are paired.
    Returns False if:
        more/less of ( than )
        A ) appears before any (
    '''
    layer = 0
    for item in expression_list:
        if item == '(':
            layer += 1
            
        elif item == ')':
            layer -= 1
            
            if layer < 0:
                return False
            
    return layer == 0


def get_split_index(expression_list: list[str], operators: list[str])-> int:
    '''
    Args:
        list of strings(1), list of strings(2)
    Returns:
        integer
        
    Iterates backwards through the expression list to find the index of the 
    specified operators. It respects parentheses layers, returning the index 
    only if the operator is at the top layer (layer 0).
    '''
    layer = 0
    for index in range(len(expression_list)-1, -1, -1):
        character = expression_list[index]
        if character == ')':
            layer += 1
            
        elif character == '(':
            layer -= 1
            
        elif layer == 0 and character in operators:
            return index
        
    return -1


def build_pemdas_tree(expression_list: list[str])-> Side:
    '''
    Args:
        list of strings
    Returns:
        Side
        
    Recursively constructs a binary tree from the expression tokens.
    It handles parentheses by stripping outer layers and splits the expression 
        at the operator with the lowest precedence (Reverse PEMDAS) to ensure 
        the correct evaluation order.
    '''
    if not expression_list:
        return PemdasNum(0.0)
    
    if len(expression_list) == 1:
        return PemdasNum(float(expression_list[0]))

    if expression_list[0] == '(' and expression_list[-1] == ')':
        outside_parentheses = True
        first_char = True
        layer = 0
        for item in expression_list[:-1]:
            if item == '(':
                layer += 1
                
            elif item == ')':
                layer -= 1
                
            if layer == 0 and not first_char: 
                outside_parentheses = False
                break
            
            if first_char:
                first_char = False
        
        if outside_parentheses:
            return build_pemdas_tree(expression_list[1:-1])

    index = get_split_index(expression_list, ['+', '-'])
    
    if index != -1:
        return Pemdas(
            operator = expression_list[index],
            left = build_pemdas_tree(expression_list[:index]),
            right = build_pemdas_tree(expression_list[index+1:])
            )

    index = get_split_index(expression_list, ['*', '/'])
    
    if index != -1:
        return Pemdas(
            operator = expression_list[index],
            left = build_pemdas_tree(expression_list[:index]),
            right = build_pemdas_tree(expression_list[index+1:])
            )
            
    index = get_split_index(expression_list, ['^'])
    
    if index != -1:
        return Pemdas(
            operator = expression_list[index],
            left = build_pemdas_tree(expression_list[:index]),
            right = build_pemdas_tree(expression_list[index+1:])
            )


def pemdas_calc(state: State, side: Side)-> float:
    '''
    Args:
        Side
    Returns:
        float
    
    Recursive function that performs operations on a tree.
    Uses similar logic as to combined_calc(),
        operators / operations are saved in State.operators / State.steps.
    Raises ZeroDivisionError if dividing by zero.
    '''
    if isinstance(side, PemdasNum):
        return side.value
    
    first = pemdas_calc(state, side.left)
    second = pemdas_calc(state, side.right)
    first_formatted = comma_format(first)
    second_formatted = comma_format(second)
    
    if side.operator == '+':
        result = first + second
        state.operators.append('+')
        state.steps.append(f"{first_formatted} + {second_formatted} = {comma_format(result)}")
        return first + second
    
    elif side.operator == '-':
        result = first - second
        state.operators.append('−')
        state.steps.append(f"{first_formatted} − {second_formatted} = {comma_format(result)}")
        return result
    
    elif side.operator == '*':
        result = first * second
        state.operators.append('×')
        state.steps.append(f"{first_formatted} × {second_formatted} = {comma_format(result)}")
        return result
        
    elif side.operator == '/':
        if second:
            result = first / second
        else:
            raise ZeroDivisionError(first_formatted)
        
        state.operators.append('÷')
        state.steps.append(f"{first_formatted} ÷ {second_formatted} = {comma_format(result)}")
        return result
        
    elif side.operator == '^':
        result = first ** second
        state.operators.append('^')
        state.steps.append(f"{first_formatted} ^ {second_formatted} = {comma_format(result)}")
        return first ** second
        
    return 0.0

@route
def pemdas_order(state: State, input_str: str)-> Page:
    '''
    Args:
        State, string
    Returns:
        Page
        
    The main controller for the custom expression calculator.
    It filters the user's input, validates parentheses, rebuilds the string for display,
        constructs the operation tree, and recursively calculates the result.
    '''
    expression_list = filter_expression(input_str)
    expression_str = ''
    if expression_list:
        for index, item in enumerate(expression_list):
            if index:
                if item in ['+','-','*','/','^','(',')']:
                    if item == '^' or item == ')':
                         expression_str += item
                    else:
                         expression_str += ' ' + item
                         
                elif expression_list[index-1] == '^':
                    expression_str += comma_format(float(item))
                    
                elif expression_list[index-1] == '(':
                    expression_str += comma_format(float(item))
                    
                else:
                    expression_str += ' ' + comma_format(float(item))
            
            elif item in ['+','-','*','/','^','(']:
                expression_str += item
                
            else:
                expression_str += comma_format(float(item))
        
        state.last_equation = expression_str
    else:
        state.last_answer = 'Calculated nothing...'
        return results_page(state)

    if not check_parentheses(expression_list):
        state.last_answer = 'Check your parentheses!'
        return results_page(state)
    
    tree = build_pemdas_tree(expression_list)
    try:
        result = pemdas_calc(state, tree)
        state.last_answer = comma_format(result)
    except ZeroDivisionError as error:
        state.last_equation = error.args[0] + ' ÷ 0.0'
        state.last_answer = 'DNE'
    except Exception:
        state.last_answer = 'Error!'
    
    return results_page(state)

@route
def results_page(state: State)-> Page:
    '''
    Args:
        State
    Returns:
        Page
    
    Resets State and sets State.keep_answer to True when an answer exists.
    Displays a page to show the recent results.
    The user can choose an operation to continue with the previous answer
        or go back to the start page.
    '''
    state.history.append(Storage(
        state.last_equation + ' = ' + state.last_answer,
        list(state.operators), list(state.steps)
        ))
    state.option = ''
    state.operators = []
    state.steps = []
    if not state.last_answer == 'DNE' and not state.last_answer == 'Error!':
        state.keep_answer = True
    
    return Page(state, [
        Header('Result:', 3),
        state.history[-1].full_equation,
        HorizontalRule(),
        'Keep going with answer?',
        Row(Button('+', add_page), Button('−', sub_page), Button('×', mul_page), Button('÷', div_page)),
        Row(Button('xª', exp_page), Button('ª√x', roo_page)),
        'Use full equation?',
        Button('Continue writing...', pemdas_page),
        HorizontalRule(),
        Button('Back to start', index)
        ])



start_server(State(
    '', '', '', [], [], False,
    [Storage('Your last calculation will appear here!', [], [])]
    ))


#assert_equals
assert_equal(
 combined_calc(State(option='÷', last_equation='1.0 × 4.0', last_answer='4.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0'])]), '4.0', '5'),
 Page(state=State(option='',
                 last_equation='4.0 ÷ 5.0',
                 last_answer='0.8',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8'])]),
     content=[Header(body='Result:', level=3),
              '4.0 ÷ 5.0 = 0.8',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 index(State(option='', last_equation='', last_answer='', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[])])),
 Page(state=State(option='',
                 last_equation='',
                 last_answer='',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[])]),
     content=[Header(body='Choose operation mode:', level=3),
              'Simple:',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Advanced:',
              Button(text='Write your own!', url='/pemdas_page'),
              HorizontalRule(),
              'History:',
              'Your last calculation will appear here!',
              Button(text='History Page', url='/history_page')]))

assert_equal(
 roo_page(State(option='', last_equation='(0.8) ^ 6.0', last_answer='0.2621440000000001', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001'])])),
 Page(state=State(option='√',
                 last_equation='(0.8) ^ 6.0',
                 last_answer='0.2621440000000001',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001'])]),
     content=[Header(body='Root:', level=4),
              Div(TextBox(name='second_str', kind='text', default_value=''), '√(', TextBox(name='first_str', kind='text', default_value='0.2621440000000001'), ')', {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 combined_calc(State(option='+', last_equation='', last_answer='', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[])]), '1', ''),
 Page(state=State(option='',
                 last_equation='1.0 + 0.0',
                 last_answer='1.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0'])]),
     content=[Header(body='Result:', level=3),
              '1.0 + 0.0 = 1.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 div_page(State(option='', last_equation='(0.2621440000000001) ^ (1/6.0)', last_answer='0.8', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8'])])),
 Page(state=State(option='÷',
                 last_equation='(0.2621440000000001) ^ (1/6.0)',
                 last_answer='0.8',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8'])]),
     content=[Header(body='Division:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='0.8'), '÷', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 div_page(State(option='', last_equation='1.0 × 4.0', last_answer='4.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0'])])),
 Page(state=State(option='÷',
                 last_equation='1.0 × 4.0',
                 last_answer='4.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0'])]),
     content=[Header(body='Division:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='4.0'), '÷', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 combined_calc(State(option='−', last_equation='1.0 − 1.0', last_answer='0.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0'])]), '0.0', '2'),
 Page(state=State(option='',
                 last_equation='0.0 − 2.0',
                 last_answer='-2.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0'])]),
     content=[Header(body='Result:', level=3),
              '0.0 − 2.0 = -2.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 combined_calc(State(option='−', last_equation='0.0 − 2.0', last_answer='-2.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0'])]), '-2.0', '-3'),
 Page(state=State(option='',
                 last_equation='-2.0 + 3.0',
                 last_answer='1.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0'])]),
     content=[Header(body='Result:', level=3),
              '-2.0 + 3.0 = 1.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 sub_page(State(option='', last_equation='0.0 − 2.0', last_answer='-2.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0'])])),
 Page(state=State(option='−',
                 last_equation='0.0 − 2.0',
                 last_answer='-2.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0'])]),
     content=[Header(body='Subtraction:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='-2.0'), '−', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 pemdas_page(State(option='', last_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='36.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0'])])),
 Page(state=State(option='',
                 last_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='36.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0'])]),
     content=[Header(body='Enter an expression:', level=4),
              TextBox(name='input_str',
                      kind='text',
                      default_value='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0)'),
              'Please use these signs for your expression!',
              '+, -, *, /, ^, (, )',
              'Other characters are ignored',
              Button(text='Calculate!', url='/pemdas_order')]))

assert_equal(
 info_page(State(option='', last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='-4.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0']), Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0', operations=['−', '×', '÷', '−'], steps=['0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0'])]), 11),
 Page(state=State(option='',
                 last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='-4.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0']),
                          Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
                                  operations=['−', '×', '÷', '−'],
                                  steps=['0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0'])]),
     content=[Header(body='Calculation Details', level=3),
              'Equation:',
              '- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
              HorizontalRule(),
              'Operations performed (in order):',
              '+, +, ^, ×, −, ×, ÷, −, ÷, −',
              'Steps taken:',
              BulletedList(items=['1.0 + 2.0 = 3.0',
                                  '3.0 + 3.0 = 6.0',
                                  '6.0 ^ 2.0 = 36.0',
                                  '4.0 × 36.0 = 144.0',
                                  '0.0 − 3.0 = -3.0',
                                  '5.0 × -3.0 = -15.0',
                                  '-15.0 ÷ 5.0 = -3.0',
                                  '-3.0 − 1.0 = -4.0',
                                  '144.0 ÷ -4.0 = -36.0',
                                  '0.0 − -36.0 = 36.0'],
                           kind='ul'),
              HorizontalRule(),
              Button(text='Back to History', url='/history_page')]))

assert_equal(
 index(State(option='', last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='-4.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0']), Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0', operations=['−', '×', '÷', '−'], steps=['0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0'])])),
 Page(state=State(option='',
                 last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='-4.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0']),
                          Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
                                  operations=['−', '×', '÷', '−'],
                                  steps=['0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0'])]),
     content=[Header(body='Choose operation mode:', level=3),
              'Simple:',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Advanced:',
              Button(text='Write your own!', url='/pemdas_page'),
              HorizontalRule(),
              'History:',
              '(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
              Button(text='History Page', url='/history_page')]))

assert_equal(
 roo_page(State(option='', last_equation='0.8 ÷ 0.0', last_answer='DNE', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE'])])),
 Page(state=State(option='√',
                 last_equation='0.8 ÷ 0.0',
                 last_answer='DNE',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE'])]),
     content=[Header(body='Root:', level=4),
              Div(TextBox(name='second_str', kind='text', default_value=''), '√(', TextBox(name='first_str', kind='text', default_value=''), ')', {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 index(State(option='', last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='-4.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0']), Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0', operations=['−', '×', '÷', '−'], steps=['0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0'])])),
 Page(state=State(option='',
                 last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='-4.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0']),
                          Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
                                  operations=['−', '×', '÷', '−'],
                                  steps=['0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0'])]),
     content=[Header(body='Choose operation mode:', level=3),
              'Simple:',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Advanced:',
              Button(text='Write your own!', url='/pemdas_page'),
              HorizontalRule(),
              'History:',
              '(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
              Button(text='History Page', url='/history_page')]))

assert_equal(
 combined_calc(State(option='√', last_equation='0.8 ÷ 0.0', last_answer='DNE', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE'])]), '-1', '1'),
 Page(state=State(option='',
                 last_equation='(-1.0) ^ (1/1.0)',
                 last_answer='DNE',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE'])]),
     content=[Header(body='Result:', level=3),
              '(-1.0) ^ (1/1.0) = DNE',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 sub_page(State(option='', last_equation='1.0 − 1.0', last_answer='0.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0'])])),
 Page(state=State(option='−',
                 last_equation='1.0 − 1.0',
                 last_answer='0.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0'])]),
     content=[Header(body='Subtraction:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='0.0'), '−', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 exp_page(State(option='', last_equation='4.0 ÷ 5.0', last_answer='0.8', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8'])])),
 Page(state=State(option='^',
                 last_equation='4.0 ÷ 5.0',
                 last_answer='0.8',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8'])]),
     content=[Header(body='Exponential:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='0.8'), '^', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 add_page(State(option='', last_equation='', last_answer='', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[])])),
 Page(state=State(option='+',
                 last_equation='',
                 last_answer='',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[])]),
     content=[Header(body='Addition:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value=''), '+', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 combined_calc(State(option='√', last_equation='(0.8) ^ 6.0', last_answer='0.2621440000000001', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001'])]), '0.2621440000000001', '6'),
 Page(state=State(option='',
                 last_equation='(0.2621440000000001) ^ (1/6.0)',
                 last_answer='0.8',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8'])]),
     content=[Header(body='Result:', level=3),
              '(0.2621440000000001) ^ (1/6.0) = 0.8',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 add_page(State(option='', last_equation='1.0 + 0.0', last_answer='1.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0'])])),
 Page(state=State(option='+',
                 last_equation='1.0 + 0.0',
                 last_answer='1.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0'])]),
     content=[Header(body='Addition:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='1.0'), '+', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 combined_calc(State(option='^', last_equation='4.0 ÷ 5.0', last_answer='0.8', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8'])]), '0.8', '6'),
 Page(state=State(option='',
                 last_equation='(0.8) ^ 6.0',
                 last_answer='0.2621440000000001',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001'])]),
     content=[Header(body='Result:', level=3),
              '(0.8) ^ 6.0 = 0.2621440000000001',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 combined_calc(State(option='+', last_equation='1.0 + 0.0', last_answer='1.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0'])]), '1.0', '-1'),
 Page(state=State(option='',
                 last_equation='1.0 − 1.0',
                 last_answer='0.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0'])]),
     content=[Header(body='Result:', level=3),
              '1.0 − 1.0 = 0.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 pemdas_page(State(option='', last_equation='(-1.0) ^ (1/1.0)', last_answer='DNE', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE'])])),
 Page(state=State(option='',
                 last_equation='(-1.0) ^ (1/1.0)',
                 last_answer='DNE',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE'])]),
     content=[Header(body='Enter an expression:', level=4),
              TextBox(name='input_str', kind='text', default_value=''),
              'Please use these signs for your expression!',
              '+, -, *, /, ^, (, )',
              'Other characters are ignored',
              Button(text='Calculate!', url='/pemdas_order')]))

assert_equal(
 combined_calc(State(option='×', last_equation='-2.0 + 3.0', last_answer='1.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0'])]), '1.0', '4'),
 Page(state=State(option='',
                 last_equation='1.0 × 4.0',
                 last_answer='4.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0'])]),
     content=[Header(body='Result:', level=3),
              '1.0 × 4.0 = 4.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 pemdas_order(State(option='', last_equation='(-1.0) ^ (1/1.0)', last_answer='DNE', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE'])]), '- 4(1 + 2 + 3)^2 / (5 * -3 / 5 - 1)'),
 Page(state=State(option='',
                 last_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='36.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0'])]),
     content=[Header(body='Result:', level=3),
              '- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 combined_calc(State(option='÷', last_equation='(0.2621440000000001) ^ (1/6.0)', last_answer='0.8', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8'])]), '0.8', '0'),
 Page(state=State(option='',
                 last_equation='0.8 ÷ 0.0',
                 last_answer='DNE',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE'])]),
     content=[Header(body='Result:', level=3),
              '0.8 ÷ 0.0 = DNE',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 mul_page(State(option='', last_equation='-2.0 + 3.0', last_answer='1.0', operators=[], steps=[], keep_answer=True, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0'])])),
 Page(state=State(option='×',
                 last_equation='-2.0 + 3.0',
                 last_answer='1.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0'])]),
     content=[Header(body='Multiplication:', level=4),
              Div(TextBox(name='first_str', kind='text', default_value='1.0'), '×', TextBox(name='second_str', kind='text', default_value=''), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Button(text='Calculate!', url='/combined_calc')]))

assert_equal(
 pemdas_order(State(option='', last_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='36.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0'])]), '(5.0 * ( - 3.0) / 5.0 - 1.0)'),
 Page(state=State(option='',
                 last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='-4.0',
                 operators=[],
                 steps=[],
                 keep_answer=True,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0']),
                          Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
                                  operations=['−', '×', '÷', '−'],
                                  steps=['0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0'])]),
     content=[Header(body='Result:', level=3),
              '(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
              HorizontalRule(),
              'Keep going with answer?',
              Div(Button(text='+', url='/add_page'), Button(text='−', url='/sub_page'), Button(text='×', url='/mul_page'), Button(text='÷', url='/div_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div(Button(text='xª', url='/exp_page'), Button(text='ª√x', url='/roo_page'), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              'Use full equation?',
              Button(text='Continue writing...', url='/pemdas_page'),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))

assert_equal(
 history_page(State(option='', last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)', last_answer='-4.0', operators=[], steps=[], keep_answer=False, history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]), Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']), Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']), Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']), Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']), Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']), Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']), Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001', operations=['^'], steps=['0.8 ^ 6.0 = 0.2621440000000001']), Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8', operations=['√'], steps=['0.2621440000000001 ^ (1/6.0) = 0.8']), Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']), Storage(full_equation='(-1.0) ^ (1/1.0) = DNE', operations=['√'], steps=['-1.0 ^ (1/1.0) = DNE']), Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'], steps=['1.0 + 2.0 = 3.0', '3.0 + 3.0 = 6.0', '6.0 ^ 2.0 = 36.0', '4.0 × 36.0 = 144.0', '0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0', '144.0 ÷ -4.0 = -36.0', '0.0 − -36.0 = 36.0']), Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0', operations=['−', '×', '÷', '−'], steps=['0.0 − 3.0 = -3.0', '5.0 × -3.0 = -15.0', '-15.0 ÷ 5.0 = -3.0', '-3.0 − 1.0 = -4.0'])])),
 Page(state=State(option='',
                 last_equation='(5.0 * ( - 3.0) / 5.0 - 1.0)',
                 last_answer='-4.0',
                 operators=[],
                 steps=[],
                 keep_answer=False,
                 history=[Storage(full_equation='Your last calculation will appear here!', operations=[], steps=[]),
                          Storage(full_equation='1.0 + 0.0 = 1.0', operations=['+'], steps=['1.0 + 0.0 = 1.0']),
                          Storage(full_equation='1.0 − 1.0 = 0.0', operations=['+'], steps=['1.0 + -1.0 = 0.0']),
                          Storage(full_equation='0.0 − 2.0 = -2.0', operations=['−'], steps=['0.0 − 2.0 = -2.0']),
                          Storage(full_equation='-2.0 + 3.0 = 1.0', operations=['−'], steps=['-2.0 − -3.0 = 1.0']),
                          Storage(full_equation='1.0 × 4.0 = 4.0', operations=['×'], steps=['1.0 × 4.0 = 4.0']),
                          Storage(full_equation='4.0 ÷ 5.0 = 0.8', operations=['÷'], steps=['4.0 ÷ 5.0 = 0.8']),
                          Storage(full_equation='(0.8) ^ 6.0 = 0.2621440000000001',
                                  operations=['^'],
                                  steps=['0.8 ^ 6.0 = 0.2621440000000001']),
                          Storage(full_equation='(0.2621440000000001) ^ (1/6.0) = 0.8',
                                  operations=['√'],
                                  steps=['0.2621440000000001 ^ (1/6.0) = 0.8']),
                          Storage(full_equation='0.8 ÷ 0.0 = DNE', operations=['÷'], steps=['0.8 ÷ 0.0 = DNE']),
                          Storage(full_equation='(-1.0) ^ (1/1.0) = DNE',
                                  operations=['√'],
                                  steps=['-1.0 ^ (1/1.0) = DNE']),
                          Storage(full_equation='- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0',
                                  operations=['+', '+', '^', '×', '−', '×', '÷', '−', '÷', '−'],
                                  steps=['1.0 + 2.0 = 3.0',
                                         '3.0 + 3.0 = 6.0',
                                         '6.0 ^ 2.0 = 36.0',
                                         '4.0 × 36.0 = 144.0',
                                         '0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0',
                                         '144.0 ÷ -4.0 = -36.0',
                                         '0.0 − -36.0 = 36.0']),
                          Storage(full_equation='(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0',
                                  operations=['−', '×', '÷', '−'],
                                  steps=['0.0 − 3.0 = -3.0',
                                         '5.0 × -3.0 = -15.0',
                                         '-15.0 ÷ 5.0 = -3.0',
                                         '-3.0 − 1.0 = -4.0'])]),
     content=[Header(body='History page:', level=3),
              HorizontalRule(),
              Div('(5.0 * ( - 3.0) / 5.0 - 1.0) = -4.0', Button(text='Info', url='/info_page', arguments=[('history_index', 12)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('- 4.0 * (1.0 + 2.0 + 3.0)^2.0 / (5.0 * ( - 3.0) / 5.0 - 1.0) = 36.0', Button(text='Info', url='/info_page', arguments=[('history_index', 11)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('(-1.0) ^ (1/1.0) = DNE', Button(text='Info', url='/info_page', arguments=[('history_index', 10)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('0.8 ÷ 0.0 = DNE', Button(text='Info', url='/info_page', arguments=[('history_index', 9)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('(0.2621440000000001) ^ (1/6.0) = 0.8', Button(text='Info', url='/info_page', arguments=[('history_index', 8)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('(0.8) ^ 6.0 = 0.2621440000000001', Button(text='Info', url='/info_page', arguments=[('history_index', 7)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('4.0 ÷ 5.0 = 0.8', Button(text='Info', url='/info_page', arguments=[('history_index', 6)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('1.0 × 4.0 = 4.0', Button(text='Info', url='/info_page', arguments=[('history_index', 5)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('-2.0 + 3.0 = 1.0', Button(text='Info', url='/info_page', arguments=[('history_index', 4)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('0.0 − 2.0 = -2.0', Button(text='Info', url='/info_page', arguments=[('history_index', 3)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('1.0 − 1.0 = 0.0', Button(text='Info', url='/info_page', arguments=[('history_index', 2)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              Div('1.0 + 0.0 = 1.0', Button(text='Info', url='/info_page', arguments=[('history_index', 1)]), {'style_display': 'flex', 'style_flex_direction': 'row', 'style_align_items': 'center'}),
              HorizontalRule(),
              Button(text='Back to start', url='/')]))
