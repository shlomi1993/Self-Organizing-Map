# Self-Organizing-Map
 
Computational Biology - Assignment 3
Solved by Shlomi Ben-Shushan (ID: 311408264).

## Description
In this ReadMe, I will describe my implementation of a Self-Oprganized-Map algorithm and I will explain how to use the wrapping app.

## Requirements
There are no unique requirements to run the executable file SOM.exe.  
But if there is a need to run the source code of the program, then the following requirements must be met first:
1. Please make sure that Python 3 is installed in your machine. The program was written using Python version 3.10 but was also tested on Python 3.8.
2. Use pip, or any other Python package manager, to install the packages: 'ntpath', 'tkinter', 'prettytable', 'matplotlib', and 'numpy'.

## Instructions
### Starting the program
If you are using the executable, just double click on it (or execute it via terminal) and the program will start.
If you want to run the source code, make sure the requirements above met. Then, navigate to the programs's main directory (where main.py file is located), and run the command 'python main.py'.

### Using the program
After the program starts, the following window will appear:  

![image](https://user-images.githubusercontent.com/72878018/173429746-fe0a90e6-3973-40e5-a85d-eb28ddd2aa29.png)  
  
In this window, you can:  
1. Load an input CSV file (required).
2. Change the number of epochs to run (default is 10).
3.  Choose the error measurement method (default is Quantization Error).
4.   Determine whether the program will show a figure (default is True).

Important Notes:
1. Make sure the input file is valid, i.e., in the form of the attached file "Elec_24.csv".
2. Selecting a high number of epochs may make the program look frozen. Patience, the computation is being done in the background and the output will be displayed when it is finished.

### Output
The program output is obtained in three forms:
1. An hexagonal diagram will be displayed in the main canvas on the right.
2. A mapping table between the municipality and the representative cell (neuron) will be displayed in the console on the left.
3. A figure describing the errors will be displayed in a new window (if True is set in the settings).

## Screenshots
Below is an example of the program output:  
![image](https://user-images.githubusercontent.com/72878018/173408379-70e5bfd5-f04b-4c99-9ad0-e3cd9090d07d.png)  

