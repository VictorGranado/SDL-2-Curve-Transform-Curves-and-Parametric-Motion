# Curved Motion Visualizer — SDL 2 (Unit 2)

This project is an interactive Python application created for a Self-Directed Learning (SDL) project focused on Unit 2: Curved Motion. The goal of the tool is to make curve transformations and parametric motion easier to understand by allowing users to interact with curves and immediately see how equations affect shape and motion.

In class, many of these topics are handled algebraically, which can make it difficult to develop geometric intuition. This visualizer helps bridge that gap by displaying curves, transformations, and motion in real time. By experimenting with parameters and watching motion along curves, users can better understand how equations relate to geometry and movement.

---

## Project Purpose

This project was built to deepen understanding of the following Unit 2 topics:

- Graphing parabolas, ellipses, and hyperbolas
- Understanding how translations and stretching affect curves
- Modeling motion using parametric equations
- Interpreting velocity and acceleration along a curve

Instead of only solving equations symbolically, this tool allows experimentation and visualization, making it easier to see how motion and curve shape are connected.

---

## Application Overview

The application contains three main sections.

### Curve Transformation Viewer
Users can select a parabola, ellipse, or hyperbola and modify parameters that translate or stretch the curve. The program displays both the original centered curve and the transformed version so changes can be compared directly.

This helps visualize how parameters affect curve position and shape.

![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/67a5fc092f2b421604b197e7792e453d3cb86428/Screenshot%202026-02-10%20215439.png)
![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/6c403499c698412e1b47011184687c72453eafa1/Screenshot%202026-02-10%20215625.png)
![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/6c403499c698412e1b47011184687c72453eafa1/Screenshot%202026-02-10%20215708.png)

---

### Parametric Motion Viewer
This section displays motion along a curve using parametric equations. A point moves along the path while velocity and acceleration vectors are drawn at the current position.

Users can modify curve parameters, motion speed, and vector scaling to see how motion changes in different situations.

This makes it easier to understand how motion behaves along curved paths.

These screenshots are showing an animation

![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/6c403499c698412e1b47011184687c72453eafa1/Screenshot%202026-02-10%20215934.png)
![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/6c403499c698412e1b47011184687c72453eafa1/Screenshot%202026-02-10%20220115.png)

---

### Help Tab
A built-in help section explains how to use the tool and how to interpret what is shown on the screen. It also includes recommended test cases so users can quickly explore meaningful examples. (I didn´t include this on my first SDL and I felt it was lacking this section)
![Alt text](https://github.com/VictorGranado/SDL-2-Curve-Transform-Curves-and-Parametric-Motion/blob/6c403499c698412e1b47011184687c72453eafa1/Screenshot%202026-02-10%20220141.png)

---

## How This Supports Learning

This visualizer supports learning by allowing users to:

- Compare original and transformed curves
- Observe how translation and stretching change equations
- See velocity direction as motion occurs
- Understand how acceleration changes motion
- Connect parametric equations to real motion paths

By interacting with the tool, abstract equations become easier to interpret geometrically.

---

## Installation

This project requires Python 3 and the following libraries:

- numpy
- matplotlib

Install dependencies with:

```bash
pip install numpy matplotlib

---

## Running the Program

After downloading the project, run:

```bash
python sdl2_curved_motion_gui.py
```

The graphical interface will open automatically.

---

## Future Improvements

If more time were available, possible improvements include:

* Displaying tangent lines during motion
* Computing arc length numerically
* Allowing custom parametric equations
* Saving plots as images
* Adding additional curve types

---

## Author Notes

This project was created as part of a self-directed learning assignment to strengthen intuition about curved motion and transformations. Building an interactive visualization proved helpful in connecting equations to geometry and motion.

---

## License

This project is provided for educational use.

```
