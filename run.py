from model.schaffer import Schaffer
from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
from optimizers import sa, mws, de


for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [de, sa, mws]:
        print "\n*****************************"
        print optimizer.__name__ + "(" + model.__name__ + ")"
        optimizer(model())
        print "*****************************\n"
