# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2018. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "Rubens Ulysse <urubens@uliege.be>"

import os
import matplotlib.pyplot as plt

home = '/'
dir = os.path.join(home, "Rompp-ProteomeXChange2010/ionimages/")
for file in os.listdir(dir):
    if file.endswith(".png"):
        f = os.path.join(dir, file)
        print(f)

        im = plt.imread(f)
        norm = plt.Normalize(vmin=im.min(), vmax=im.max())
        im = plt.cm.plasma(norm(im))
        plt.imsave("{}_plasma_norm.png".format(f[:-4]), im)
