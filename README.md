# Developing an agent using NEAT neural networks
This project was about creating an intelligent agent which can navigate on a 2D map, where it would chase a treasure/goal which keeps respawning on new locations.
The agent would then be able to navigate around the map, regardless of size or complexity of its structure.
To do this, we used the NEAT neural network algorithm implemented in python to train a neural network to avoid obstacles while navigating to and finding the goal.


# 1. Map design
<img src="https://github.com/ZpeedX/AI-Projekt/blob/master/images/architecture.png" width="500">
The idea of the map is that the agent, pictured above as the blue square, tries to navigate to the yellow goal while avoiding the black blocks.
This could ultimately be used as a hostile AI, where the agent can receive input values to navigate toward a "sound" or a player, 
which it can then chase until it is reached/aborted.


# 2. Neural network
<img src="https://github.com/ZpeedX/AI-Projekt/blob/master/images/architecture-player.png" width="500">
The topology above was used, where the NEAT algorithm progressively added new nodes and connections to the network as the net was learning. 
By using the input structure of X and Y axis inputs for both which squares are free and which direction the treasure is in, 
the agent could navigate on all possible map structures.


## 2.1 Input structure
The 4 out of 8 inputs given to the neural net indicate which square is free or occupied around it.
The second 4 are to indicate which direction the goal is.
Both either have values 0 or 1, where both inputs follow the following order: left, up, right, down - 
to indicate either if the square is free/occupied or if the treasure is in that direction.

Example: [0,0,1,1,0,0,1,0] means that squares to the left and up are blocked while the squares to the right and down are free [0,0,1,1,...].
The treasure is located directly to the right of the player [..., 0,0,1,0].


# 3. Classes and file descriptions

### **config-feedforward**  
File with configuration values of the neural network.

### **enemy.py**
Enemy object - deprecated class, previously used as an hostile enemy walking around, where the AI would die if it navigated into it.

### **levels.py**
Contains all maps used by the AI for training and testing. 

### **main.py**
Main file used for training and testing.

### **neat-checkpoint-good-0/1**
Trained neural networks which previously performed well. Can be loaded again in the 'main.py' file.

### **pen.py**
Pen that stamps walls and obstacles on the 'Turtle' display. Used to display how the AI is performing visually, irrelevant to the net itself.

### **playable-game.py**
A file where the game is manually playable.

### **player.py**
Class to represent the player in the game.

### **treasure.py**
Class to represent the goal/treasure.

### **winner-genome-playback.py**
File to run the winning genome, which is saved after a training is completed. This can be seen in the 'main.py' file,
but it usually means either reaching 10 000 fitness or gathering reaching enough goals/treasures.

## **winner.pkl**
File which contains binary data of the winning genome, 'used in winner-genome-playback.py' file.

# 4. How to run
To run the files, you will need to install python, NEAT (https://neat-python.readthedocs.io/en/latest/installation.html) 
and any other libraries used (math etc.)

After that, the 'main.py' file can be run to train the neural net. 
Alternatively, maps can be modofied through 'levels.py' or by modifying in the 'main.py' file.
