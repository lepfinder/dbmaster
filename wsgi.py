#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#########################################################################
# File Name: wsgi.py
# Author: xiyang
# mail: sdlgxxy@gmail.com
# Created Time: 五  3/31 08:21:42 2017
########################################################################

from dbmaster import create_app


application = create_app('config.cfg')

if __name__ == '__main__':
    application.run()