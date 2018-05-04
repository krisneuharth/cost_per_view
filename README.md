### Cost Per View

##### Submitted by Kris Neuharth - 5/4/2018

**Installation**

This application requires Python 3, here I assume OSX for simplicity but this is easy to verify on other operating systems:

    $ brew install python3
    $ python --version


Next clone or unzip the project:
    
    $ git clone git@github.com:krisneuharth/cost_per_view.git
 
Install dependencies and set path
    
    $ pip install -r requirements.txt
    $ python setup.py develop


**Running the application**

    $ cd cpv
    $ python cpv.py
    

**Output**

    {
      "cpv": {
        "rotation_by_creative_by_day": {
          "Prime - TEST002H - 2016-01-02": 0.19,
          "Afternoon - TEST002H - 2016-01-02": 0.19,
          "Afternoon - TEST001H - 2016-01-02": 0.28,
          "Prime - TEST001H - 2016-01-02": 0.28,
          "Prime - TEST002H - 2016-02-02": 0.43,
          "Morning - TEST001H - 2016-01-02": 0.58,
          "Morning - TEST001H - 2016-02-02": 0.29
        },
        "creative": {
          "TEST002H": 0.26,
          "TEST001H": 0.34
        },
        "day": {
          "2016-01-02": 0.26,
          "2016-02-02": 0.36
        },
        "rotation_by_day": {
          "Prime - 2016-02-02": 0.43,
          "Morning - 2016-01-02": 0.58,
          "Morning - 2016-02-02": 0.29,
          "Afternoon - 2016-01-02": 0.22,
          "Prime - 2016-01-02": 0.22
        },
        "rotation": {
          "Morning": 0.39,
          "Afternoon": 0.22,
          "Prime": 0.29
        }
      }
    }

**Running the tests**

    $ nosetests

**Assumptions**

0) I assumed Python would be ok for this exercise. I didn't use any of the data science tools but that may have made it easier.

1) I assumed that timezones didn't matter since it wasn't specified.

2) There are overlapping times for the rotations so I treated them as two separate spots for purposes of calculations.     

3) I treated any unspecified rotation as "Other". This wasn't present in the data set but with a larger one it would show up.

4) I assumed a console print out would be sufficient for output.

5) I calculated a few other dimensions along the way just because.

6) I structured this app so that it would be fairly simple to make it run in parallel
with multiprocessing.

7) I assumed that rounding to the nearest hundredth would be sufficient but this is easily changed.

8) I assumed a pretty clean data set and did not do much error handling.

9) I assumed larger data sets so I built this with memory use in mind, hence the classes with slots.




Thank you!
<br/>
Kris
