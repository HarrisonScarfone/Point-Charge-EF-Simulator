# Point Charge Electric Field Simulator

Standalone electric field simulator for point charges written in Python 3.8.2.  Uses `pysimplegui` for the interface.

## Field Calculation

Draws a graph section of `600x600`.  User can then place point charges at specified points based on a cartesian coordinate system with the very center of the graph being the point `(0,0)`.

When the field vectors need to be drawn, the graph is sectioned into squares dependant on the amount of vectors to be drawn, then the following steps are taken.

1. Sum of forces from all point charges is taken at the center of that section using cylindrical coordinates that are converted to cartesian components for easy summing.
2. Unit vector of the resultant vector is taken.
3. Color of the vector is determined by a net positive or net negative force at the point.
4. Using the unit vector and color, vector of specified length is then drawn through the center of that box.

## Adding a Charge

Enter the X and Y coordinates of the charge to add.  Center of the white field pane is `(0,0)`.  Charge is in nC and can accept any valid `int`.

## Clearing the Screen and Showing Vectors

### Clear All Charges

Removes all charge objects from memory and your simulation.

### Clear All Vectors

Removes all vectors from memory and your simulation.

### Showing Vectors

Vectors are on by default.  If they are cleared, you can redraw them with `Show Vectors` using the current settings in memory.

## Calculating Force at a Particular Point

The net field effect can be calculated by providing a cartesian pair.  Resultant vector is given in component form.

## Export Data

Creates 2 CSV files in the working directory. 
* `electric_field.csv` contains `Object ID`, `X Position`, `Y Position`, `Charge (C)`
* `force_vectors.csv` contains `Object ID`, `Line Color`, `X Position`, `Y Position`, `X Force Vector Comp.`, `Y Force Vector Comp.` , `Field Strength`

## Updating Number of Vectors and Vector Length

Delete all current force vectors and redraw with new parameters.  For vector length, any non-zero `int` is a valid entry.  The default value is `8`.

For vectors, perfect squares work best but any `int` number is a valid entry.

> :warning: **There is no upper bound on the number of force vectors you can ask the program to draw**: This can lead to large (or catastrophic) memory usage and long draw/delete times.

## Quiting the Program

Press the `Exit` button, close the window or if instance is generated from `terminal` or `cmd`, end the process.