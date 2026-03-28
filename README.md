# Havoc 🚀

![Forged in 2008](https://img.shields.io/badge/Forged_in-2008-8A2BE2?style=for-the-badge)
![Forged on Arch Linux](https://img.shields.io/badge/Forged_on-Arch_Linux-1793d1?style=for-the-badge&logo=arch-linux)
![Powered by Python](https://img.shields.io/badge/Powered_by-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Engine Pygame](https://img.shields.io/badge/Engine-Pygame-green?style=for-the-badge)
![Data libxml2](https://img.shields.io/badge/Data-libxml2-orange?style=for-the-badge)


> **Before cloud telemetry, before local LLMs, and before off-the-shelf game engines... there was bare-metal math and raw Pygame.**

**A Time Capsule from 2008.** Before I was building Android OpenGL engines or working with Local AI Agents, I was building custom 2D physics and state machines from scratch in pure Python. I recently dug this project out of the archives and am open-sourcing it for historical purposes.

Built back when you had to understand trigonometry and geometry just to make a sprite move across a screen, it's a fun look back at the simple mechanics and memory management that was important at the time.

<p align="center">
  <video src="_matforvideo/havocgameplay_edited.mp4" width="100%" playsinline autoplay loop muted controls></video>
</p>

## 🛠️ The Tech Stack of the Gods
* **Python** (The sacred texts)
* **Pygame** (The hammer and anvil)
* **libxml2** (Because hardcoding is for scrubs)

To unleash this beast, simply drop this in your terminal:
```bash
python __init__.py
```

---

## 🧠 Core Architecture & Quirky Ideas

### 1. External Data Driven (XML)
No hardcoded levels. This old fella uses `libxml2` to rip game configurations straight from `data/game.xml`.
* **Level & Wave Management:** Defines levels, titles, and individual enemy waves like a true general orchestrating a war.
* **Spawn Control:** Dictates the exact X,Y spawn coordinates for absolute precision strikes from enemies like the `reddevil`.
* **Dynamic Dialog:** Stores groups of "hurtquotes" and "killquotes" in the XML, dynamically assigning them to enemies when they spawn so they can talk trash in real-time.

**Implementation:**
```xml
<!-- A small taste of game.xml -->
<wave>
    <enemy class="reddevil" x="30" y="30" />
    <enemy class="reddevil" x="130" y="30" />
</wave>
<hurtquotes>
    <quote id="1" text="My eyes\nwill never forgive\nyou!" />
</hurtquotes>
```

### 2. Dynamic Speech Bubbles (Because AI needs to BM)
* **Balloon System:** A big-brain `balloon` sprite class that calculates its own dimensions dynamically based on how much text it needs to spit.
* **Contextual Spawning:** Bubbles appear right next to the speaking entity, flipping left or right depending on screen position so you never miss the insult.
* **Triggers:** Enemies will literally taunt you upon killing you (killquotes) or scream in agony/rage when their HP drops (hurtquotes). BM at its finest.

**Implementation (`gameobjects.py`):**
```python
class balloon(pygame.sprite.Sprite):
    def __init__(self, txt, target, fontname, fontsize):
        # We don't do static images here. We calculate text dimensions dynamically.
        self.textlines = txt.split('\n')
        # ... math happens ...
        self.image = pygame.Surface((maxwidth + 30, maxheight + 30))
        # Custom polygon pointers are drawn on the fly based on where the enemy is standing.
```

### 3. Image Shattering / Object Breaking (Visual Carnage)
* **Sprite Chopping:** The `explosion` class doesn't just swap an image; it literally simulates objects breaking apart into jagged pieces when destroyed.
* **Quadrant Splitting:** Uses `pygame.transform.chop` to violently slice the destroyed entity's original PNG into four distinct, bloody quadrants.
* **Physics Particles:** Each sliced quadrant morphs into a `particle` object, flying off with randomized angles, rotation speeds, and fading alpha values to mimic the physical debris of your defeated foes.

**Implementation (`gameobjects.py`):**
```python
class explosion(pygame.sprite.Sprite):
    def __init__(self, pos, original_image):
        # Brutally slice the original PNG into 4 pieces of flying debris
        self.tl = pygame.transform.chop(self.image, (self.rect.width/2, 0, self.rect.width/2, self.rect.height))
        self.tr = pygame.transform.chop(self.image, (0, 0, self.rect.width/2, self.rect.height))
        # Give them velocity and watch them bleed.
```

### 4. Advanced Collision Detection (No BS Hitboxes)
* **Pixel-Perfect Accuracy:** Bounding boxes? Get out of here. This implements custom hitmasks mapping the alpha channels of PNGs to ensure collisions are based on the *actual drawn pixels* of the ships and lasers. If you dodged it visually, you dodged it mechanically.
*(Note: The `pixelperfect.py` module used for this was a legendary community snippet written by John Eriksson in 2006, released to the public domain. Respect your elders.)*

**Implementation (`gameobjects.py` & `pixelperfect.py`):**
```python
# Bounding box is just the appetizer
aliens_shots = pygame.sprite.groupcollide(self.shotsGroup, self.alienGroup, 0, 0)
for cshot in aliens_shots.keys():
    for calien in aliens_shots[cshot]:
        # The main course: true overlapping pixel mask check
        if pixelperfect.check_collision(cshot, calien):
            calien.hit(cshot.power) # Get rekt
```

### 5. Player Mechanics & Weaponry (Sweaty Tryhard Loadouts)
* **Resource Management:** Tracks your "Hull" (HP) and "Antimatter" (AM). AM regenerates over time and is your lifeblood for speed-boosting and unleashing absolute hellfire.
* **Advanced Weapon Targeting:**
    * `homingShot`: Literally tracks targets by calculating interception angles and adjusting its trajectory mid-flight. There is no escape.
    * `magneticShot`: Analyzes impact predictions against multiple targets and aggressively snaps to the closest poor soul.
    * Lazors were in the backburner at the time...

### 6. Enemy Artificial Intelligence (They Know What You're Doing)
* **State Machine:** Enemies don't just sit there waiting to die. They cycle through complex states: moving to waypoints, idling/drifting, aggressively engaging (circling or closing in), and attacking.
* **Evasion Maneuvers:** Enemies actively scan for your incoming projectiles. If your shot is detected within their danger zone, they calculate an evasion vector and violently attempt to dodge while firing back. They want you dead as much as you want them dead.

### 7. Visual Effects & UI (Eye Candy)
* **Rich Text Rendering:** A custom `text` class that essentially acts as a mini-HTML parser, supporting basic tags (e.g., `<span style="color: #FF0000...">`) for multi-colored, styled text with fade and stretch effects because standard fonts are boring.
* **Parallax Background:** A scrolling background system utilizing tiles and a dynamic, randomly generated starfield moving at different speeds to create dizzying depth. Welcome to space.

**Implementation (`text.py`):**
```python
class textLine:
    def parse_text(self):
        # We built our own mini-HTML parser for text rendering.
        # e.g., <html><body><p><span style="color:#FF0000">Warning! Critical Damage!</span></p></body></html>
```