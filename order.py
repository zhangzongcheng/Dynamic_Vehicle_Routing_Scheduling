class Order:

    def __init__(self, id_, x, y, w, p, a, req_skill, dt_):

        """Construction method

        :param id_: int
        :param x: float
        :param y: float
        :param w: float
        :param p: float
        :param a: datetime object
        :param req_skill: list
        :param dt_: datetime object
        """

        """
        Attributes
        ----------

        --> id_ : int : unique ID of the order
        --> x_coor : float : x coordinate of the location of the order
        --> y_coor : float : y coordinate of the location of the order
        --> weight : float : priority (importance) of the order
        --> process_time : float : process time in minutes
        --> arrival_time : datetime : arrival time of the order
        --> req_skill : list : required skills
        --> deadline : datetime : deadline of the order

        --> is_outsource : boolean : whether it is completed by outsourcing or not.

        # Following parameters will be None if it is completed by using outsourcing.
        # Otherwise  they must have their corresponding values. 

        --> which_crew : int : ID of the crew to which it is assigned
        --> starting time : datetime : starting time of the order
        --> completion_time : datetime : completion time of the order
        --> waiting_time : float : how much time the order have been waiting in the system
        --> lateness : float : max{0, completion_time - deadline}  
        """

        self.id_ = id_
        self.x_coor = x
        self.y_coor = y
        self.weight = w
        self.process_time = p
        self.arrival_time = a
        self.req_skill = req_skill
        self.deadline = dt_

        self.is_outsource = None  # boolean
        self.which_crew = None  # crew id,  int
        self.starting_time = None  # datetime
        self.completion_time = None  # datetime
        self.waiting_time = None  # double (minutes)
        self.lateness = None  # double (minutes)
