from model.schaffer import Schaffer
from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
from model.golinski import Golinski
from optimizer.sa import sa
from optimizer.mws import mws
from optimizer.de import de


for model in [Schaffer, Osyczka2, Kursawe, Golinski]:
    for optimizer in [de]:  # , sa, mws]:
        print "\n*****************************"
        print optimizer.__name__ + "(" + model.__name__ + ")"
        optimizer(model(), threshold=-1)
        print "*****************************\n"
