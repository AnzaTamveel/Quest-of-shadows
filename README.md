# DSA Final Project - Maze Game

**Subject Code:** CSC200 - Data Structures and Algorithms  
**Instructor:** Nazeef Ul Haq

---

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Data Structures and Algorithms Used](#data-structures-and-algorithms-used)
4. [Technologies Used](#technologies-used)
5. [Code Structure](#code-structure)
6. [Folder Structure](#folder-structure)
7. [How to Run the Project](#how-to-run-the-project)
8. [Challenges and Solutions](#challenges-and-solutions)
9. [Contributions](#contributions)
10. [Conclusion](#conclusion)

---

## Introduction

The **Maze Game** is an exciting puzzle-solving game where players navigate through dynamically generated mazes of increasing difficulty. The game incorporates key data structures and algorithms to ensure challenging and engaging gameplay. Unexplored areas of the maze remain hidden with a "darkness" effect, adding an element of suspense as the player uncovers the path to the goal.

---

## Key Features

- **Dynamic Maze Generation:** Each maze is generated using graph structures, providing unique experiences every time a new level is played.
- **Depth-First Search (DFS) Pathfinding:** Ensures there is always a valid path from the starting point to the destination.
- **Increasing Complexity:** As players progress, the mazes grow in size and complexity, providing an escalating challenge.
- **Darkness Effect:** Only explored nodes are illuminated, adding an extra layer of challenge to the navigation process.
- **Step-by-Step Player Movement:** The player can move through the maze one step at a time until the goal is reached.
- **Interactive Visual Interface:** The game features a user-friendly graphical interface developed with Pygame, allowing players to interact with the maze in real-time.

---

## Data Structures and Algorithms Used

### **Graph**
- **Purpose:** Represents the maze where each node is a maze cell, and edges indicate valid paths.
- **Time Complexity:** O(V + E) for traversal.
- **Space Complexity:** O(V + E) for adjacency list representation.

### **Stack**
- **Purpose:** Used in DFS for maintaining the path and ensuring the maze has a valid solution.
- **Time Complexity:** O(1) for push/pop operations.

### **Arrays**
- **Purpose:** Stores maze layout, player positions, and visited cells for efficient tracking.
- **Time Complexity:** O(1) for indexing.

### **DFS (Depth-First Search)**
- **Purpose:** Guarantees that the maze has a valid path from start to end by exploring nodes systematically.
- **Time Complexity:** O(V + E).

### **Dynamic Maze Illumination**
- **Purpose:** Keeps track of visited nodes to dynamically adjust the visibility of the maze.
- **Space Complexity:** O(V) for the visited array.

---

## Technologies Used

- **Python:** Core programming language for implementing game logic and data structures.
- **Pygame:** A library used to develop the graphical user interface (GUI) for the interactive maze game.

---

## Code Structure

### **Key Files**
- `bklevel.py`: Handles the level management and progression.
- `bk.py`: Contains the backend game logic, including data structures for maze generation and traversal.
- `bkmaze.py`: The main class that implements the game logic and user interface.

---

## Folder Structure

```plaintext
Maze-Game/
│
├── bklevel.py           # Level management
├── bk.py                # Core game logic
├── bkmaze.py            # Game logic & UI implementation
└── assets/              # Game assets (e.g., images, sounds)

---

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/AnzaTamveel/Quest-of-Shadows
   ```
2. Install the required dependencies:
   - Python 3.x
   - Pygame: Install via pip:
     ```bash
     pip install pygame
     ```
3. Navigate to the project directory:
   ```bash
   cd Project
   ```
4. Run the game:
   ```bash
   python bklevel.py
   ```

---

## Challenges and Solutions
- **Challenge:** Ensuring a valid path in every maze.
  **Solution:** Used Depth-First Search to guarantee connectivity between the start and end points.
- **Challenge:** Handling large mazes efficiently.
  **Solution:** Optimized data structures like arrays and adjacency lists for fast lookups.
- **Challenge:** Dynamic darkness visualization.
  **Solution:** Implemented a visited tracker to dynamically illuminate explored areas.

---

## Contributions
- **Anza Tamveel**
- **Amna Atiq**
- **Zainab Batool**

---

## Conclusion
This project allowed us to deeply explore the practical implementation of data structures and algorithms, showcasing how these concepts can powerfully solve real-world problems like maze generation and navigation.

---
