

class Crew:

    def __init__(self, id_, s_t_, s_l_, init_route, have_skills, last_t):

        """ Construction method

        :param id_: int
        :param s_t_: datetime
        :param s_l_: datetime
        :param init_route: list of Order objects
        :param have_skills: list
        :param last_t: datetime
        """

        """
        Attributes
        ----------
        
        --> id_ : int : unique ID of the crew
        --> starting_time : datetime : first available time of the crew
        --> starting_loc : tuple : x and y coordinates of the first available locations of the crew
        --> route : list : sequence of the orders the crew will visit
        --> skills : list : list of the skill the crew has
        --> last_time : datetime : limit for overtime of the crew
        --> drop_time : datetime : the time all of the orders of the crews are completed
        --> overtime : float : how many minutes the crew works in overtime.

        """
        self.id_ = id_
        self.starting_time = s_t_
        self.starting_loc = s_l_
        self.route = init_route
        self.skills = have_skills
        self.last_time = last_t

        self.drop_time = None
        self.overtime = None
