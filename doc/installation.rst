============
Installation
============

The installation of ``ts_dateloc`` requires the use of the LSST software stack. Follow the installation instructions from `here <https://pipelines.lsst.io/install/newinstall.html#installing-from-source-with-newinstall-sh>`_ to get a minimal setup. Go ahead and let the stack software provide Python unless you feel comfortable providing your own. Follow the instructions to get into the stack environment. The instructions will refer to the stack installation directory as ``stack_install_dir``.

Next, install the following stack packages::

    eups distrib install sims_utils -t sims

Now install the source code into your favorite location (called ``gitdir``) via::

	git clone https://github.com/lsst-ts/ts_dateloc.git

With the stack environment setup as instructed above, declare the packge to EUPS::

	cd gitdir/ts_dateloc
	eups declare ts_dateloc git -r . -c
	setup ts_dateloc git
	scons

**NOTE**: The declaration steps only need to be done once. After that do::

	source stack_install_dir/loadLSST.<shell>
	setup ts_dateloc git