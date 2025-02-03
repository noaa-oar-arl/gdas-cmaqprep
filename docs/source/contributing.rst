Contributing to GDAS CMAQ Preprocessor
======================================

We love your input! We want to make contributing to GDAS CMAQ Preprocessor as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

Development Process
-------------------

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from ``main``
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code meets our coding standards
6. Issue that pull request!

Fork, then clone the repo:

.. code-block:: bash

    git clone git@github.com:your-username/gdas-cmaqprep.git

Pull Request Process
--------------------

1. Update the README.md with details of changes to the interface, if applicable
2. Update the documentation with any new dependencies, configuration options, or features
3. The PR will be merged once you have the sign-off of at least one maintainer
4. The PR should work for Python 3.8+.

Any contributions you make will be under the BSD 3-Clause License
-----------------------------------------------------------------

In short, when you submit code changes, your submissions are understood to be under the same `BSD 3-Clause License`_ that covers the project. Feel free to contact the maintainers if that's a concern.

Report bugs using GitHub's `issue tracker`_
-------------------------------------------

We use GitHub issues to track public bugs. Report a bug by `opening a new issue`_.

Write bug reports with detail, background, and sample code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or things you tried that didn't work)

Coding Style
------------

* Use 4 spaces for indentation
* Follow PEP 8 style guidelines
* Use descriptive variable names
* Add comments for complex logic
* Keep functions focused and concise
* Use type hints
* Write docstrings in Google style

Testing
-------

Before submitting a pull request, please ensure:

1. Your code includes unit tests
2. All existing tests pass
3. Your code is well-documented
4. You've added docstrings to new functions

To run tests locally::

    python -m pytest tests/

Documentation
-------------

We use Sphinx for documentation. Please update the documentation when you make changes:

1. Update docstrings for any modified functions
2. Add new .rst files for new modules
3. Update the index.rst if needed
4. Build and check the documentation locally::

    cd docs
    make html

* Use Google style docstrings
* Keep documentation up to date
* Add examples where appropriate
* Include doctest examples when possible

License
-------

By contributing, you agree that your contributions will be licensed under the BSD 3-Clause License.

References
----------

.. _BSD 3-Clause License: https://opensource.org/licenses/BSD-3-Clause
.. _issue tracker: https://github.com/noaa-arl/gdas-cmaqprep/issues
.. _opening a new issue: https://github.com/noaa-arl/gdas-cmaqprep/issues/new

Questions?
----------

Contact the maintainers if you have any questions about contributing.

Feel free to open an issue with questions.

Thank you for your interest in improving GDAS CMAQ Preprocessor!
