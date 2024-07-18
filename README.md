# MS-Sudoku-Solver

## Introduction

This is a python based program that interacts with the desktop version of Microsoft Sudoku. Thanks to the constraints of the problem, i.e. a very predictable number format, it uses perhaps the simplest form of machine learning to predict the numbers.

## Algorithm

### Window

The program starts out by grabbing the window on the desktop, bringing it to the foreground, focusing on it, resizing it, and placing the top left corner at 0, 0. All to create a very standard environment from which to work on.

### Grid

Once the window is resized, it grabs an image of the window. Since we only need the sudoku grid, it narrows down to around the grid, and then uses numpy logic to get the first and last rows in the x and y coordinates. Then reduces the grid to everything on the inside plus a one pixel edge. From here it goes through the internal grid lines to reduce them to one pixel as well.

### Numbers

When the structure is completed, the algorithm grabs the row and column boundaries of each cell. With these, it loops through the boundaries, grabbing each cell and putting it into a numpy array. Then creating a box whose edges are bound to the sides of the number. It then takes these bound boxes and then stretches them to a standard 30x30 using `scikit.transform.resize()`.

### The simplest ML alrogithm

As mentioned, thanks to the constraints of the problem, the numbers are very standardized. They are not, however, the same across each cell. One 5 may not be the same as another 5, but only very slightly. Hence, you can't just compare them directly. Instead, I tried to find some of the best looking numbers, grabbed their standardized data and just threw them into CSVs. At the start of the program, we can load those in and grab them as we need them. To get the correct number, we can use numpy's boolean logic and compare each array (the number on the grid, and the saved number) directly by using `grid == saved` and then taking the mean of this value (`(grid == saved).mean()`). This will give us a percentage of how well the number matches the saved number. Do this for all 9 digits and then take the one with the greatest mean and we have our number!

### Solving the sudoku

Since we now have the numbers, we can throw them in an nxn numpy array of integers and set the empty cells to 0. We can then use a backtracking algorithm to solve the sudoku quickly. At this point it was very late and I'd spent most of the day on it, so I googled a solution and used [Geeksforgeeks](https://www.geeksforgeeks.org/sudoku-backtracking-7/). I did, however, clean up their version by numpy-ifying (numpifying?) it since I was already working with this powerful library.

### Interacting with the game

Now we have the cell locations and their correct values. We just have to interact with the game to click on the cell and input the number. This was done with `pyautogui`. Since the screen has been set to a standardized point, we just have to get the amount of `x, y` offset that we used to get to the top left point of the grid when we setup the grid. Using this we can get the offset, and use the midpoint of the row and column boundaries for each cell to get the point at which we need to click. Using `pyautogui.moveTo(x, y)` we move the mouse to that point. Then `pyautogui.click()` to click. Then `pyautogui.typewrite(value as string)` to type the desired number for the cell. Do this for every empty cell and we have a solved game.



# Dependencies

The dependencies for this are:

- `numpy`
- `skimage`
- `matplotlib` - installing this should install `numpy` as well
- `win32gui`
- `Pillow`
- `pynput`
- `keyboard`
- `pyautogui`

# Variables

There is a delay variable in `main.py` that will need to be messed around with. It is the delay in seconds that is set when switching to the game window. The reason for this is that when you click off the window and click back on, Microsoft for some reason decides to reload the whole screen. This loading depends on your Internet connect as well. You will need to experiment around with it. If it is too slow, the program will grab the screen before it is meant to and throw an error and crash.

There is another delay that is for the time between click and typing when solving the game. I believe there is a minimum that it will actually go. I tried seeing how fast it will go and set it to about 10 ms, but it was definitely not moving anywhere near that. This could be library or system dependent. I do not know as it was not important to me.

Once setup, run the program with the game launched. I set a `keyboard.wait()` event at the beginning. This was to allow you to manually switch over to a new board before executing a new solve. You can delete this whole line and run the program manually if you wish. Don't forget to delete the `while(True)` as well or it will just try to solve it endlessly and crash.

# Game setup

The game needs to have a few specific settings set for this to work properly.

1. In the options menu, `Update Notes` and `Show All Notes` need to be switched to off.
2. The theme needs to be set to `Black and White`.

# Instructions

In order to start the program, you must already be in the puzzle you wish to solve. Go to `Classic`, then select your difficulty. Once the puzzle fully loads, run the script.

The ad skip functionality is there. It's not perfect and will crash on certain ads. They apparently do not have a uniform format to how they are laid out.

# Use cases

Currently the program is only setup for use in `Classic` mode. It will solve classic daily challenges, but it will not solve irregular or ice puzzles.
