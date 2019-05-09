from environment import SimulationEnvironment
from method import *
from entity import *


o0 = Order(id_=0, loc=(0,0), w= 2, p=10, a=dt.datetime.strptime('13:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o1 = Order(id_=1, loc=(0,0), w= 4, p=10, a=dt.datetime.strptime('13:05:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o2 = Order(id_=2, loc=(0,0), w= 3, p=10, a=dt.datetime.strptime('13:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o3 = Order(id_=3, loc=(0,0), w= 1, p=10, a=dt.datetime.strptime('13:05:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o4 = Order(id_=4, loc=(0,0), w= 5, p=10, a=dt.datetime.strptime('13:10:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o5 = Order(id_=5, loc=(0,0), w= 2, p=10, a=dt.datetime.strptime('13:15:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o6 = Order(id_=6, loc=(0,0), w= 3, p=10, a=dt.datetime.strptime('13:15:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o7 = Order(id_=7, loc=(0,0), w= 1, p=10, a=dt.datetime.strptime('13:05:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o8 = Order(id_=8, loc=(0,0), w= 4, p=10, a=dt.datetime.strptime('13:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o9 = Order(id_=9, loc=(0,0), w= 4, p=10, a=dt.datetime.strptime('13:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o10 = Order(id_=10, loc=(0,0), w= 5, p=10, a=dt.datetime.strptime('13:10:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o11 = Order(id_=11, loc=(0,0), w= 5, p=10, a=dt.datetime.strptime('13:15:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

o12 = Order(id_=12, loc=(0,0), w= 1, p=10, a=dt.datetime.strptime('13:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('15:30:00', '%H:%M:%S'))

c1 = Crew(id_=1, s_t_=dt.datetime.strptime('13:04:00', '%H:%M:%S'), s_l_=(0,0),
          init_route=[o4, o3, o6, o5], have_skills=[5,5,5])
c2 = Crew(id_=2, s_t_=dt.datetime.strptime('13:17:00', '%H:%M:%S'), s_l_=(0,0),
          init_route=[o8, o9, o10, o11, o12], have_skills=[5,5,5])


o13 = Order(id_=13, loc=(0,0), w= 2, p=10, a=dt.datetime.strptime('14:00:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('19:08:00', '%H:%M:%S'))

o14 = Order(id_=14, loc=(0,0), w= 3, p=10, a=dt.datetime.strptime('14:10:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('16:30:00', '%H:%M:%S'))

o15 = Order(id_=15, loc=(0,0), w= 7, p=10, a=dt.datetime.strptime('14:05:00', '%H:%M:%S'),
           s=[2,5,3], d_=dt.datetime.strptime('17:00:00', '%H:%M:%S'))

precs = [(o4, o3), (o6, o5)]

crews = [c1, c2]
outs = [o1, o2, o7]

sol = Solution(crews, outs, precs)  # solution coming from previous planing horizon
new_orders = [o13, o14, o15]  # new orders

sim = SimulationEnvironment(sol, new_orders)
x = sim.apply_adaptive_large_neighborhood_search(2,3,1000,10,0)

x.__str__()