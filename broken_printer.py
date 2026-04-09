import sys
from collections import deque 

def backtrace(parent, start, end):
    if end == None:
        return "SEARCH FAILED"
    retval = end
    curr = end
    counter = 0
    while curr != start and counter < 1000:
        curr = parent[curr]
        retval = curr + "," + retval
        counter += 1
    return retval if curr == start else "SEARCH FAILED"

def compare_str(s1, s2):
    # print(len(s2))
    if len(s1) == 0 or len(s2) == 0:
        return False
    for i in range(len(s1)):
        if s1[i] == 'X' or s2[i] == 'X':
            continue
        if s1[i] != s2[i]:
            return False
    return True

def flip_bit(string, bit_idx):
    if string[bit_idx] == '0':
        return string[:bit_idx] + '1' + string[bit_idx + 1:]
    else:
        return string[:bit_idx] + '0' + string[bit_idx + 1:]

def bfs_search(start, goals, unsafe, length_string):
    parent = {}
    expanded = []
    fringe = deque([start])
    found_legal_state = False
    goal_found = None
    while len(fringe) > 0 and not found_legal_state:
        l = len(fringe)
        for _ in range(l):
            curr = fringe.popleft()
            for i in range(length_string):
                new_num = flip_bit(curr, i)
                is_unsafe = False
                for u in unsafe:
                    # return str(u)
                    is_unsafe = is_unsafe or compare_str(new_num, u)
                if not is_unsafe and new_num not in expanded and new_num not in fringe:
                    # print("original: " + curr + " flipped: " + new_num)
                    fringe.append(new_num)
                    parent[new_num] = curr
            expanded.append(curr)
            
            for g in goals:
                if compare_str(curr, g):
                    found_legal_state = True
                    goal_found = curr
                    break
            if len(expanded) >= 1000:
                break
            if found_legal_state:
                break
    path_to_goal = backtrace(parent, start, goal_found)
    return path_to_goal + "\n" + ",".join(expanded)
    

def dfs_search(start, goals, unsafe, length_string):
    parent = {}
    expanded = []
    fringe = deque([start])
    found_legal_state = False
    goal_found = None
    while len(fringe) > 0 and not found_legal_state:
        l = len(fringe)
        for _ in range(l):
            curr = fringe.popleft()
            temp_array = []
            # print("Current: " + curr)
            # print(fringe)
            for i in range(length_string):
                new_num = flip_bit(curr, i)
                is_unsafe = False
                for u in unsafe:
                    is_unsafe = is_unsafe or compare_str(new_num, u)
                if new_num in fringe:
                    fringe.remove(new_num)
                if not is_unsafe and new_num not in expanded:
                    # print("original: " + curr + " flipped: " + new_num)
                    temp_array.append(new_num)
                    parent[new_num] = curr
            expanded.append(curr)
            # print("lala")
            # print(temp_array)
            temp_array.reverse()
            # print(temp_array)
            fringe.extendleft(temp_array)

            for g in goals:
                if compare_str(curr, g):
                    found_legal_state = True
                    goal_found = curr
                    break
            if len(expanded) >= 1000:
                break
            if found_legal_state:
                break
    path_to_goal = backtrace(parent, start, goal_found)
    # print(expanded)
    return path_to_goal + "\n" + ",".join(expanded)

def ids_search(start, goals, unsafe, length_string):
    pass

def dfs_search_recursive(start, goals, unsafe, length_string, max_depth=1000):
    expanded = []
    goal_found = [None]
    path_to_goal = [None]
    def recursion(curr_depth, depth_limit, curr_path, curr):
        if curr_depth >= depth_limit or curr in curr_path or goal_found[0] is not None:
            return
        expanded.append(curr)
        # print(expanded)
        for g in goals:
            if compare_str(curr, g):
                goal_found[0] = curr
                path_to_goal[0] = curr_path[:] + [curr]
                return
        for i in range(length_string):
            new_num = flip_bit(curr, i)
            is_unsafe = False
            for u in unsafe:
                is_unsafe = is_unsafe or compare_str(new_num, u)
            if not is_unsafe and new_num not in expanded and new_num not in curr_path:
                curr_path.append(curr)
                recursion(curr_depth + 1, depth_limit, curr_path, new_num)
                curr_path.pop()
                if goal_found[0] is not None:
                    return

    recursion(0, max_depth, [], start)
    if(goal_found[0] is None or path_to_goal[0] is None):
        # return "SEARCH FAILED" + "\n" + ",".join(expanded)
        return "SEARCH FAILED", expanded
    # return ",".join(path_to_goal[0]) + "\n" + ",".join(expanded)
    return ",".join(path_to_goal[0]), expanded

def greedy_search(start, goals, unsafe, length_string):
    h_value = {}
    parent = {}
    expanded = []
    fringe = deque([start])
    
    h_value[start] = 0
    for k in goals:
        h_start = 0
        for l in range(len(start)):
            if start[l] != k[l]:
                h_start += 1
        if h_start > h_value[start]:
            h_value[start] = h_start
    # print(h_value[start])

    found_legal_state = False
    goal_found = None
    while len(fringe) > 0 and not found_legal_state:
        l = len(fringe)
        for _ in range(l):
            # curr = fringe.popleft()
            curr = None
            for m in fringe:
                if curr == None:
                    curr = m
                else:
                    if h_value[m] < h_value[curr]:
                        curr = m
            fringe.remove(curr)
                
            for i in range(length_string):
                new_num = flip_bit(curr, i)
                is_unsafe = False
                for u in unsafe:
                    is_unsafe = is_unsafe or compare_str(new_num, u)
                if not is_unsafe and new_num not in expanded and new_num not in fringe:
                    # print("original: " + curr + " flipped: " + new_num)
                    fringe.append(new_num)
                    h_value[new_num] = None
                    for k in goals:
                        heuristic = 0
                        for l in range(len(new_num)):
                            if new_num[l] != k[l]:
                                heuristic += 1
                                # print(l, heuristic)
                        if h_value[new_num] == None:
                            h_value[new_num] = heuristic
                        if heuristic < h_value[new_num]:
                            h_value[new_num] = heuristic
                    parent[new_num] = curr

                    # print(len(backtrace(parent, start, new_num).split(","))-1, "blahhh", new_num)
                    # print(new_num, h_value[new_num])
            expanded.append(curr)
            
            for g in goals:
                if compare_str(curr, g):
                    found_legal_state = True
                    goal_found = curr
                    break
            if len(expanded) >= 1000:
                break
            if found_legal_state:
                break
    path_to_goal = backtrace(parent, start, goal_found)
    return path_to_goal + "\n" + ",".join(expanded)

def astar_search(start, goals, unsafe, length_string):
    h_value = {}
    parent = {}
    expanded = []
    fringe = deque([start])
    
    h_value[start] = 0
    for k in goals:
        h_start = 0
        for l in range(len(start)):
            if start[l] != k[l]:
                h_start += 1
        if h_start > h_value[start]:
            h_value[start] = h_start
    # print(h_value[start])

    found_legal_state = False
    goal_found = None
    while len(fringe) > 0 and not found_legal_state:
        l = len(fringe)
        for _ in range(l):
            # curr = fringe.popleft()
            curr = None
            for m in fringe:
                if curr == None:
                    curr = m
                else:
                    if h_value[m] + len(backtrace(parent, start, m).split(","))-1 < h_value[curr] + len(backtrace(parent, start, curr).split(","))-1:
                        curr = m
            fringe.remove(curr)
                
            for i in range(length_string):
                new_num = flip_bit(curr, i)
                is_unsafe = False
                for u in unsafe:
                    is_unsafe = is_unsafe or compare_str(new_num, u)
                if not is_unsafe and new_num not in expanded and new_num not in fringe:
                    # print("original: " + curr + " flipped: " + new_num)
                    fringe.append(new_num)
                    h_value[new_num] = None
                    for k in goals:
                        heuristic = 0
                        for l in range(len(new_num)):
                            if new_num[l] != k[l]:
                                heuristic += 1
                                # print(l, heuristic)
                        if h_value[new_num] == None:
                            h_value[new_num] = heuristic
                        if heuristic < h_value[new_num]:
                            h_value[new_num] = heuristic
                    parent[new_num] = curr

                    # print(len(backtrace(parent, start, new_num).split(","))-1, "blahhh", new_num)
                    # print(new_num, h_value[new_num])
            expanded.append(curr)
            
            for g in goals:
                if compare_str(curr, g):
                    found_legal_state = True
                    goal_found = curr
                    break
            if len(expanded) >= 1000:
                break
            if found_legal_state:
                break
    path_to_goal = backtrace(parent, start, goal_found)
    return path_to_goal + "\n" + ",".join(expanded)

def hillclimb_search(start, goals, unsafe, length_string):
    h_value = {}
    parent = {}
    expanded = []
    fringe = deque([start])
    
    h_value[start] = None
    for k in goals:
        h_start = 0
        for l in range(len(start)):
            if start[l] != k[l]:
                h_start += 1
        if h_value[start] == None:
            h_value[start] = h_start
        if h_start < h_value[start]:
            h_value[start] = h_start
    # print(h_value[start])

    found_legal_state = False
    goal_found = None
    while len(fringe) > 0 and not found_legal_state:
        l = len(fringe)
        for _ in range(l):
            # curr = fringe.popleft()
            curr = None
            check = False
            for m in fringe:
                if len(backtrace(parent, start, m).split(",")) == len(start):
                    for g in goals:
                        if compare_str(m, g):
                            check = True
                    if check == False:
                        return "SEARCH FAILED" + "\n" + ",".join(expanded)
                if curr == None:
                    curr = m
                else:
                    if h_value[m] < h_value[curr]:
                        curr = m

            if curr == None:
                return "SEARCH FAILED" + "\n" + ",".join(expanded)
            fringe.remove(curr)
            fringe.clear()
                
            for i in range(length_string):
                new_num = flip_bit(curr, i)
                is_unsafe = False
                for u in unsafe:
                    is_unsafe = is_unsafe or compare_str(new_num, u)
                if not is_unsafe and new_num not in expanded and new_num not in fringe:
                    # print("original: " + curr + " flipped: " + new_num)
                    fringe.append(new_num)
                    h_value[new_num] = None
                    for k in goals:
                        heuristic = 0
                        for l in range(len(new_num)):
                            if new_num[l] != k[l]:
                                heuristic += 1
                                # print(l, heuristic)
                        if h_value[new_num] == None:
                            h_value[new_num] = heuristic
                        if heuristic < h_value[new_num]:
                            h_value[new_num] = heuristic
                    parent[new_num] = curr

                    # print(len(backtrace(parent, start, new_num).split(","))-1, "blahhh", new_num)
                    # print(new_num, h_value[new_num])
            expanded.append(curr)
            
            for g in goals:
                if compare_str(curr, g):
                    found_legal_state = True
                    goal_found = curr
                    break
            if len(expanded) >= 1000:
                break
            if found_legal_state:
                break
    path_to_goal = backtrace(parent, start, goal_found)
    return path_to_goal + "\n" + ",".join(expanded)

def broken_printer(char, filename):
    # TODO
    #open file and read its contents (will always be 3 lines of text)
    f = open(filename, "r")
    start = f.readline()
    if start[-1] == "\n":
        start = start[:-1]
    # return start
    length_string = len(start)
    goals = f.readline()
    if goals[-1] == '\n':
        goals = goals[:-1].split(",")
    # return goals[-1]
    unsafe = f.readline()
    if unsafe != '':
        if unsafe[-1] == '\n':
            unsafe = unsafe[:-1].split(",")
        else:
            unsafe = unsafe.split(",")
    # return unsafe[0]
    if char == 'B':
        return bfs_search(start, goals, unsafe, length_string)
    elif char == 'D':
        # return dfs_search_recursive(start, goals, unsafe, length_string)
        return dfs_search(start, goals, unsafe, length_string)
    elif char == 'I':
        path_to_goal = ""
        expanded = []
        i = 1
        while i < 100:
            ids_result = dfs_search_recursive(start, goals, unsafe, length_string, i)
            path_to_goal = ids_result[0]
            expanded += ids_result[1]
            i += 1

            if path_to_goal != "SEARCH FAILED":
                # print(expanded)
                return path_to_goal + "\n"  + ",".join(expanded)

        # return dfs_search_recursive(start, goals, unsafe, length_string)
    elif char == 'G':
        return greedy_search(start, goals, unsafe, length_string)
    elif char == 'A':
        return astar_search(start, goals, unsafe, length_string)
    elif char == 'H':
        return hillclimb_search(start, goals, unsafe, length_string)
    return ''


if __name__ == '__main__':
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        char = 'B'
        filename = 'example1.txt'
    else:
        char = sys.argv[1]
        filename = sys.argv[2]
    print(broken_printer(char, filename))
    # print("")
    # # print(broken_printer('D', 'example2.txt'))
    # print("")
    # print(broken_printer('B', 'example1.txt'))
    # print("")
    # # print(broken_printer('G', 'example1.txt'))
