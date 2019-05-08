import datetime as dt
import pandas as pd
import mert


class Order:

    def __init__(self, id_, loc, w, p, a, s, d_):

        self.id_ = id_  # int
        self.loc = loc  # tuple
        self.weight = w   # float
        self.process_time = p  # float
        self.arrival_time = a  # float
        self.skills = s  # list
        self.deadline = d_  # datetime

        # filled later

        self.is_outsource = None  # True if it is achieved by outsourcing; None otherwise
        self.which_crew = None  # int or none
        self.starting_time = None  # datetime
        self.completion_time = None  # datetime
        self.waiting_time = None  # float (minutes)


class Crew:

    def __init__(self, id_, s_t_, s_l_, init_route, have_skills):

        self.id_ = id_  # int
        self.starting_time = s_t_  # datetime
        self.starting_loc = s_l_  # tuple
        self.route = init_route  # list of Orders
        self.skills = have_skills  # list

        # fill later
        self.drop_time = None  # datetime


class Solution:

    def __init__(self, crews, outs):

        self.crews = crews
        self.outs = outs
        self.update()

    def update(self):
        """Whenever a change occurs in one of the routes in the system,
           this method has to be called since it re-adjusts the relevant
           attributes of the orders and crews

           :return: %INPLACE%
        """
        for order in self.outs:
            order.is_outsource = True
            order.completion_time = order.deadline
            order.waiting_time = (order.completion_time - order.arrival_time).seconds / 60.0

        for crew in self.crews:
            tmp = crew.starting_time
            for i, order in enumerate(crew.route):
                if i == 0:
                    tmp = tmp + dt.timedelta(minutes=mert.get_time(crew.starting_loc, order.loc))
                else:
                    previous_order = crew.route[i-1]
                    tmp = tmp + dt.timedelta(minutes=mert.get_time(previous_order.loc, order.loc))

                order.which_crew = crew.id_
                order.starting_time = max(tmp, order.arrival_time)
                tmp = order.starting_time + dt.timedelta(minutes=order.process_time)
                order.completion_time = tmp
                order.waiting_time = (order.completion_time - order.arrival_time).seconds / 60.0

            if len(crew.route) > 0:
                crew.drop_time = crew.route[-1].completion_time

    def get_obj_val(self):

        obj = sum([o.waiting_time*o.weight for crew in self.crews for o in crew.route])
        obj += sum([o.waiting_time*o.weight for o in self.outs])
        return obj

    def is_feasible(self):

        # orders assigned to a crew must be completed before its deadline
        # crews cannot work after the end of the day
        flag = True
        for crew in self.crews:
            if crew.drop_time > mert.final_of_day:
                flag = False
                break
            for order in crew.route:
                if order.completion_time > order.deadline:
                    flag = False
                    break

        #skills
        if flag:
            for crew in self.crews:
                for order in crew.route:
                    for sk in range(len(order.skills)):
                        if crew.skills[sk] < order.skills[sk]:
                            flag = False
                            break

        return flag

    def __str__(self):

        print()
        print('Outsourced Orders: ', end="")
        for i,order in enumerate(self.outs):
            if i < len(self.outs)-1:
                print(str(order.id_) + '-', end="")
            else:
                print(str(order.id_), end="")
        print()
        for crew in self.crews:
            print('Route of the crew with ID ', str(crew.id_), ': ', end="")
            for i, order in enumerate(crew.route):
                if i < len(crew.route) - 1:
                    print(str(order.id_) + '-', end="")
                else:
                    print(str(order.id_), end="")
            print()

        print('Objective Function Value: ', str(self.get_obj_val()))
        print('Is Feasible: ', str(self.is_feasible()))
        print()
        _o_ = [o for crew in self.crews for o in crew.route]  # routed order
        for o in self.outs:
            _o_.append(o)
        _o_ = sorted(_o_, key=lambda x: x.id_)

        id_, w, p = [o.id_ for o in _o_], [o.weight for o in _o_], [o.process_time for o in _o_]
        a_t, d_ = [o.arrival_time.time() for o in _o_], [o.deadline.time() for o in _o_]

        ind_ = ['Outsource' if o.is_outsource else 'Crew '+str(o.which_crew) for o in _o_]
        c_ = [o.completion_time.time() for o in _o_]
        a_ = [o.waiting_time for o in _o_]

        df = pd.DataFrame()
        df['ID'] = id_
        # df['Process Time'] = p
        df['Arrival Time'] = a_t
        df['Deadline'] = d_
        df['Decision'] = ind_
        df['Completion Time'] = c_
        df['Waiting Time'] = a_
        df['Weight'] = w

        print(df)
