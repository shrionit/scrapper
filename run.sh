#!/bin/bash

uvicorn server:api --host 0.0.0.0 --port 8000 --reload
