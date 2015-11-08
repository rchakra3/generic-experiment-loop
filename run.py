from model.schaffer import Schaffer
from model.osyczka2 import Osyczka2
from model.kursawe import Kursawe
from model.golinski import Golinski
from optimizer.sa import sa
from optimizer.mws import mws
from optimizer.de import de
from optimizer.ga import ga


for model in [Schaffer, Osyczka2, Kursawe, Golinski]:

    era_size = 10

    era0 = []

    ga(model())

    # while(len(era0) < era_size):
    #     model_instance = model()
    #     can = model_instance.gen_candidate()
    #     if can:
    #         era0 += [can]

    # for optimizer in [de, sa, mws]:
    #     print "\n*****************************"
    #     print optimizer.__name__ + "(" + model.__name__ + ")"
    #     optimizer(model_instance, threshold=-1, era_size=era_size, era0=era0)
    #     print "*****************************\n"
