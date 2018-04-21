#!/bin/bash
export FLASK_APP=todo/todo.py
flask initdb
flask run
