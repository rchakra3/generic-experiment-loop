from model import Model
from helpers.decision import Decision
import math


class Golinski(Model):

    def __init__(self):
        Model.__init__(self)
        self.initialize_decs()

    def initialize_decs(self):
        dec = Decision('x1', 2.6, 3.6)
        self.decs.append(dec)
        dec = Decision('x2', 0.7, 0.8)
        self.decs.append(dec)
        dec = Decision('x3', 17.0, 28.0)
        self.decs.append(dec)
        dec = Decision('x4', 7.3, 8.3)
        self.decs.append(dec)
        dec = Decision('x5', 7.3, 8.3)
        self.decs.append(dec)
        dec = Decision('x6', 2.9, 3.9)
        self.decs.append(dec)
        dec = Decision('x7', 5.0, 5.5)
        self.decs.append(dec)

    def f1(self, candidate):
        x1 = candidate.dec_vals[0]
        x2 = candidate.dec_vals[1]
        x3 = candidate.dec_vals[2]
        x4 = candidate.dec_vals[3]
        x5 = candidate.dec_vals[4]
        x6 = candidate.dec_vals[5]
        x7 = candidate.dec_vals[6]

        const1 = 0.7854 * x1 * (x2 ** 2)
        var1 = (10 * (x3 ** 2) / 3) + (14.933 * x3 - 43.0934)
        part1 = const1 * var1

        const2 = -1.508 * x1
        var2 = ((x6 ** 2) + (x7 ** 2))
        part2 = const2 * var2

        const3 = 7.477
        var3 = (x6 ** 3 + x7 ** 3)
        part3 = const3 * var3

        const4 = 0.7854
        var4 = (x4 * (x6 ** 2)) + (x5 * (x7 ** 2))
        part4 = const4 * var4

        return part1 + part2 + part3 + part4

    def f2(self, candidate):
        x2 = candidate.dec_vals[1]
        x3 = candidate.dec_vals[2]
        x4 = candidate.dec_vals[3]
        x6 = candidate.dec_vals[5]

        part1 = ((745.0 * x4) / (x2 * x3)) ** 2
        part2 = 1.69 * (10 ** 7)
        part3 = 0.1 * (x6 ** 3)

        return (math.sqrt(part1 + part2)) / part3

    def objectives(self):
        return [self.f1, self.f2]

    def aggregate(self, candidate):
        aggr = 0
        self.eval(candidate)
        for score in candidate.scores:
            aggr += score
        return aggr

    def ok(self, candidate, debug=False):

        if len(candidate.dec_vals) != 7:
            return False

        x1 = candidate.dec_vals[0]
        x2 = candidate.dec_vals[1]
        x3 = candidate.dec_vals[2]
        x4 = candidate.dec_vals[3]
        x5 = candidate.dec_vals[4]
        x6 = candidate.dec_vals[5]
        x7 = candidate.dec_vals[6]

        g1 = (((1.0 / (x1 * (x2 ** 2) * x3)) - (1.0 / 27)) <= 0)
        # print "g1:" + g1
        g2 = g1
        # print "g2:" + g2
        g3 = (((x4 ** 3) / (x2 * (x3 ** 2) * (x6 ** 4))) - (1 / 1.93) <= 0)
        # print "g3:" + g3
        g4 = (((x5 ** 3) / (x2 * x3 * (x7 ** 4))) - (1 / 1.93) <= 0)
        # print "g4:" + g4
        g5 = ((x2 * x3) - 40 <= 0)
        # print "g5:" + g5
        g6 = ((x1 / x2) - 12 <= 0)
        # print "g6:" + g6
        g7 = (5 - (x1 / x2) <= 0)
        # print "g7:" + g7
        g8 = (1.9 - x4 + 1.5 * x6 <= 0)
        # print "g8:" + g8
        g9 = (1.9 - x5 + 1.1 * x7 <= 0)
        # print "g9:" + g9
        g10 = self.f2(candidate) <= 1300
        # print "g10:" + g10

        a = 745 * (x5 / (x2 * x3))
        b = 1.575 * (10 ** 8)

        g11 = math.sqrt((a ** 2) + (b ** 2)) / (0.1 * (x3 ** 7)) <= 1100
        # print "g11:" + g11

        return (g1 and g2 and g3 and g4 and g5 and g6 and g7 and g7 and
                g8 and g9 and g10 and g11)
