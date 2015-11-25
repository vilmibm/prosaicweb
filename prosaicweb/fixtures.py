# prosaicweb
# Copyright (C) 2015  nathaniel smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from os import path

import cfg
from models import Template, User, Source

templates = [
    {'name':'sonnet',
     'lines': [
         {'rhyme':'A', 'syllables': 10},
         {'rhyme':'B', 'syllables': 12},
         {'rhyme':'A', 'syllables': 11},
         {'rhyme':'B', 'syllables': 13},
         {'blank': True},
         {'rhyme':'C', 'syllables': 10},
         {'rhyme':'D', 'syllables': 12},
         {'rhyme':'C', 'syllables': 11},
         {'rhyme':'D', 'syllables': 13},
         {'blank': True},
         {'rhyme':'E', 'syllables': 10},
         {'rhyme':'F', 'syllables': 12},
         {'rhyme':'E', 'syllables': 11},
         {'rhyme':'F', 'syllables': 13},
         {'blank':True},
         {'rhyme':'G', 'syllables': 12},
         {'rhyme':'G', 'syllables': 10},]},

    {'name': 'haiku',
     'lines': [
         {'syllables': 5},
         {'syllables': 7},
         {'syllables': 5},]},

    {'name':'morbid',
     'lines': [
         {'keyword':'dying'},
         {'fuzzy': 'death'},
         {'keyword': 'dark'},
         {'fuzzy': 'pitch'},
         {'blank': True},
         {'keyword': 'dying'},
         {'keyword': 'end'}
     ]}
]

source_filenames = ['paradise_lost.txt',
                    'call_of_cthulhu.txt',
                    'odyssey_into_prose.txt',
                    'leaves_of_grass.txt',
                    'hanging_stranger.txt',
                    'metamorphosis.txt',
                    'doom_that_came_to_sarnath.txt',
                    'dream_quest_of_unknown_kadath.txt',
                    'pride_and_prejudice.txt',
                    'jane_eyre.txt',
                    'sea_garden.txt',
                    'the_waste_land.txt',
                    'the_raven.txt',
                    'fall_of_the_house_of_usher.txt',
                    'the_colors_of_space.txt',
                    'frankenstein.txt',
                    'the_last_man.txt']

def install():
    print("installing templates...")
    for template_data in templates:
        print("\t{}".format(template_data['name']))
        t = Template(template_data)
        t.save()

    print("installing source texts...")
    for source_filename in source_filenames:
        source_path = path.join(path.dirname(__file__), 'static/txt', source_filename)
        print("\treading {}".format(source_path))
        text = open(source_path).read()
        s = Source({'name':source_filename,
                    'text':text,
                    'uploader': cfg.SYSTEM_USER})
        print("\tprocessing {}".format(source_path))
        s.process()
        print("\tsaving {}".format(source_path))
        s.save()

    print('adding system user')
    u = User({'name':cfg.SYSTEM_USER,
              'password': ''})
    u.save()
