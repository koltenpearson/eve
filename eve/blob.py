import numpy as np
import math

class trace_point :

    def __init__(self, x, y) :
        self.x = x
        self. y = y

    def __eq__ (self, other) :
        if (self.x == other.x and self.y == other.y) :
            return True
        else :
            return False

    def __ne__ (self, other) :
        if self == other :
            return False
        else :
            return True

    def __hash__(self) :
        return int(str(self.x) +str(self.y))

    def __add__(self, other) :
        return trace_point(self.x + other.x, self.y + other.y)

    def __sub__(self, other) :
        return trace_point(self.x - other.x, self.y - other.y)

    def __repr__(self) :
        return "(" + str(self.x) + " , " + str(self.y) + ")"


class trace :

    ##okay so x is the x coordint of the seed point, b is the y coordinate of the seed point
    # b_check(x,y) is a function, returns true if the point flagged on the image false if otherwise (flagged = out of bounds of interest)
    def __init__(self, x, y, b_check) :
        self.init_p = trace_point(x, y)
        self.b_check = b_check

        self.points = set()
        self.points.add(self.init_p)

    def __len__(self) :
        return len(self.points)


    def _get_next_delta(self, delta) :
        if (delta == trace_point(-1,-1)) :
            return trace_point(0, -1)
        elif (delta == trace_point(0, -1)) :
            return trace_point(1, -1)
        elif (delta == trace_point(1, -1)) :
            return trace_point(1, 0)
        elif (delta == trace_point(1, 0)) :
            return trace_point(1, 1)
        elif (delta == trace_point(1, 1)) :
            return trace_point(0, 1)
        elif (delta == trace_point(0, 1)) :
            return trace_point(-1, 1)
        elif (delta == trace_point(-1, 1)) :
            return trace_point(-1, 0)
        elif (delta == trace_point(-1, 0)) :
            return trace_point(-1, -1)

    def _next_point(self, cpoint, lpoint) :

        delta = lpoint - cpoint
        delta = self._get_next_delta(delta)
        lpoint = cpoint + delta
        while (self.b_check(lpoint.x, lpoint.y)) :
            delta = self._get_next_delta(delta)
            lpoint = cpoint + delta
        return lpoint

    def _single_pixel_check(self) :
        count = 0
        next_point = self.init_p + trace_point(-1, -1)
        for i in range(8) :
            if (self.b_check(next_point.x, next_point.y)) :
                count += 1
            else :
                break
            next_point = self.init_p + self._get_next_delta(next_point - self.init_p )

        if (count == 8) :
            return True
        else :
            return False


    def trace_bounds(self) :
        if self._single_pixel_check() :
            return

        next_point = self.init_p + trace_point(-1, -1)
        current_point = self.init_p
        next_point = self._next_point(self.init_p, next_point)

        while (next_point != self.init_p) :
            temp = current_point
            current_point = next_point
            next_point = self._next_point(current_point, temp)
            self.points.add(current_point)

    def fill_bounds(self) :

        filled = set()
        
        for p in self.points :
            filled.add(p)
            for dx in (trace_point(-1,0),  trace_point(1,0)) :
                current = p + dx
                while (current not in filled and not self.b_check(current.x, current.y)) :
                    filled.add(current)
                    current += dx

        self.points = filled



def test_checker(x, y) :
    index = y * 11 + x

    print("checking {}, {}".format(x,y))

    if (test2[index] == 1) :
        print("true")
        return True
    else :
        print("false")
        return False

def test() :

    t = trace(3, 2, test_checker)
    t.trace_bounds()
    print(t.points)
    t.fill_bounds()
    print(t.points)


test1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

test2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
         0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0,
         0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0,
         0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

test3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
         0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,
         0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0,
         0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
         0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
