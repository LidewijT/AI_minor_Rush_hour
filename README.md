# Rush Hour


## The game
Rush Hour is a game in which the goal is to get the red car out as fast aspossible, minimising its number of moves. Cars are not allowed to collide and can only will only move one tile at the time in their orientation. This codebase can solve boards with sizes 6x6, 9x9, and 12x12 with different algorithms. These include breadth-first search, depth-first search, depth-limited search, depth-first search with hill climber, random car movements algorithms. Furthermore, there is a heuristic to prioritise moving the red car in addition to the random algorithm, and a heuristic to sort the children states in the depth-first search according to their priority values.

## Requirements
This codebase is completely written in Python 3.9.13. The requisite packages can be found in the file 'requirements.txt' to assure the succesfullness of running the program. These can be installed using pip or conde with the following command.

```
pip install -r requirements.txt
```

or

```
conda install --file requirements.txt
```

This will guarantee all packages will be installed with the right version.


## Usage
To solve a gameboard or visualise a solution, the program can be runned by the following command in the terminal:

```
python main.py
```

Then, the terminal will ask you for the input what board the user desires to solve. Subsequently, the user will be guided through different choices on how to solve the input gameboard, including which algorithms, their corresponding parameters and a name for the output file.

If running an experiment is desired, the following command can be runned in the terminal:

```
python m code.experiments.name_experiment
```

## Structure
Here, you can find a list with the most important folders and files of this projects, including its locations.

- **/code**: folder which includes all of the code
    - **/code/algorithms**: folder which includes all of the code for algorithms
    - **/code/classes**: folder which includes all classes
    - **/code/experiments**: folder which includes the code for all experiments
    - **/code/helpers**: folder which includes a file to prompt the user.
    - **/code/visualisation**: folder which includes the code for the visualisation
- **/data**: folder which contains all input and output files
    - **/data/experiments**: folder which contains the output of the experiments
    - **/data/gameboards**: folder which contains all gameboard files (input)
    - **/data/graphs**: folder which contains all graph images
    - **/data/solutions**: folder which contains all solution files of the runned programs (output)

## Authors
- Judith Atsma
- Michiel Beltman
- Lidewij Tijhuis
