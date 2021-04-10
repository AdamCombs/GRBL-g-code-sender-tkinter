# Python G-Code Sender for GRBL

## Running the application

1. Activate a virtual environment that contains the packages in `requirements.txt`

2. Navigate to the location of `main.py` and open it.

## Objective 

This is a `Python` app that utilizes Tkinter and the serial library to create a simple user 
interface that allows the user to do the following:

 + Upload and visualize G Code before sending.
 + Select the `COM` port to send the code.
 + Send the uploaded code as serial data.

The `GRBL Gshield v5b` is a stepper motor driver board that attaches to an `Arduino UNO` and 
receives commands via serial data. It powers and moves the stepper motors with an addition 
12 to 30 volt, 2 amp, power supply.

The G-Code commands allow the stepper motors to move in sequence with one another. 
This application made communication with the GRBL easier, 
as the other G-Code senders were subscription software products.

## Application Structure

This structure of this application had a simple two file structure:
1. `main.py` - Starts of the application and creates the UI application frame.
2. `main_frame.py` - Contains all the parts of the UI, and the program logic. 

### Thank you for reading,
### Adam Combs
### Adamcombs1@gmail.com