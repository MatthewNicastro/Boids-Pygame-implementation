# Boids-Pygame-implementation
This is a simple boids implementation with pygame. 
Boids is a simple flocking algorithm first developed in 1986 by Craig Reynolds. The algorithm utilizes 3 main constraints cohesion, separation and alignment in order to dictate how the each boid behaves. If you would like to read more about the algorithm here is a link to its Wikipedia page:

https://en.wikipedia.org/wiki/Boids

The following implementation was done using Pygame. Pygame has no native UI support thus I decided to do my own UI implementation.
Some added features I have included are: 
- Random movement support 
- Jitter feature where the boids ossiclate with adjustable angle 
- The ability to always limit the boids speed, or only limit the boids speed if its greater than the maximum speed

**Installation**

Clone the repository

```git clone https://github.com/MatthewNicastro/Boids-Pygame-implementation```

Go to the cloned repository

```cd path/to/cloned repository```

(Optional) Create virtual environment

```python -m venv "NAME OF VIRTUAL ENVIRONMENT"```

Install requirements

```pip install -r requirements```

In certain cases try

```pip3 install -r requirements```

Run the simulation

```python main.py```
**Video demo**

Here is a video demo of my running the simulation and messing around with some of the features: 

<a href="https://www.youtube.com/watch?v=Y1uMH353CgU" target="_blank"><img src="http://img.youtube.com/vi/Y1uMH353CgU/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>
