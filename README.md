# Chrysopelea
Python interface for AVL and XFOIL

## Purpose
[AVL](http://web.mit.edu/drela/Public/web/avl/) and [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) are efficient and reliable tools for low-fidelity
analysis of lifting surfaces. Chrysopelea is intended to provide a convenient way to use these tools from Python scripts, which is ideal for sizing and stability
analysis during preliminary design. The object oriented framework makes it feasible to extend this interface to incorporate other data or design considerations.
Finally, it saves the headache of editing AVL files by hand, which is no trivial matter, especially when constructing complex planforms.

Chrysopelea is intended for convenience. It is not currently optimized for execution speed. It is meant to be as intuitive as possible for all users. However,
it may still be much easier to understand if the user has basic proficiency with the command line interface of AVL and XFOIL.

## On the name
Chrysopelea ([Wikipedia](https://en.wikipedia.org/wiki/Chrysopelea)), aka "flying snake" is a genus of snakes that can glide from trees to the ground by extending
their ribs to flatten the cross section of their body. A flying snake seemed to be a suitable namesake for a Python program for analyzing aircraft.

## Capabilities
Currently supports:
- Creation of aircraft configurations employing most features supproted by AVL.
- Creation of 2D wing sections from coordinate files or NACA designations.
- Calculation of 3D, inviscid aerodynamic properties, including stability derivatives, with AVL.
- Total drag estimates combining AVL predictions for induced drag with XFOIL predictions for 2D section drag.
- Moment, trim, and static stability calculations.
- Calculation of derived geometric properties, including aspect ratio and mean aerodynamic chord.
- Calculation of lift and bending moment distributions.
- Geometry and Treffitz plots.
- Reading and writing AVL files. (Reading human-generated files is still a bit unreliable).

## Dependencies
Users must supply their own copies of AVL and XFOIL. They may specify the command or executable file used to invoke AVL and XFOIL by setting the class
attributes `Avl.avl_cmd` and `Section.xfoil_cmd` respectively. Python dependencies are:
- Python 3
- Python libraries:
  - matplotlib
  - pandas

## Installation
No installation is necessary. To verify that Chrysopelea functions properly, navigate to the directory `tests` and execute `python3 *.py`. You should see
a bunch of aerodynamic data and no exceptions.

## Documentation
Documentation is in progress. For now, the file `tests/test_avl.py` demonstrates most of the important features. `tests/test_section.py` demonstrates how
`Section` can be used as a stand-alone XFOIL interface.

## Contributions and issues
Feedback or contributions regarding problems or new features are welcome. Please contact Micaiah at micaiah@smithpierce.net or micaiah@gatech.edu.
