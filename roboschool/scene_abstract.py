# This is the only place cpp_household really imported. From other places, it is referenced as scene_abstract.cpp_household
# If this doesn't work, please see instructions in README on how to build Bullet physics library.

#from roboschool import cpp_household_d as cpp_household    # you can debug C++ code
from roboschool  import cpp_household   as cpp_household

import gym
import os

class Scene:
    "A base class for single- and multiplayer scenes"

    def __init__(self, gravity, timestep, frame_skip):
        self.np_random, seed = gym.utils.seeding.np_random(None)
        self.timestep = timestep
        self.frame_skip = frame_skip
        self.dt = self.timestep * self.frame_skip
        self.cpp_world = cpp_household.World(gravity, timestep)
        self.cpp_world.set_glsl_path(os.path.join(os.path.dirname(__file__), "cpp-household/glsl"))

        self.big_caption = self.cpp_world.test_window_big_caption  # that's a function you can call
        self.console_print = self.cpp_world.test_window_print      # this too

        self.test_window_still_open = True  # or never opened
        self.human_render_detected = False  # if user wants render("human"), we open test window

        self.multiplayer_robots = {}

    def test_window(self):
        "Call this function every frame, to see what's going on. Not necessary in learning."
        self.human_render_detected = True
        return self.test_window_still_open

    def actor_introduce(self, robot):
        "Usually after scene reset"
        if not self.multiplayer: return
        self.multiplayer_robots[robot.player_n] = robot

    def actor_is_active(self, robot):
        """
        Used by robots to see if they are free to exclusiveley put their HUD on the test window.
        Later can be used for click-focus robots.
        """
        return not self.multiplayer

    def episode_restart(self):
        "This function gets overridden by specific scene, to reset specific objects into their start positions"
        self.cpp_world.clean_everything()
        self.cpp_world.test_window_history_reset()

    def global_step(self):
        """
        The idea is: apply motor torques for all robots, then call global_step(), then collect
        observations from robots using step() with the same action.
        """
        if self.human_render_detected:
            self.test_window_still_open = self.cpp_world.test_window()
        self.cpp_world.step(self.frame_skip)

class SingleRobotEmptyScene(Scene):
    multiplayer = False  # this class is used "as is" for InvertedPundulum, Reacher
