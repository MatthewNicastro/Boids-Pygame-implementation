from pygameui.__screen_object__ import ScreenObject
import numpy as np
import pygame
from typing import List
from typing import Optional

class Boid(ScreenObject):
    def __init__(self, 
                 start_loc: List[int],  
                 max_speed: int,
                 influence: int,
                 min_dist: int,
                 obj_margin: int,
                 window_size: List[int],
                 cohesion_factor: float,
                 separation_factor: float,
                 align_factor: float,
                 color: Optional[List[int]] = [0,0,0],
                 base: Optional[int] = 11,
                 height: Optional[int] = 21, 
                 random_theta: Optional[bool] = True):
        '''
        Initialize the boid
        Parameters
        ----------
        start_loc : int[]
            Boids Starting location.
        max_speed : int
            Boids maximum speed.
        influence : int
            Radius of region at which boids influence one anthoer.
        min_dist : int
            Minimum separation distance between boids.
        obj_margin : int
            Minimum separation distance between boid and screen objects.
        window_size : int[]
            Size of the pygame window.
        cohesion : float
            Cohesion multiplication factor.
        separation : float
            Separation multiplicaiton factor.
        align : float
            Alignment multiplication factor.
        color : int[], optional
            Array of size 3 with each channel representing
            the red, green and blue channels for the boids color. 
            The default is [0,0,0].
        base : int, optional
            Base of boid triangle. The default is 11.
        height : int, optional
            Height of boid triangle. The default is 21.

        Returns
        -------
        None.

        '''
        super().__init__(start_loc, color, [])       
        self.speed = max_speed
        if random_theta: theta = 2 * np.pi * np.random.random()
        else: theta = np.pi 
        self.v = np.array([max_speed * np.sin(theta), max_speed * np.cos(theta)])
        
        self.inf_2 = influence * influence
        self.min_dist_2 = min_dist * min_dist
        self.obj_margin_2 = obj_margin * obj_margin
        self.jitter_direction = 1
        
        self.cohesion_factor = cohesion_factor 
        self.separation_factor = separation_factor 
        self.align_factor = align_factor 
        
        self.screen_size = np.array(window_size)
        self.dims = [base, height]
        self.points = None
        self.__build__()
        self.__rot__()
    
    def set_speed(self, speed): self.speed = speed
    def set_inf_2(self, influence): self.inf_2 = influence * influence
    def set_min_dist_2(self, min_dist): self.min_dist_2 = min_dist * min_dist
    def set_obj_margin_2(self, obj_margin): self.obj_margin_2 = obj_margin * obj_margin
    def set_cohesion_factor(self, cohesion_factor): self.cohesion_factor = cohesion_factor 
    def set_separation_factor(self, separation_factor): self.separation_factor = separation_factor 
    def set_align_factor(self, align_factor): self.align_factor = align_factor 
    
    def __build__(self):
        '''
        Builds the default boid traingle around the boids center. Default
        triangle starts at tge starting loc and move half the distance in base direction aswell 
        as heigh direction to the 3 points defining the triangle.

        Returns
        -------
        None.

        '''
        if self.points is None:
            self.points = np.array([[self.center[0] - self.dims[0]/2, self.center[1] - self.dims[1]/2], 
                                    [self.center[0], self.center[1] + self.dims[1]/2],
                                    [self.center[0] + self.dims[0]/2, self.center[1] - self.dims[1]/2]])
        else: 
            self.points[0] = [self.center[0] - self.dims[0]/2, self.center[1] - self.dims[1]/2]
            self.points[1] = [self.center[0], self.center[1] + self.dims[1]/2]
            self.points[2] = [self.center[0] + self.dims[0]/2, self.center[1] - self.dims[1]/2]
    
    def __bounded_domain__(self, 
                           influence: Optional[int] = 2, 
                           boundary: Optional[List[int]] = None, 
                           margin: Optional[int] = 100):
        '''
        Creates a bounded domain around the window with the supplied margin

        Parameters
        ----------
        influence : int, optional
            This is the factor by which to divide the limiting speed inorder 
            to keep the boid within the bounded domain. The default is 2.
        boundary: int[], optional
            The location of the outer boundry lines (where on the right side 
            should the boid turn). The default is the screen size. 
            *Note: the inner boundries are the x = 0, y = 0 lines.
        margin : int, optional
            Distance away from both the inner and outter boundries at which 
            to start turning the boid. The default is 100.
        
        Returns
        -------
        None.

        '''
        i = self.speed/influence
        if boundary is None: boundary = self.screen_size
        
        if self.center[1] > boundary[1] - margin:
            self.v[1] -= i
        if self.center[1] < margin:
            self.v[1] += i
        if self.center[0] > boundary[0] - margin:
            self.v[0] -= i
        if self.center[0] < margin:
            self.v[0] += i
    
    def __infinite_domain__(self): 
        '''
        Allows the boids to infinitely move around the screen, 
        in a modulo fashion.
        Returns
        -------
        None.

        '''
        self.center %= self.screen_size
            
    def __dist2__(self, other_center: List[float]) -> float:
        '''
        Calculates the distance squared between two points

        Parameters
        ----------
        other_center : float[]
            Array containing the x,y coords of the other object

        Returns
        -------
        float
            Squared distance between the two centers.

        '''
        diff = other_center - self.center 
        return np.dot(diff, diff)
    
    def __trans__(self):
        '''
        Moves the triangle at the supplied velocity x, y velocity in its forward direction.

        Parameters
        ----------
        v : int
            Speed at which to move the triangle

        Returns
        -------
        None.

        '''
        self.center = self.center + self.v
     
    def __rot__(self, rad: Optional[float] = 0.0):
        '''
        Rotate triangle around triangles center coordinates

        Parameters
        ----------
        theta : int
            Degree at which to rotate the triangle

        Returns
        -------
        None.

        '''
        if rad == 0.0: rad = np.arctan2(*self.v)
        cos = np.cos(rad)
        sin = np.sin(rad)
        
        rot_matrix = np.array([[cos, -sin], [sin, cos]])
        self.points = np.dot(self.points - self.center, rot_matrix) + self.center
        
    def cohesion(self, others):
        '''
        Finds the center of mass for the boid given 
        all of the other boids within said boids visual range, 
        and adjusts the boids velocity so that is points to the 
        center of mass. This adjustment is dependant of the 
        cohesion factor property.

        Parameters
        ----------
        others : Boid[]
            Array of all other boids.

        Returns
        -------
        None.

        '''
        m_center = np.array([0,0])
        neighbours = 0
        for b in others:
            if b != self and self.__dist2__(b.center) < self.inf_2:
                m_center = m_center + b.center
                neighbours += 1
        
        if neighbours > 0:
            m_center = m_center / neighbours
            self.v = self.v + (m_center - self.center) * self.cohesion_factor
    
    def separation(self, others: List, objs: Optional[List] = []):
        '''
        Affects boids speed by asserting the boid separates from all other boids
        as well as all objects of type ScreenObject on the screen by adjusting the velocity
        of the boid to repell by the separation factor.

        Parameters
        ----------
        others : Boid[]
            Array of all other boids.
        objs : ScreenObject[], optional
            Array of all ScreenObjects on the canvas.The default is None

        Returns
        -------
        None.

        '''
        sep = np.array([0,0])
        for b in others:
            if b != self and self.__dist2__(b.center) < self.min_dist_2:
                sep = sep + (self.center - b.center)
        if objs != []:
            for obj in objs:
                if self.__dist2__(obj.center) < self.obj_margin_2:
                    sep = sep + (self.center - obj.center)
        
        self.v = self.v + sep * self.separation_factor 
        
    def alignment(self, others: List):
        '''
        Affects the boids alignment by changing the velocity of 
        the boid by averaging all the others boids velocities within 
        the given boids perceptual range and incrementing the current boids 
        velocity by the alignment. 

        Parameters
        ----------
        others : Boid[]
            Array of all other boids.

        Returns
        -------
        None.

        '''
        vel = np.array([0,0])
        neighbours = 0
        for b in others:
            if b != self and self.__dist2__(b.center) < self.inf_2:
                vel = vel + b.v
                neighbours += 1
        if neighbours > 0:
            vel /= neighbours
            self.v = self.v + (vel - self.v) * self.align_factor
    
    def __jitter__(self, factor: float):
        '''
        Ocillates the boids forward direction [-factor, factor].

        Parameters
        ----------
        factor : float

        Returns
        -------
        None.

        '''
        self.jitter_direction *= -1
        self.__rot__(rad = self.jitter_direction * factor)
        
    def __noise__(self, factor: float):
        '''
        Adds random noise to boids current velocity in the range 
        [-factor, factor]

        Parameters
        ----------
        factor : float
            Absolute value of the boids for the boids random noise.

        Returns
        -------
        None.

        '''
        self.v += factor * (2 * (0.5 - np.random.random(2)))
    
    def __limit_speed__(self, s: float):
        '''
        Limits the boids velocity for each direction so that it
        does not exceed the max speed limit.

        Parameters
        ----------
        s : float
            Current speed

        Returns
        -------
        None.

        '''
        self.v = (self.v/s) * self.speed
    
    def __check_speed__(self, s: float):
        '''
        Checks if the current speed is above the max speed limit.

        Parameters
        ----------
        s : float
            Current speed

        Returns
        -------
        None.

        '''
        if s > self.speed: self.__limit_speed__(s)
    
    def move(self, 
             others: List, 
             objs: Optional[List] = [],
             noise_factor: Optional[float] = 0,
             always_limit_speed: Optional[bool] = False,
             jitter_factor: Optional[float] = 0):
        '''
        Sequence of funtion calls dictating how the boid should move. 
        Sequence: 
            Attract
            Separate
            Align
            If supplied add random noise
            Limit speed
            Keep within screen
            translate
            Build boid points in default configuration
            rotate boid points to current forward defined by velocity
            If supplied jitter

        Parameters
        ----------
        others : Boid[]
            Array of all other boids.
        objs : ScreenObject[], optional
            Array of ScreenObjects boids must avoid. The default is None
        noise_factor : float, optional
            Float representing how much noise to add to boids current forward. The default is None.
        always_limit_speed : boolean, optional
            Decides if the speed of the boids should always be limited. The default is False.
        jitter_factor : float, optional
            Float representing the bounds for the boids jittering
            Bounds are +- np.pi/jitter. The default is None.

        Returns
        -------
        None.

        '''
        self.cohesion(others)
        self.separation(others, objs)
        self.alignment(others)
        if noise_factor != 0.0: self.__noise__(noise_factor)

        s = np.sqrt(np.dot(self.v, self.v))
        if always_limit_speed: self.__limit_speed__(s)
        else: self.__check_speed__(s)
        
        self.__infinite_domain__()
        self.__trans__()
        self.__build__()
        self.__rot__()
        if jitter_factor > 0.0: self.__jitter__(np.pi/(2 * jitter_factor))
    
    def draw(self, screen: pygame.display): 
        '''
        Draws the boid on the pygame screen

        Parameters
        ----------
        screen : pygame.display
            Current pygame screen display

        Returns
        -------
        None.

        '''
        pygame.draw.polygon(screen, self.color, self.points)
