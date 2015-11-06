from schaffer import Schaffer
from osyczka2 import Osyczka2
from kursawe import Kursawe
from optimizers import sa, mws


for model in [Schaffer, Osyczka2, Kursawe]:
    for optimizer in [sa, mws]:
        print "\n*****************************"
        print optimizer.__name__ + "(" + model.__name__ + ")"
        optimizer(model(), threshold=-1)
        print "*****************************\n"
