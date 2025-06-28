import math
import random

class Drone:
    def __init__(self, drone_id, initial_position):
        self.id = drone_id
        self.position = initial_position
        self.waypoints = []
        self.current_wp_index = 0
        self.speed = 10 # units per second

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints

    def distance_to_wp(self):
        if self.current_wp_index >= len(self.waypoints):
            return None
        wp = self.waypoints[self.current_wp_index]
        return math.dist(self.position, wp)

    def step(self, dt):
        # FAILURE MODES
        # Failure mode: delay at waypoint
        if hasattr(self, "failure_modes") and self.failure_modes.get("delay_at_wp", 0) > 0:
            if not hasattr(self, "_delay_timer"):
                self._delay_timer = 0
            if self.distance_to_wp() < 0.1:
                if self._delay_timer < self.failure_modes["delay_at_wp"]:
                    self._delay_timer += dt
                    return False # delay, do not move on
                else:
                    self._delay_timer = 0
                    self.current_wp_index += 1
                    return False

        # Failure mode: position drift
        if hasattr(self, 'failure_modes') and self.failure_modes.get('position_drift', 0) > 0:
            drift = self.failure_modes['position_drift']
            self.position[0] += random.uniform(-drift, drift) * dt
            self.position[1] += random.uniform(-drift, drift) * dt

        # Linear movement towards current waypoint
        if self.current_wp_index >= len(self.waypoints):
            return True

        wp = self.waypoints[self.current_wp_index]
        dist = self.distance_to_wp()

        if dist < 0.1: # reached waypoint
            self.current_wp_index += 1
            return False

        direction = [(wp[0] - self.position[0]) / dist, (wp[1] - self.position[1]) / dist]
        move_dist = min(self.speed * dt, dist)
        self.position = [self.position[0] + direction[0] * move_dist,
                         self.position[1] + direction[1] * move_dist]
        return False
