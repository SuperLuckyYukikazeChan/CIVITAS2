from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import redirect,render,HttpResponse
from assist import *
from django.contrib.sessions.models import Session
from django.contrib import auth
from MaterialModel.models import *
from UserModel.models import *
from RecipesModel.models import *
from WorkModel.models import *
import random
import json
import datetime