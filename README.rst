Randomizeitor (deprecated)
==========================

**Randomizeitor is DEPRECATED, it hasn't been updated in a very long time and is not expected to currently work**.

Randomizeitor is a simple GNOME wallpaper randomizer created by Fidel Ramos (aka
haplo) because, shockingly, there wasn't anything up to the task already. Sure,
there were some scripts here and there, but I wanted more control.

I was inspired by a script by Kevin Bridges: http://kevinbridges.org/node/60

Randomizeitor is licensed under the GNU GPL v3 (see COPYING).

Go to http://github.com/haplo/randomizeitor for the latest version.

Usage
-----

Just run the script passing the path to the directory with the wallpapers,
for example::

  python randomizeitor.py ~/wallpapers/

or if randomizeitor.py is executable::

  ./randomizeitor.py ~/wallpapers/

Randomizeitor will filter the files to select only images. Also, randomizeitor
writes a *.randomizeitor* hidden file in the wallpaper dir to remember which
wallpapers have already been picked, to avoid repetitions.

The best way to set up a periodic random wallpaper change is to edit your
crontab with ``crontab -e`` and then putting something like::

  */5 * * * * bash -c "DISPLAY=:0.0 /(...)/randomizeitor.py /(...)/wallpapers/"

This will trigger a random wallpaper change every 5 minutes. ``DISPLAY=:0.0`` is
required because *cron* doesn't have information about your X session. The value
of ``DISPLAY`` may vary if you are not in the first graphical session in the
machine.

If you only want a wallpaper change at GNOME start you can set it up at
*System->Preferences->Startup Programs*.

Dependencies
------------

 * Python 2.5 (it may or may not work in 2.4, but it's untested)
 * python-gconf

Future features
---------------

In no particular order:

 * Allow for recursive search of files.
 * Allow for different wallpapers if there are multiple screens.
 * Config file.
 * Create a GNOME applet.
 * Useful GUI.
