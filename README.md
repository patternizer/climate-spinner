![image](https://github.com/patternizer/climate-spinner/blob/master/app-snapshot.png)

# climate-spinner

A visual tool for the public and media to use to help understand and communicate statistical climate attribution and the 
probability of occurrence of extreme weather events using digital climate spinner boards. The app is designed as a basis 
for including a range of probabilistic climate impact scales as they are now and how they are expected to change in reponse 
to anthropogenic climate change. Inspired by the Twitter thread: https://twitter.com/richardabetts/status/1280794725679800321
and the BAMS paper by Rachel Dryden & M. Granger Morgan, 'A Simple Strategy to Communicate about Climate Attribution', 
Bull. Amer. Meteor. Soc. (2020), 101(6): E949–E953, doi: https://doi.o10.1175/BAMS-D-19-0174.1.

An online app for testing and development is available at: https://climate-spinners.herokuapp.com/

## Contents

* `app.py` - main script to be run with Python 3.6+
* `climate-spinner.py` - static version for local testing and dev

The first step is to clone the latest  climate-spinner code and step into the check out directory: 

    $ git clone https://github.com/patternizer/climate-spinner.git
    $ cd climate-spinner
    
### Using Standard Python 

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested 
in a conda virtual environment running a 64-bit version of Python 3.6+.

climate-spinner can be run from sources directly, once the following module requirements.txt are resolved.

Run a static version at localhost with:

    $ python climate-spinner.py
	        
## License

The code is distributed under terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).

## Contact information

* [Michael Taylor](https://patternizer.github.io)

