#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:40:20 2022

@author: pritamkhose

pip install sqlalchemy

https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_selecting_rows.htm

"""
import sqlalchemy
print(sqlalchemy.__version__)

from sqlalchemy import create_engine
# engine = create_engine("mysql://user:pwd@localhost/college",echo = True)
# print(engine)

from sqlalchemy import MetaData,create_engine
meta = MetaData()
print(meta)