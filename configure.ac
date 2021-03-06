AC_INIT(freespeak, 0.3.0, [http://developer.berlios.de/bugs/?group_id=10396])
AC_CONFIG_SRCDIR(freespeak/__init__.py)
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE
GNOME_COMMON_INIT

AM_MAINTAINER_MODE
AM_DISABLE_STATIC
AM_PROG_LIBTOOL
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")
AC_PROG_CC

dnl ****************************************************************************
dnl * Translation & i18n
dnl ****************************************************************************

GETTEXT_PACKAGE="freespeak"
IT_PROG_INTLTOOL([0.35.0])
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
ALL_LINGUAS="it fr sv"
AM_GLIB_GNU_GETTEXT

dnl ****************************************************************************
dnl * Gnome Doc Utils
dnl ****************************************************************************
GNOME_DOC_INIT

dnl ****************************************************************************
dnl * GConf support
dnl ****************************************************************************
AC_PATH_PROG(GCONFTOOL, gconftool-2)
AM_GCONF_SOURCE_2

dnl ****************************************************************************
dnl * Python 2.4
dnl ****************************************************************************
AM_PATH_PYTHON(2.4)

dnl ****************************************************************************
dnl * Write the values of various paths in defs.py
dnl ****************************************************************************
AC_SUBST(VERSION)
AC_SUBST(PACKAGE)

AS_AC_EXPAND(DATADIR, $datarootdir)
AC_SUBST(DATADIR)

AS_AC_EXPAND(LIBDIR, $libdir)
AC_SUBST(LIBDIR)

AS_AC_EXPAND(LIBEXECDIR, $libexecdir)
AC_SUBST(LIBEXECDIR)

AS_AC_EXPAND(PYTHONDIR, $pythondir)
AC_SUBST(PYTHONDIR)
		
dnl ****************
dnl * Python modules
dnl ****************
AM_CHECK_PYMOD(dbus)
AM_CHECK_PYMOD(gconf)
AM_CHECK_PYMOD(gettext)
AM_CHECK_PYMOD(gobject)
AM_CHECK_PYMOD(gtk)
AM_CHECK_PYMOD(gtk.gdk)
AM_CHECK_PYMOD(gtkmozembed)
AM_CHECK_PYMOD(gtkspell)
AM_CHECK_PYMOD(lxml)
AM_CHECK_PYMOD(lxml.html)
AM_CHECK_PYMOD(pango)
AM_CHECK_PYMOD(Xlib)

dnl ****************************************************************************
dnl * --------------------------------------------------------------------------
dnl ****************************************************************************
AC_OUTPUT([
Makefile
bin/Makefile
freespeak/Makefile
freespeak/defs.py
freespeak/translators/Makefile
freespeak/ui/Makefile
freespeak/applet/Makefile
data/Makefile
data/art/Makefile
data/freespeak.desktop.in
data/Freespeak_Applet.server.in
docs/Makefile
help/Makefile
po/Makefile.in
])

echo
echo $PACKAGE v$VERSION
echo