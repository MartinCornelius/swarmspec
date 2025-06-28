# 🐝 swarmspec

**swarmspec** is a lightweight, modular testing framework for evaluating drone behavior in simulation or swarm scenarios. It provides a structured way to define, run, and visualize test cases against real or simulated drones — with support for failure injection, test acceleration, and real-time feedback.

> Built for research and prototyping — minimal, extensible, and focused.

---

## Features
* Define test cases in YAML
* Simulate drone movement and coordination
* Inject failure modes: GPS loss, battery drop, communication loss

---

## Example Scenarios (YAML)
```yaml
drones:
  - id: drone1
    initial_position: [0, 0]
    waypoints:
      - [100, 100]
      - [200, 50]
    failure_modes:
      delay_at_wp: 1 # seconds delay at each waypoints
      position_drift: 5 # meters max random drift
  - id: drone2
    initial_position: [50, 50]
    waypoints:
      - [150, 150]
      - [300, 100]

tolerance: 10  # meters
max_time: 60   # seconds per waypoint
```
