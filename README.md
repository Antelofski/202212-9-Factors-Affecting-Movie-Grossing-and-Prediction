# EECS6893_Final_Project
Project ID: 202212-9

Project Name: Factors Affecting Movie Grossing and Prediction

Group Members: Hanlun Wang (hw2839), Jingtian Zhang (jz3500), Weirui Peng (wp2297)

This repository contains:

1. [__init__.py](flaskr/__init__.py) backend file writen in Python based on Flask
2. [http files](flaskr/templates) frontend files based on Jinja template
3. [css file](flaskr/static/css) define the sytle
4. [js file](flaskr/static/js) define the javascript
5. [requirements.txt](requirements.txt) for packages needed
6. [models](/models/) models we trained
7. [crawl.py](crawl.py) craws the data on the web page
8. [combine.py](combine.py) aggregates and pre-processes the collected data
9. [prediction.ipynb](prediction.ipynb) train models and do prediction

## Table of Contents

- [EECS6893_Final_Project](#EECS6893_Final_Project)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
  - [Contributors](#contributors)
  
## Background
This is a system to predict the box office of a movie. It contains data crawling, data visualization, machine learning model training, web backend, and web frontend.

The user can use [crawl.py](crawl.py) to crawl the data on the web page and [combine.py](combine.py) to aggregate and pre-process the collected data. The processed data is stored in the [dataset](/dataset/) folder.

The user can use [predict.py](prediction.ipynb) to train and predict the gross. The program will read data from dataset file and automatically split the data into training and predicting sets. Several models are choosen to do the training. All models' training, predicting, and error are shown in the jupyter notebook file. 

[flaskr](/flaskr/) file contains the website backend and frontend. Users can see a brief introduction of our project on the website. Users can also input their own data to try the prediction. Their input data will be feeded into the model to do the prediction and the predicted grossing will be shown on the website. 

## Install
This project uses Python3 and is based on Flask. Use
```sh
$ pip install -r requirements.txt
```
to install required packages.

## Usage
Go to the flaskr file and run
```sh
$ python3 __init__.py
```

## Contributors
[Hanlun Wang](https://github.com/HanlunWang),
[Jingtian Zhang](https://github.com/Iris1e27),
[Weirui Peng](https://github.com/Antelofski)