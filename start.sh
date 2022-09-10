#!/bin/bash

pip install gunicorn
gunicorn app:server
