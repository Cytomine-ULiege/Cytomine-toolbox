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

import os

from os.path import isfile
from time import sleep

from cytomine.cytomine import Cytomine
from cytomine.models.image import ImageInstanceCollection, AbstractImage
from cytomine.models.imagegroup import ImageGroup, ImageSequence, ImageSequenceCollection, ImageGroupHDF5
from cytomine.models.storage import UploadedFile

__author__ = "Rubens Ulysse <urubens@uliege.be>"
__contributors__ = ["Marée Raphaël <raphael.maree@uliege.be>"]
__copyright__ = "Copyright 2010-2018 University of Liège, Belgium, http://www.cytomine.be/"

upload = "demo-upload.cytomine.be"
id_storage = 0
project_id = 0

priv = ""
publ = ""
c = Cytomine.connect('demo.cytomine.be', publ, priv)

dir_path = "Rompp-ProteomeXChange2010/ionimages"
onlyfiles = [f for f in os.listdir(dir_path) if isfile(os.path.join(dir_path, f)) and f[-4:] == ".png"]
onlyfiles.sort()
print(onlyfiles)

# Upload files
zstack = {}
t = 0
for file_path in onlyfiles:
    print("Upload file {}".format(file_path))
    p = os.path.join(dir_path, file_path)
    uf = c.upload_image(upload, p, id_storage, project_id)
    print(uf)
    zstack[uf.id] = t
    t += 1

n_imgs = -1
img_insts = None
while n_imgs != len(onlyfiles):
    img_insts = ImageInstanceCollection(filters={"project": project_id}).fetch()
    n_imgs = len(img_insts)
    sleep(3)

# Make image group
group = ImageGroup("RAW", project_id).save()
print(group)

for img_inst in img_insts:
    ai = AbstractImage().fetch(img_inst.baseImage)
    uf2 = UploadedFile().populate(c.get("uploadedfile/image/{}.json".format(ai.id)))
    se = ImageSequence(group.id, img_inst.id, zstack[uf2.id], None, 0, 0).save()
    print(se)

n_seqs = -1
while n_seqs != n_imgs:
    seq = ImageSequenceCollection(filters={"imagegroup": group.id}).fetch()
    n_seqs = len(seq)
    print(n_seqs)
    print(n_imgs)
    sleep(3)

# Make HDF5 image group (i.e. launch the conversion to HDF5 from set of images)
groupHDF5 = ImageGroupHDF5(group.id).save()
print(groupHDF5)
