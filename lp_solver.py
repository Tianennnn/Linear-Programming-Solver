import sys
from fractions import Fraction

def getData():
    """
    extract the data from the standard input.
    """
    data = []
    for line in sys.stdin:
        line = line.split( )
        data.append(line)
    return data

def convertDict(data):
    """
    convert the data into dictionary form.
    """
    data[0][-1] = data[0][-1].replace('\n', '')
    data[0].append('0')
    for n in range(len(data[0])-1, 0, -1):
        data[0][n] = Fraction(data[0][n-1])
    data[0][0]=0


    for i in range(1,len(data)):
        data[i][-1] = data[i][-1].replace('\n', '')

        val = Fraction(data[i][-1])
        for j in range(len(data[i])-1,0, -1):
            data[i][j]= - Fraction(data[i][j-1])
        data[i][0] = val

        # append the coefficient of slack variable to the front
        data[i].append('0')
        for j in range(len(data[i])-1,0, -1):
            data[i][j]= Fraction(data[i][j-1])
        data[i][0] = Fraction(1)

    return data

def get_dict_variables(dict):
    non_basic=[]
    subscript=1
    for i in range(1, len(dict[0])):
        non_basic.append('x'+str(subscript))
        subscript = subscript+1

    basic=[]
    subscript=1
    for j in range(1, len(dict)):
        basic.append('w'+str(subscript))
        subscript = subscript+1

    dict_variables = []
    dict_variables.append(non_basic)
    dict_variables.append(basic)
    return dict_variables


def is_unbounded(dict)->bool:
    """
    A dictionary is unbounded if the coefficients of the non-basic variable in a
    column are all positive.
    """
    for i in range(1,len(dict[0])):
        if (dict[0][i]>0):
            for j in range(1, len(dict)):
                if (dict[j][i+1]<0):
                    break
                if j == (len(dict)-1):
                    return True
    return False

def is_initially_infeasible(dict)->bool:
    """
    A dictioanry is initially infeasible if any of the basic variables is negative.
    """
    for i in range(1, len(dict)):
        if(dict[i][1]<0):
            return True
    return False

def is_optimal(dict)->bool:
    """
    The optimal solution is attained when all the coefficients of the variables
    in the objective function are negative.
    """
    for i in range(1,len(dict[0])):
        if (dict[0][i]>0):
            return False
    return True

def choose_leaving_var(dict, index):
    """
    return the index of chosen leaving variable
    """
    var_index = index+1
    min = -1
    min_index = -1
    for i in range(1, len(dict)):
        # i for the i-th constraint
        if (dict[i][var_index]<0):
            val = Fraction(dict[i][1], (-dict[i][var_index]))
            if (min==-1) or (val<min):
                min = val
                min_index = i
    return min_index

def largest_increase(dict):
    """
    return the index of chosen entering variable using the Largest-Increase Rule
    """
    temp_list = []
    for i in range(1, len(dict[0])):
        # i for the i-th non-basic variable
        obj_increase_val = -2
        if(dict[0][i]>0):
            index = choose_leaving_var(dict, i)
            var_increase_val = Fraction(dict[index][1], (-dict[index][i+1]))
            obj_increase_val = Fraction(dict[0][i]) * var_increase_val
        temp_list.append(obj_increase_val)

    max = -1
    max_index = -1
    for j in range(0, len(temp_list)):
         if temp_list[j]>max:
             max = temp_list[j]
             max_index = j
    return max_index+1

def bland(dict,dict_variables):
    """
    return the index of chosen entering variable using the Bland's Rule
    """
    min = 'az'
    min_index = -1
    for i in range(0, len(dict_variables[0])):
        if(dict[0][i+1]>0):
            if dict_variables[0][i][0]>min[0]:   # The ascii value of w is smaller than x, so use '>' here
                min = dict_variables[0][i]
                min_index = i
            elif dict_variables[0][i][0]==min[0]:
                if dict_variables[0][i][1:]<min[1:]:
                    min = dict_variables[0][i]
                    min_index = i
    return min_index+1

def pivot(dict, dict_variables, entering_var_index):
    """
    perform a pivot operation on the given entering variable
    """
    leaving_var_index = choose_leaving_var(dict,entering_var_index)
    entering_var = dict_variables[0][entering_var_index-1]
    leaving_var = dict_variables[1][leaving_var_index-1]

    coefficient = -dict[leaving_var_index][entering_var_index+1]
    for i in range(0, len(dict[leaving_var_index])):
        dict[leaving_var_index][i] = dict[leaving_var_index][i] / coefficient

    temp = dict[leaving_var_index][0]   # stores the coefficient of the leaving_var_index
    dict[leaving_var_index][0] = -dict[leaving_var_index][entering_var_index+1]
    dict[leaving_var_index][entering_var_index+1] = -temp

    dict_variables[1][leaving_var_index-1] = entering_var

    # update the rest of the basis
    for i in range(1, len(dict)):
        if i != leaving_var_index:
            entering_var_coefficient = dict[i][entering_var_index+1]
            for j in range(1, len(dict[i])):
                dict[i][j] = dict[i][j] + entering_var_coefficient*dict[leaving_var_index][j]
            dict[i][entering_var_index+1] = entering_var_coefficient*dict[leaving_var_index][entering_var_index+1]

    # update the objective function
    entering_var_coefficient = dict[0][entering_var_index]
    for i in range(0,len(dict[0])):
        dict[0][i] = dict[0][i] + entering_var_coefficient*dict[leaving_var_index][i+1]
    dict[0][entering_var_index] = entering_var_coefficient*dict[leaving_var_index][entering_var_index+1]

    dict_variables[0][entering_var_index-1] = leaving_var

def print_optimal(dict, dict_variables, opti_variables):
    print('optimal')
    dict[0][0] = float(dict[0][0])
    if dict[0][0].is_integer():
        dict[0][0] = int(dict[0][0])
    print("%.7g" % dict[0][0])
    for i in range(0, len(opti_variables)):   # for each optimization variable
        for non_basic in dict_variables[0]:
            # if the optimization variable appear in the non_basic variables
            if opti_variables[i] == non_basic:
                opti_variables[i] = 0
                break
        if opti_variables[i]!=0:
            # if the optimization variable is not a non_basic variable
            index = 1
            for basis in dict_variables[1]:
                if opti_variables[i] == basis:
                    # Match the optimization variable with the basic variables in the dictionary
                    break
                index = index + 1
            opti_variables[i] = float(dict[index][1])
            if opti_variables[i].is_integer():
                opti_variables[i] = int(opti_variables[i])
    for var in opti_variables:
        print("%.7g" % var, end=' ')

def dict_copy(dict, dict_variables):
    """
    Return a copy of the input dictionary.
    """
    dict_copy = []
    for row in dict:
        copy_row=[]
        for coefficient in row:
            copy_row.append(coefficient)
        dict_copy.append(copy_row)

    variables_copy = []
    for row in dict_variables:
        copy_vars = []
        for var in row:
            copy_vars.append(var)
        variables_copy.append(copy_vars)
    return dict_copy, variables_copy

def if_list_same(list_1, list_2):
    """
    Check if list_1 and list_2 have the same elements, regardless of the order.
    """
    for element in list_1:
        if element not in list_2:
            return False
    return True

def if_cycle(dict, dict_variables, previous_non_basic_vars, initial_obj_val)->bool:
    """
    Return if the LP cycles. Or assign the dictionary to empty to indicate unboundedness.
    """
    while (is_optimal(dict)==False):
        if(is_unbounded(dict)):
            dict = []
            return
        entering_var_index = largest_increase(dict)
        pivot(dict, dict_variables, entering_var_index)

        obj_val = dict[0][0]
        if (obj_val==initial_obj_val):
            for non_basic_vars in previous_non_basic_vars:
                if(if_list_same(dict_variables[0], non_basic_vars)):
                    return True
            previous_non_basic_vars.append(dict_variables[0])
        else:
            return False

def get_dual_dict(dict):
    """
    return the dual of the input dictionary.
    """
    dual_dict = []
    for i in range(0,len(dict[0])):
        # i for i-th column in primal dict
        dual_row = []
        dual_row.append(-dict[0][i])
        for j in range(1,len(dict)):
            # j for j-th row in primal dict
            dual_row.append(-dict[j][i+1])
        dual_dict.append(dual_row)

    for basis in range(1, len(dual_dict)):
        # insert the coefficient of the slack variable to the front of each row of basis
        dual_dict[basis].insert(0,Fraction(1))

    return dual_dict

def get_dual_variables(dict_variables):
    dual_variables=[]

    dual_non_basic_vars = []
    for basic in dict_variables[1]:
        if (basic[0]=='x'):
            dual_non_basic = 'z'
        elif (basic[0]=='w'):
            dual_non_basic = 'y'
        elif (basic[0]=='z'):
            dual_non_basic = 'x'
        else:
            dual_non_basic = 'w'
        dual_non_basic = dual_non_basic + basic[1:]
        dual_non_basic_vars.append(dual_non_basic)
    dual_variables.append(dual_non_basic_vars)

    dual_basis = []
    for non_basic in dict_variables[0]:
        if (non_basic[0]=='x'):
            dual_basic = 'z'
        elif (non_basic[0]=='w'):
            dual_basic = 'y'
        elif (non_basic[0]=='z'):
            dual_basic = 'x'
        else:
            dual_basic = 'w'
        dual_basic = dual_basic + non_basic[1:]
        dual_basis.append(dual_basic)
    dual_variables.append(dual_basis)

    return dual_variables

def get_optimal(dict, dict_variables):
    """
    Perform pivot operations to get the optimal dictionary
    Return ([], []) if the dictionary is detected to be unbounded.
    """
    orig_dict, orig_variables=dict_copy(dict, dict_variables)
    while (is_optimal(dict)==False):
        if(is_unbounded(dict)):
            return [],[]
        # keep a record of the dictionary before pivoting
        last_obj_val = dict[0][0]
        last_non_basic_vars = []
        for var in dict_variables[0]:
            last_non_basic_vars.append(var)

        entering_var_index = largest_increase(dict)
        pivot(dict, dict_variables, entering_var_index)

        # check if degenerate
        obj_val = dict[0][0]
        if(obj_val==last_obj_val):  # if degenerate, check if cycle
            previous_non_basic_vars=[]
            previous_non_basic_vars.append(last_non_basic_vars)
            if (if_cycle(dict, dict_variables, previous_non_basic_vars, last_obj_val)):
                # if cycle then use Bland's Rule
                dict = orig_dict
                dict_variables = orig_variables
                while (is_optimal(dict)==False):
                    if(is_unbounded(dict)):
                        return [],[]
                    entering_var_index = bland(dict,dict_variables)
                    pivot(dict, dict_variables, entering_var_index)
    return dict, dict_variables

def primal_dual_method(dict, dict_variables):
    """
    Use primal-dual Method to return a initially feasible dictionary.
    """
    # store the original objective function
    orig_obj_coefficient = []
    for coefficient in dict[0]:
        orig_obj_coefficient.append(coefficient)
    orig_obj_vars = []
    for var in dict_variables[0]:
        orig_obj_vars.append(var)

    # modifify the dictionary
    for i in range(0, len(dict[0])):
        dict[0][i] = Fraction(0)
    # solve the dual and convert back to primal
    dict = get_dual_dict(dict)
    dict_variables = get_dual_variables(dict_variables)
    dict, dict_variables = get_optimal(dict, dict_variables)
    if dict ==[]:   #if unbounded
        print("infeasible")
        exit()
    dict = get_dual_dict(dict)
    dict_variables = get_dual_variables(dict_variables)

    # update the objective function
    for i in range(0,len(orig_obj_vars)):
        for j in range(0, len(dict_variables[0])):
            if orig_obj_vars[i] == dict_variables[0][j]:
                orig_index = i
                new_index = j
                dict[0][j+1] = dict[0][j+1]+ orig_obj_coefficient[i+1]
                break
        for j in range(0, len(dict_variables[1])):
            if orig_obj_vars[i] == dict_variables[1][j]:
                orig_index = i
                new_index = j
                for n in range(0, len(dict[0])):
                    dict[0][n] = dict[0][n] + orig_obj_coefficient[i+1]*dict[j+1][n+1]
    return dict, dict_variables

def main():
    data = getData()
    dict = convertDict(data)
    dict_variables = get_dict_variables(dict)
    opti_variables = []
    for opti_var in dict_variables[0]:
        opti_variables.append(opti_var)

    if(is_initially_infeasible(dict)):
        # if initially infeasible, then solve the dual if the dual is feasible
        dict = get_dual_dict(dict)
        dict_variables = get_dual_variables(dict_variables)
        if not is_initially_infeasible(dict):
            dict, dict_variables = get_optimal(dict, dict_variables)
            if dict ==[]:   #if unbounded
                print("infeasible")
                exit()
            dict = get_dual_dict(dict)
            dict_variables = get_dual_variables(dict_variables)
        else:   # if the dual is also initially infeasible, use the primal-dual method
            dict = get_dual_dict(dict)
            dict_variables = get_dual_variables(dict_variables)
            dict, dict_variables = primal_dual_method(dict, dict_variables)
            dict, dict_variables = get_optimal(dict, dict_variables)
            if dict ==[]:   #if unbounded
                print("unbounded")
                exit()
    else: # if initially feasible, then just solve
        dict, dict_variables = get_optimal(dict, dict_variables)
        if dict == []:  #if unbounded
            print("unbounded")
            exit()

    print_optimal(dict, dict_variables, opti_variables)


if __name__ == '__main__':
    main()
