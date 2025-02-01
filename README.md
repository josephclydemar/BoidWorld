# BoidWorld
Visualizes the collective movement of agents (boids) following simple rules to mimic natural flocking behavior. Each boid follows three rules: separation (avoiding crowding neighbors), alignment (matching velocity with nearby boids), and cohesion (steering towards the group’s center). The simulation dynamically adjusts to changing environments, creating emergent, lifelike swarm behavior.

<br>

### Instructions
#### Step 1: Install dependencies
```
pip install -r requirements.txt
```


#### Step 2: Run program
```
python ./src/main.py
```

<br>

---
### Summoner Controls
- Press `w` key to move forward.     
- Press `d` key to steer clockwise.     
- Press `a` key to steer counter-clockwise.
- Press `SPACE` key to speed up.
- Press `q` key to summon Boids.


<br>
<br>
<br>
<br>
<br>


---

<br>

### Block Orientation
```
      1e
 0c _______ 1c
   |       |
0e |       | 2e
   |_______|
 3c   3e    2c

```
