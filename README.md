### Cost Per View

##### Submitted by Kris Neuharth - 4/3/2018

**Installation**

This application requires Python 3, here I assume OSX for simplicity but this is easy to verify on other operating systems:

    $ brew install python3
    $ python --version


Next clone or unzip the project and run:
    
    $ pip install -r requirements.txt
    $ python setup.py develop


**Running**

    $ cd cpv
    $ python cpv.py
    

**Output**

    ```json
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

**Assumptions**
1) 


Thank you!
