import numpy as np
import re


Coxeter_type = input("Coxeter type (e.g.,A, B, C, D): ")

one_line_input = input("One-line notation is (e.g., -3 1 2): ")
one_line = [int(x) for x in one_line_input.split()]



def replace_zeros(seq, n):
    return [n if x == 0 else x for x in seq]

def convert_notation(notation, n):
    result = []
    i = 0
    while i < len(notation):
        if notation[i] == 's':
            i += 1
            num_str = ""
            while i < len(notation) and notation[i].isdigit():
                num_str += notation[i]
                i += 1
            num = int(num_str)
            result.append(n - num)
        elif notation[i] == 'r':
            result.append(n)
            i += 1
        else:
            i += 1
    return result



if Coxeter_type == 'A':
    def one_line_to_reflections(one_line):
        n = len(one_line) - 1
        reflections = []
        current_permutation = one_line[:]
        for i in range(n):
            for j in range(n - i):
                if current_permutation[j] > current_permutation[j + 1]:
                    current_permutation[j], current_permutation[j + 1] = current_permutation[j + 1], current_permutation[j]
                    reflections.append(f"s{j + 1}")
        return reflections
    reflections = one_line_to_reflections(one_line)
    reflection_numbers = [int(reflection[1:]) for reflection in reflections]
    reflection_numbers = reflection_numbers[::-1]
    print(f"w = {reflection_numbers}")

elif Coxeter_type in ['B', 'C']:
    def apply_swap(perm, i):
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
        return perm
    def apply_t(perm):
        perm[0] = -perm[0]
        return perm
    def convert_reflection_indices(reflections, n):
        return [idx if idx == n else (n - idx) for idx in reflections]
    current = one_line.copy()
    n = len(current)
    reflections = []
    for i in range(n):
        if current[i] < 0:
            for j in range(i, 0, -1):
                reflections.append(j)
                current = apply_swap(current, j - 1)
            reflections.append(n)
            current = apply_t(current)

    abs_perm = [abs(x) for x in current]
    for i in range(n):
        for j in range(0, n - i - 1):
            if abs_perm[j] > abs_perm[j + 1]:
                reflections.append(j + 1)
                abs_perm[j], abs_perm[j + 1] = abs_perm[j + 1], abs_perm[j]
                current = apply_swap(current, j)
    converted_reflections = convert_reflection_indices(reflections, n)
    converted_reflections =converted_reflections[::-1]
    print(f"Weyl element is (simple reflection form) : {converted_reflections}")
    #print(f"Weyl element is (Geck's reflection & 0 --> n) form : {w_final}")

elif Coxeter_type == 'D':
    def get_reflection_product(w):
        n = len(w)
        operations = []
        while True:
            natural_order = list(range(1, n + 1))
            if w == natural_order:
                break
            s_applied = False
            for i in range(n - 1):
                if w[i] > w[i + 1]:
                    w[i], w[i + 1] = w[i + 1], w[i]
                    operations.insert(0, f's{i + 1}')
                    s_applied = True
                    break
            if not s_applied:
                w[0], w[1] = -w[1], -w[0]
                operations.insert(0, 'r')
        return ''.join(operations)


    def apply_operations(w, operations):
        for op in reversed(operations):
            if op.startswith('s'):
                index = int(op[1:]) - 1
                w[index], w[index + 1] = w[index + 1], w[index]
            elif op == 'r':
                w[0], w[1] = -w[1], -w[0]
        return w

    result1 = get_reflection_product(one_line.copy())
    #print(f"The final inverse map is : {result1}")
    converted_list = convert_notation(result1, len(one_line))
    #reversed_converted = converted_list[::-1]

    print(f"Weyl element is (simple reflection form): {converted_list}")
    #print(f"Weyl element is (Geck's reflection & 0 --> n) form: {w_final}")











