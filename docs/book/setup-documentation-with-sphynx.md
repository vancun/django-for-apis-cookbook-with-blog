# Setup Project Documentation with Sphynx

Setting up Sphinx documentation for a Python project involves several steps, including installing Sphinx, configuring it, and generating the documentation. Here’s a step-by-step guide to help you get started:

### 1. Install Sphinx
First, you need to install Sphinx and other necessary packages. You can do this using pip:

```sh
pip install sphinx
```

Optionally, you can also install the `sphinx-autobuild` package for live-reloading during documentation development:

```sh
pip install sphinx-autobuild
```

### 2. Create Documentation Directory
Navigate to your project’s root directory and create a directory for your documentation (commonly named `docs`):

```sh
mkdir docs
cd docs
```

### 3. Initialize Sphinx
Run the Sphinx quickstart command to initialize the documentation:

```sh
sphinx-quickstart
```

This command will prompt you with several questions to configure your Sphinx setup. You can accept the default values or customize them as needed. Key questions include:

- Project name
- Author name
- Project version
- Separate source and build directories (usually a good idea to say "yes")

### 4. Configure Sphinx
After running `sphinx-quickstart`, you will have a `conf.py` file in your `docs` directory. Open this file to configure Sphinx according to your project’s needs. Here are some common configurations:

#### Add Extensions
Add any Sphinx extensions you want to use. For example, to use the `autodoc` extension, add it to the `extensions` list:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google and NumPy style docstrings
    'sphinx.ext.viewcode',  # To include links to the source code
]
```

#### Set Path for Modules
Ensure that Sphinx can find your project modules by adding the project’s root directory to `sys.path`. Modify the `sys.path` in `conf.py`:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
```

#### Configure HTML Theme
You can change the HTML theme to something more appealing. For example, to use the popular "Read the Docs" theme:

```python
html_theme = 'sphinx_rtd_theme'
```

Make sure to install the theme:

```sh
pip install sphinx_rtd_theme
```

### 5. Document Your Code
Use docstrings in your Python modules to document your code. Sphinx can automatically extract these docstrings to generate documentation. Here’s an example of a module with Google-style docstrings:

```python
def example_function(param1, param2):
    """
    This is an example function.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
    return True
```

### 6. Generate Documentation
In your `docs` directory, create a reStructuredText (.rst) file that includes your modules. For example, create a `index.rst` file and add your modules:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

.. automodule:: your_module
   :members:
   :undoc-members:
   :show-inheritance:
```

### 7. Build the Documentation
Generate the HTML documentation by running:

```sh
make html
```

Your generated documentation will be in the `_build/html` directory. Open the `index.html` file in your browser to view it.

### 8. (Optional) Auto-Generate `.rst` Files
If you have many modules and want to automate the creation of `.rst` files, you can use the `sphinx-apidoc` command:

```sh
sphinx-apidoc -o . ../your_project
```

This command will generate `.rst` files for all your modules, which you can then include in your `index.rst`.

### 9. Live-Reload (Optional)
If you installed `sphinx-autobuild`, you can use it to auto-reload your documentation as you make changes:

```sh
sphinx-autobuild . _build/html
```

### Example Directory Structure
After setting up Sphinx, your project directory might look like this:

```
your_project/
├── docs/
│   ├── _build/
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── modules.rst
│   ├── Makefile
│   ├── make.bat
├── your_project/
│   ├── __init__.py
│   ├── module1.py
│   ├── module2.py
├── setup.py
└── requirements.txt
```

This setup will help you maintain a clean and organized structure for your documentation. By following these steps, you’ll be able to set up Sphinx documentation for your Python project effectively.

