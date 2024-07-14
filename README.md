# Ultimate Tic Tac Toe AI

## Abstract

### Game Setup
1. The game unfolds on a 3x3 grid comprising nine smaller grids, arranged in a 3x3 layout.
2. Each small grid operates like a standard Tic-Tac-Toe, with players placing their marks (X or O) until one emerges victorious or the grid reaches capacity.
3. Victory in Ultimate Tic-Tac-Toe is attained by dominating the larger grid, achieved by securing three small grids in a row, either horizontally, vertically, or diagonally.

### Gameplay
1. Players alternate placing their marks in any allowed and vacant square of the large grid.
2. The chosen square dictates the small grid where the opponent must make their subsequent move.
3. For instance, if Player A marks the top-right cell of a small grid, Player B must respond in kind in the corresponding grid of the larger layout.
4. When a player captures a region, their mark is displayed in the corresponding cell of the large grid.
5. Should a player's move lead to an already won or full small grid, the opponent gains the freedom to play in any vacant cell of the large grid - this is known as a “free go.”
6. The game progresses until one player secures victory by securing three small grids in a row or until the large grid reaches capacity, in which case the player with most captured regions wins.
7. If the larger board reaches capacity and both players have the same number of captured regions, the game is tied.

### Objective of the AI System
The objective was to develop an AI system adept at engaging novice players in Ultimate Tic-Tac-Toe, offering a stimulating yet enjoyable experience. Leveraging adversarial search algorithms, particularly the minimax algorithm bolstered by alpha-beta pruning, the AI strives for efficient decision-making while preserving strategic depth. Additional enhancements, including region and position heuristics, boost the AI's performance.

## AI System Description

### Minimax Algorithm
The AI system's foundation lies in the minimax algorithm, implemented as a recursive function with a depth limit in case terminal states (win, lose, or tie) are not reached, which is common throughout most of the game. When the depth limit is reached, the resulting board configuration is passed to an evaluation function that scores the board based on different heuristic functions. A positive score benefits the computer, the maximizing player, while a negative score benefits the human player. This evaluation function is key to decision-making through the simulation of alternate game states.

### AI Agent Versions
Six versions of the AI agent were designed for the experiment. Each subsequent agent has additional, more advanced features implemented:

1. **Random Agent (R)**: Randomly selects from the legal moves, serving as the control group.
2. **Minimax Agent (M)**: Uses raw minimax with a depth limit cut off at 3. No heuristics were used.
3. **Alpha Beta Pruning Agent (AB)**: Incorporates alpha-beta pruning to the minimax algorithm, achieving a depth of 5 without any heuristics.
4. **Captured Regions Heuristic Agent (CR)**: Introduces a heuristic that counts the number of smaller regions captured by a player within the larger layout.
5. **Positional Advantage Heuristic Agent (PA)**: Adds a heuristic that counts the number of opportunities a board configuration gives a player. Opportunities refer to when a player has two marks and only needs one more to capture a region.
6. **Free Goes Heuristic Agent (FG)**: Includes a heuristic for the number of free goes offered to the opponent. This agent builds upon all previous features.

### Performance Optimization
To mitigate the computational complexity inherent in Ultimate Tic-Tac-Toe, alpha-beta pruning was integrated, significantly streamlining the evaluation process. Additionally, the higher AI versions incorporate region and position heuristics to refine decision-making, prioritizing moves based on strategic significance. These features collectively enhance performance in terms of move time and depth of exploration, ensuring a challenging yet balanced gaming experience.

## Experimental Results

### Performance Evaluation
The two primary measures used to evaluate the AI agents were win rate and response time, with an emphasis on win rate. Fifty games were played with each version of the AI by novice players, and the average response time per move and the number of wins were recorded.

#### Win Ratios
The results showed that the fifth AI agent, which included the positional advantage and captured regions heuristics, was optimal with an 82% win ratio. Introducing additional features like alpha-beta pruning and heuristics increased the AI's difficulty level, with the exception of the free goes heuristic.

#### Response Times
Regarding response times, the random agent was the fastest since it implemented no search techniques but was easy to beat. All subsequent agents based on the minimax algorithm had an exponential time complexity of O(b^d). The raw minimax agent, with a max depth of 3, was the slowest at 6.7 seconds, while alpha-beta pruning reduced response time to 3.3 seconds by cutting down the number of nodes searched by half. The three heuristic agents involved additional computations for each heuristic, explaining the linear increase in response time with each additional heuristic.

### Discussion and Analysis
An unexpected revelation was the superior performance of the positional advantage heuristic in refining the AI's gameplay compared to the agent that included the free goes heuristic. Despite initial expectations favoring the integration of all three heuristics, it became evident that the position and captured regions heuristics alone sufficed to achieve optimal results. This underscores the importance of tailoring specific aspects of the AI system to maximize performance effectively.

## Limitations and Future Work
A notable challenge encountered was the absence of established heuristic functions tailored for Ultimate Tic Tac Toe. Developing accurate heuristics proved to be a significant hurdle. Future research could explore the integration of advanced methodologies such as Monte Carlo Simulation to enhance the AI's gameplay capabilities. Ongoing refinement of heuristic functions tailored specifically for Ultimate Tic Tac Toe could unlock additional performance enhancements.

## Conclusion
The investigation revealed that the AI system's optimal performance in Ultimate Tic Tac Toe was achieved when equipped with the positional advantage and captured regions heuristics. Despite the high branching factor and inability to reach terminal states in a minimax search even with alpha-beta pruning, the introduction of various heuristic evaluation functions was indispensable. The positional advantage heuristic proved to be the most significant, leading to the highest win ratio of 82%. This project resulted in an intuitive console-based Ultimate Tic Tac Toe game written in Python, easy to learn and exciting for novice players. Future research could explore methods like Monte Carlo simulation for creating more powerful AI opponents suitable for advanced players.

## References
1. “Ultimate tic-tac-toe,” The Game Gal, Sep. 2018. https://www.thegamegal.com/2018/09/01/ultimate-tic-tac-toe/ (accessed Apr. 7, 2024).
2. “The Minimax Algorithm 101,” Japlslounge.com, 2020. https://japlslounge.com/posts/articles/Minimax_Blog/1.htm (accessed Apr. 14, 2024).
3. Gila, O., “Ultimate tic-tac-toe,” Wikipedia, Oct. 18, 2023. https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe (accessed Apr. 10, 2024).