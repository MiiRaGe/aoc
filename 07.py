import re
import functools

extract_numbers_re = re.compile('^(\d+): (.*)$')

def  parse_input():
    equations = []
    with open('./07.input', 'r') as f:
        line = f.readline()
        while line:
            matched = extract_numbers_re.match(line)
            equations.append((int(matched.group(1)), tuple(int(x) for x in matched.group(2).split(' '))))
            line = f.readline()
    return equations


@functools.lru_cache(maxsize=1024)
def is_possible(target, acc, operands):
    if not operands and target != acc:
        return False
    if target == acc and operands:
        return False
    if target == acc and not operands:
        return True
    next_operand = operands[0]
    mult = next_operand * acc
    if mult <= target and is_possible(target, mult, operands[1:]):
        return True
    add = next_operand + acc
    if add <= target and is_possible(target, add, operands[1:]):
        return True
    return False

@functools.lru_cache(maxsize=1024)
def is_possible_v2(target, acc, operands, equation_str = ''):
    if not operands and target != acc:
        return False
    if target == acc and not operands:
        print(equation_str)
        return True
    next_operand = operands[0]
    mult = next_operand * acc
    if mult <= target and is_possible_v2(target, mult, operands[1:], equation_str + ' * %s' % next_operand):
        return True
    add = next_operand + acc
    if add <= target and is_possible_v2(target, add, operands[1:], equation_str + ' + %s' % next_operand):
        return True
    acc_str = str(acc)
    acc = int(acc_str + str(next_operand))
    return is_possible_v2(target, int(acc_str + str(next_operand)), operands[1:], equation_str + ' || %s' % next_operand)  
    
def brute_force(target, acc, operands):
    if not operands and target != acc:
        return False
    if target == acc and operands:
        return False
    if target == acc and not operands:
        return True
    if acc == 0:
        return brute_force(target, operands[0], operands[1:])


def sum_possible_equations(list_of_equations):
    possible_equations = [target for target, operands in list_of_equations if is_possible(target, operands[0], operands[1:])]
    impossible_equations = [(target,operands) for target, operands in list_of_equations if not is_possible(target, operands[0], operands[1:])]
    possible_equations_v2 = [target for target, operands in impossible_equations if is_possible_v2(target,operands[0], operands[1:], '%s: %s'%(target, operands[0]))]
    impossible_possible_equations_v2 = ["%s: %s" % (target, " ".join(str(x) for x in operands)) for target, operands in impossible_equations if not is_possible_v2(target,operands[0], operands[1:], '%s: %s'%(target, operands[0]))]
    return sum(possible_equations + possible_equations_v2)
        

if __name__ == "__main__":
    input = parse_input()
    print(sum_possible_equations(input))