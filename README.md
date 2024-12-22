# DSA Final Project - Maze Game

**Subject Code:** CSC200 - Data Structures and Algorithms  
**Instructor:** Nazeef Ul Haq 

## Table of Contents
1. **Introduction**
2. **Key Features**
3. **Data Structures and Algorithms Used**
4. **Technologies Used**
5. **Code Structure**
6. **Folder Structuring**
7. **How to Run the Project**
8. **Challenges and Solutions**
9. **Contributions**
10. **Conclusion**

---

## Introduction
The Maze Game is a puzzle-solving game where players navigate through mazes of increasing complexity. The game leverages various data structures and algorithms to ensure dynamic gameplay. Players can explore the maze while only revealing visited nodes, enhancing the challenge with a "darkness" effect on unexplored areas.

---

## Key Features
- **Maze Generation:** Each maze is dynamically generated using graphs, ensuring unique gameplay for every level.
- **DFS Pathfinding:** Depth-First Search ensures the maze always has a valid path from the start to the end.
- **Levels of Complexity:** The mazes increase in size and complexity as the player progresses.
- **Darkness Effect:** Unvisited nodes remain hidden, and only explored areas are illuminated.
- **Player Movement:** Players can navigate through the maze step by step until they reach the goal.
- **Interactive Visuals:** The game offers an intuitive interface for interacting with the maze.

---

## Data Structures and Algorithms Used
### Graph:
- Used to represent the maze structure, where each node is a maze cell and edges represent valid paths.
- **Time Complexity:** O(V + E) for graph traversal.
- **Space Complexity:** O(V + E) for adjacency list representation.

### Stack:
- Implemented for DFS to ensure a valid path in maze generation.
- **Time Complexity:** O(1) for push/pop operations.

### Arrays:
- Used to store the maze layout, player positions, and visited cells.
- **Time Complexity:** O(1) for indexing.

### DFS:
- Ensures a valid path exists between the start and end nodes.
- **Time Complexity:** O(V + E).

### Dynamic Maze Illumination:
- Tracks visited nodes to control the visibility of the maze.
- **Space Complexity:** O(V) for the visited array.

---

## Technologies Used
- **Python:** Game logic and data structures.
- **Pygame:** For implementing the interactive graphical interface.

---

## Code Structure
### Key Files:
- `bklevel.py`: Handle all the levels.
- `bk.py`: Contain all the backend of the game.
- `bkmaze.py`: The main class for game logic and UI implementaiton.

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
