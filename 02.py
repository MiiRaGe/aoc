from collections import defaultdict

l1 = list()

with open('./02.input', 'r') as f:
    line = f.readline()
    while line:
        l1.append([int(x) for x in line.split(' ')])
        line = f.readline()

def count_safe_report(l1):
    safe_report = 0
    for report in l1:
        is_safe = check_list(report)
        if is_safe:
            safe_report += 1
            continue
        for i in range(0, len(report)):
            is_safe = check_list(report[:i] + report[i+1:])
            if is_safe:
                safe_report += 1
                break
    return safe_report

def check_list(l):
    if l[0] == l[1]:
        return 0
    is_increasing = l[0] < l[1]
    for i, x in enumerate(l):
        try:
            diff = l[i+1] - l[i] 
            if is_increasing:
                if diff > 3 or diff <= 0:
                    return 0
            else:
                if diff < -3 or diff >= 0:
                    return 0
        except IndexError:
            pass
    return 1

if __name__ == '__main__':
    print(len(l1))
    print(count_safe_report(l1))