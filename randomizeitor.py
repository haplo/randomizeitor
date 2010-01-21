#!/usr/bin/python
"""
Simple GNOME wallpaper randomizer.

Created by Fidel Ramos (haplo). Licensed under GPL v3.

Inspired by a script by Kevin Bridges: http://kevinbridges.org/node/60.

Go to http://github.com/haplo/randomizeitor for the latest version.

For usage info read README (duh!)

"""

import gconf
import mimetypes
import os
import random
import sys


class RandomizeitorError(Exception):
    pass


class Randomizeitor(object):
    """Sets a new random wallpaper in GNOME picking it from a given
    collection and taken care not to repeat twice."""

    def __init__(self, wallpaper_dir):
        self._check_directory(wallpaper_dir)
        self._client = gconf.client_get_default()
        self.wallpaper_dir = wallpaper_dir
        self.already_picked = os.path.abspath(os.path.join(wallpaper_dir, '.randomizeitor'))

    def _check_directory(self, wallpaper_dir):
        if not os.path.isdir(wallpaper_dir):
            raise RandomizeitorError(u"%s is not a directory" % wallpaper_dir)

    def get_current_wallpaper(self):
        return self._client.get_string("/desktop/gnome/background/picture_filename")

    def set_wallpaper(self, wallpaper):
        self._client.set_string("/desktop/gnome/background/picture_filename",
                                wallpaper)
        self._remember_wallpaper(wallpaper)

    def set_random_wallpaper(self):
        candidate_wallpapers = self.get_candidate_wallpapers()
        if candidate_wallpapers:
            the_chosen_one = random.choice(candidate_wallpapers)
            self.set_wallpaper(the_chosen_one)
            return the_chosen_one
        else:
            print u"No wallpapers found!"
            return None

    def _remember_wallpaper(self, wallpaper):
        datafile = open(self.already_picked, "a")
        datafile.write(wallpaper+os.linesep)
        datafile.close()

    def _already_picked(self):
        wallpapers = []
        if os.path.exists(self.already_picked):
            datafile = open(self.already_picked, "r")
            wallpapers = [l.strip() for l in datafile.readlines() if l.strip()]
            datafile.close()
        return wallpapers

    def get_candidate_wallpapers(self):
        """Retrieve a list of available wallpapers, discarding those previously
        shown (stored in a hidden datafile)."""
        files = self.get_all_images()
        already_picked = self._already_picked()
        available_wallpapers = [w for w in files if w not in already_picked]
        if files and not available_wallpapers: # every wallpaper showed once, reset
            try:
                os.remove(self.already_picked)
                available_wallpapers = self.get_candidate_wallpapers()
            except OSError, e:
                print u"ERROR: %s, can't delete %s" % (e, self.already_picked)
        return available_wallpapers

    def get_all_images(self):
        files = []
        try:
            files = os.listdir(self.wallpaper_dir)
            def filter_format(f):
                full_path = os.path.abspath(os.path.join(self.wallpaper_dir, f))
                mtype = mimetypes.guess_type(full_path)[0]
                return mtype is not None and mtype.startswith('image/')
            files = filter(filter_format, files)
            files = [os.path.abspath(os.path.join(self.wallpaper_dir, f)) for f in files]
        except OSError, e:
            print u"ERROR: %s, ignoring" % e
        return files

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print u"Usage: python %s /path/to/wallpaper/directory/" % sys.argv[0]
        sys.exit(0)
    wallpaper_dir = sys.argv[1]
    try:
        client = Randomizeitor(wallpaper_dir)
        chosen_wallpaper = client.set_random_wallpaper()
        if chosen_wallpaper is not None:
            print u"New wallpaper! %s" % chosen_wallpaper
    except RandomizeitorError, e:
        print u"ERROR: %s" % e.message
        sys.exit(1)
    sys.exit(0)
