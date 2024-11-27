# K.I.no 🎥

### So what is this about?

Long story short, this is a project i'm doing just for fun, trying to predict the audience turnout for our campus cinema!

### _But why?_
To be honest, this project and subsequently this repository are more for learning purposes than anything else. Best case, this project will end with a model that can reliably predict the attendance of a movie.
Worst case, i learned something. I'm hoping for something in between lol.

### How will it work?
I'm not set on a special Machine Learning Algorithm yet, but there are definetly some i want to try out!
- Linear Regression
- Multiple Regression
- Support Vector Machine 
- Some kind of Pipeline (Random Forest +...+ etc.)
- Gradient Boosting
- XGBoost
- Some kind of Neural Network (?)

At the end i will probably settle for some kind of Pipeline, but who knows.


### Big shoutout to the Cine-Asta Trier!
They provided the data i will use to train the model! The model will also only work for the cinema who provided the data, which in this case is them ✨

https://www.asta-trier.de/cineasta/

## Setup Guide

This guide is for starting `K.I.no` app.

> You may also use the Dockerfile to run the app.

1. Clone this repository.

```bash
git clone https://github.com/Tisinti/K.I.no.git
```

2. Install dependencies inluding the correct python version using [rye](https://rye.astral.sh/).

```bash
rye sync
```

3.  Apply your virtual enviroment and start the app

```bash
source .venv/bin/activate
python main.py
```





