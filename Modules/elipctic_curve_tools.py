from Modules.group_tools import *


def copy_curve(curve):
    help_curve = []
    for num in curve:
        help_curve.append(num)
    return help_curve


def is_elliptic(curve, regime):
    # curve - [y^2 y yx x^3 x^2 x^1 a]
    if curve[0] != 1 or curve[3] != 1:
        print("Given curve is not elliptic!")
        return False
    if regime:
        help_curve = copy_curve(curve)
        operation = [" + ", " + ", " + ", " + ", " + ", " + ", " + "]
        for point in range(0, len(curve)):
            if curve[point] < 0:
                help_curve[point] = abs(curve[point])
                operation[point] = " - "
        print("Elliptic curve: y^2" + operation[1] + str(help_curve[1]) + " * y" + operation[2] + str(
            help_curve[2]) + " * xy = x^3" + operation[4] + str(help_curve[4]) + " * x^2" + operation[5] + str(
            help_curve[5]) + " * x" + operation[6] + str(help_curve[6]))
    return curve


def is_point_on_elliptic_curve(x, y, f, curve, regime):
    if is_elliptic(curve, False) is False:
        return False
    a = (y ** 2 + curve[1] * y + curve[2] * x * y) % f
    b = (x ** 3 + curve[4] * x ** 2 + curve[5] * x + curve[6]) % f
    if (y ** 2 + curve[1] * y + curve[2] * x * y) % f == (x ** 3 + curve[4] * x ** 2 + curve[5] * x + curve[6]) % f:
        if regime:
            print("Point (" + str(x) + "," + str(y) + ") is on elliptic curve!")
        return True
    print("Point (" + str(x) + "," + str(y) + ") is not on elliptic curve!")
    return False
    # curve - [y^2 y yx x^3 x^2 x^1 a]


def order_of_ec(f, curve, regime):
    if is_elliptic(curve, True) is False:
        print("Given Curve is not Elliptic!")
        return False
    if curve[2] != 0:
        print("Not supported type of EC")
        return False
    line_points = []
    y_2_points = []
    for y in range(0, int(f / 2) + 1):
        y_2_points.append((y ** 2) % f)
    x_points = []
    x_side_points = []
    for x in range(0, f):
        x_points.append(x)
        x_side_points.append((x ** 3 + x ** 2 * curve[4] + x * curve[5] + curve[6]) % f)
    for x in range(0, f):
        x_side = x_side_points[x]
        points = find_point(x, x_side, y_2_points, f)
        if points is False:
            y_2 = "-"
            y = "-"
            points = "-"
        else:
            y_2 = points[0][1] ** 2
            y = "+-" + str(points[0][1])
        line_points.append([x, x_side, y_2, y, points])
    line_points.append(["∞", "-", "-", "∞", "[∞,∞]"])
    order = 0
    list_of_point = []
    for line in line_points:

        if regime:
            print(line)
        if line[4] == "[∞,∞]":
            list_of_point.append(line[4])
            order += 1
        elif line[4] != "-":
            if line[2] == 0:
                order += 1
                list_of_point.append(line[4][0])
            else:
                list_of_point.append(line[4][0])
                list_of_point.append(line[4][1])
                order += 2
    if regime:
        print("Order of E[F" + str(f) + "] is: " + str(order))
    return [order, list_of_point]


def find_sqrt_ec(x, field):
    for i in range(0, field):
        result = (i * i) % field
        if result == x:
            return i


def find_point(x, x_side, y_2_points, f):
    for y in range(0, len(y_2_points)):
        if x_side == y_2_points[y]:
            if y_2_points[y] == 0:
                return [[x, find_sqrt_ec(y_2_points[y], f)]]
            return [[x, find_sqrt_ec(y_2_points[y], f)], [x, -find_sqrt_ec(y_2_points[y], f)]]
    return False


def add_point(point_p, point_q, f, curve, regime):
    point_p = [point_p[0] % f, point_p[1] % f]
    point_q = [point_q[0] % f, point_q[1] % f]
    if not (is_point_on_elliptic_curve(point_p[0], point_p[1], f, curve, False) and is_point_on_elliptic_curve(
            point_q[0]
            , point_q[1], f
            , curve, False)):
        print("One or Two points, which were given, are not on E[F " + str(f) + "].")
        return False
    if point_p[0] != point_q[0]:
        a = (point_q[1] - point_p[1])
        b = find_inverse(point_q[0] - point_p[0], f, False)
        lambdas = a * b % f
        x_r = (lambdas ** 2 - point_q[0] - point_p[0]) % f
        r = [x_r, (lambdas * (point_p[0] - x_r) - point_p[1]) % f]
    elif point_p[0] == point_q[0] and point_p[1] == point_q[1] and point_p[1] != 0:
        a = (3 * point_p[0] ** 2 + curve[5]) % f
        b = find_inverse(2 * point_p[1], f, False)
        lambdas = a * b % f
        x_r = (lambdas ** 2 - 2 * point_p[0]) % f
        r = [x_r, (lambdas * (point_p[0] - x_r) - point_p[1]) % f]
    else:
        r = "[∞,∞]"
    if regime:
        print("P =  " + str(point_p) + ", Q =  " + str(point_q) + ", R = P + Q =  " + str(r))
    return r


def divisors(number):
    list_of_divisors = []
    for num in range(1, number + 1):
        if number % num == 0:
            list_of_divisors.append(num)
    return list_of_divisors


def order_of_point(point, f, curve, regime):
    order = 1
    help_point = [point[0], point[1]]
    while True:
        help_point = add_point(help_point, point, f, curve, False)
        order += 1
        if help_point == "[∞,∞]":
            if regime:
                print("Order is: " + str(order))
            return order


def order_of_points(f, curve):
    order_of_ec_value_points = order_of_ec(f, curve, False)
    if order_of_ec_value_points is False:
        return False
    list_of_orders = divisors(order_of_ec_value_points[0])
    list_of_point_orders = []
    for order in list_of_orders:
        list_of_point_orders.append([order])
    for point in order_of_ec_value_points[1]:
        if point == '[∞,∞]':
            order = 1
        else:
            order = order_of_point(point, f, curve, False)
        for i in range(0, len(list_of_point_orders)):
            if list_of_point_orders[i][0] == order:
                list_of_point_orders[i].append(point)
                break
    for line in list_of_point_orders:
        print(line)
    return list_of_point_orders


def possible_orders(order_of_curve, new_field):
    possible_orders_old = divisors(order_of_curve)
    possible_orders_field = divisors(new_field)
    possible_orders_new = []
    for order_old in possible_orders_old:
        for order_field in possible_orders_field:
            if order_old == order_field:
                possible_orders_new.append(order_field)
    print(possible_orders_new)
    return possible_orders_new


def mov_attack(secret, g, order):
    for i in range(1, order + 1):
        a = g ** i % (order + 1)
        if a == secret:
            print("Secret is: " + str(i))
            return i
    return True


def get_z_x_table(g, x):
    order = order_of_num(g, x)
    if order != len(find_group_mult(5, False)):
        print("Given G is not generator!")
        return False
    list_of_elements = []
    for i in range(0, order):
        list_of_elements.append((g ** i) % x)
    # form table
    list_of_table = []
    for element in list_of_elements:
        help_line = []
        for i in range(0, order):
            help_line.append((element ** i) % x)
        list_of_table.append(help_line)
    for line in list_of_table:
        print(line)
    return list_of_table

# is_elliptic([1, -1, 2, 1, -5, 3, 2])
# order_of_ec(7, [1, 0, 0, 1, 0, -1, -1],True)
# add_point([0,1],[0,-1],7,[1,0,0,1,0,1,1])
# print(order_of_points(5, [1, 0, 0, 1, 0, -1, 1]))
# order_of_point([4,1],5,[1,0,0,1,0,-1,1])
# print(possible_orders(36, 22))
# mov_attack(13,6,16)
# get_z_x_table(2, 5)
