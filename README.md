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

    $ cd cost_per_view
    $ python cpv.py
    

**Output**

    {
      "cpv": {
        "rotation": {
          "Prime": 3.45,
          "Afternoon": 4.64,
          "Morning": 2.59
        },
        "rotation_by_creative_by_day": {
          "Morning - TEST001H - 2016-02-02": 3.5,
          "Afternoon - TEST002H - 2016-01-02": 5.29,
          "Prime - TEST001H - 2016-01-02": 3.64,
          "Prime - TEST002H - 2016-02-02": 2.33,
          "Morning - TEST001H - 2016-01-02": 1.72,
          "Afternoon - TEST001H - 2016-01-02": 3.64,
          "Prime - TEST002H - 2016-01-02": 5.29
        },
        "creative": {
          "TEST002H": 3.91,
          "TEST001H": 2.95
        },
        "rotation_by_day": {
          "Morning - 2016-01-02": 1.72,
          "Prime - 2016-01-02": 4.64,
          "Afternoon - 2016-01-02": 4.64,
          "Prime - 2016-02-02": 2.33,
          "Morning - 2016-02-02": 3.5
        },
        "day": {
          "2016-02-02": 2.8,
          "2016-01-02": 3.85
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

10) Possibly naively assumed that CPV is spend / views.



Thank you!
<br/>
Kris
