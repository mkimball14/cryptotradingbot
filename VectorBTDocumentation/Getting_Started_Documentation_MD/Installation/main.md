# Installation[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#installation "Permanent link")

Info

VectorBT® PRO is a totally different beast compared to the open-source version. In fact, the PRO version redesigns the underlying core to enable groundbreaking features. 

To avoid using an outdated code, make sure to only import **vectorbtpro**!


# Requirements[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#requirements "Permanent link")


# Authentication[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#authentication "Permanent link")


# Option 1: Token[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#option-1-token "Permanent link")

After you've been added to the list of collaborators and accepted the repository invitation, the next step is to create a [Personal Access Token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) for your GitHub account in order to access the PRO repository programmatically (from the command line or GitHub Actions workflows):

 1. Go to <https://github.com/settings/tokens>
 2. Click on [Generate a new token (classic)]
 3. Enter a name (such as "terminal")
 4. Set the expiration to some fixed number of days
 5. Select the [`repo`](https://docs.github.com/en/developers/apps/scopes-for-oauth-apps#available-scopes) scope
 6. Generate the token and save it in a safe place

Important

After a few months, you might receive an email from GitHub notifying you that your personal access token has expired. If this happens, please follow the steps outlined above to generate a new token. This has nothing to do with your membership status!


# Option 2: Credential Manager[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#option-2-credential-manager "Permanent link")

Alternatively, use [Git Credential Manager](https://github.com/git-ecosystem/git-credential-manager) instead of creating a personal access token.

Note

Git Credential Manager only supports HTTPS.


# Git[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#git "Permanent link")

If you don't have Git, [install it](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).


# TA-Lib[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#ta-lib "Permanent link")

To use TA-Lib for Python, you need to install the actual library. Follow [these instructions](https://github.com/mrjbq7/ta-lib#dependencies).

Hint

If you have issues installing TA-Lib, or you don't need it in your work, you can also install vectorbtpro [without TA-Lib](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#without-ta-lib).


# Recommendations[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#recommendations "Permanent link")


# Windows[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#windows "Permanent link")

If you're on Windows, it's recommended to use [WSL](https://learn.microsoft.com/en-us/windows/wsl/setup/environment) for development.


# New environment[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#new-environment "Permanent link")

If you plan to use vectorbtpro locally, it's recommended to establish a new environment solely for vectorbtpro.


# Conda[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#conda "Permanent link")

The easiest way is to [download Anaconda](https://www.anaconda.com/download), which has a graphical installer and comes with many popular data science packages required by vectorbtpro such as NumPy, Pandas, Plotly, and more.

After the installation, [create a new environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-0-1)conda create --name vectorbtpro python=3.11
 
[/code]

[Activate the new environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-1-1)conda activate vectorbtpro
 
[/code]

Note

You need to activate the environment every time you start a new terminal session.

You should now see `vectorbtpro` in the list of all environments and being active (notice `*`):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-2-1)conda info --envs
 
[/code]

You can now proceed with the installation of the actual package.


# IDE[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#ide "Permanent link")

If you primarily work with an IDE, you can create a separate environment for each project. [Here](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html) is how to create a new environment with PyCharm. The same but for Visual Studio Code is explained [here](https://code.visualstudio.com/docs/python/environments).


# With pip[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#with-pip "Permanent link")

The PRO version can be installed with `pip`.

Hint

It's highly recommended creating a new virtual environment solely for vectorbtpro, such as with [Anaconda](https://www.anaconda.com/).

Uninstall the open-source version if installed:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-3-1)pip uninstall vectorbt
 
[/code]


# HTTPS[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#https "Permanent link")

Install the base PRO version (with recommended dependencies) using `git+https`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-4-1)pip install -U "vectorbtpro[base] @ git+https://github.com/polakowo/vectorbt.pro.git"
 
[/code]

Info

This operation may require at least 1GB of disk space and take several minutes to complete.

Hint

Whenever you are prompted for a password, paste the token that you generated in the previous steps.

To avoid re-entering the token over and over again, you can [add it to your system](https://stackoverflow.com/a/68781050) or set an environment variable `GH_TOKEN` and then install the package as follows:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-5-1)pip install -U "vectorbtpro[base] @ git+https://${GH_TOKEN}@github.com/polakowo/vectorbt.pro.git"
 
[/code]

On some systems, such as macOS, the token is usually remembered automatically.

Read more on managing tokens [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).


# Without TA-Lib[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#without-ta-lib "Permanent link")

Base version without TA-Lib:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-6-1)pip install -U "vectorbtpro[base-no-talib] @ git+https://github.com/polakowo/vectorbt.pro.git"
 
[/code]


# Lightweight[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#lightweight "Permanent link")

Lightweight version (with only required dependencies):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-7-1)pip install -U git+https://github.com/polakowo/vectorbt.pro.git
 
[/code]

For other optional dependencies, see [pyproject.toml](https://github.com/polakowo/vectorbt.pro/blob/main/pyproject.toml).


# SSH[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#ssh "Permanent link")

To install the base version with `git+ssh`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-8-1)pip install -U "vectorbtpro[base] @ git+ssh://git@github.com/polakowo/vectorbt.pro.git"
 
[/code]

See [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).


# Updating[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#updating "Permanent link")

Whenever a new version of vectorbtpro is released, the package **will not** update by itself - you need to install the update. Gladly, you can use the same exact command that you used to install the package to also update it.


# Specific branch[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#specific-branch "Permanent link")

Append `@` followed by [a branch name](https://github.com/polakowo/vectorbt.pro/branches/all) to the command.

For example, to install the `develop` branch:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-9-1)pip install -U "vectorbtpro[base] @ git+https://github.com/polakowo/vectorbt.pro.git@develop"
 
[/code]

Note

If you have the latest regular version installed, you must uninstall it first:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-10-1)pip uninstall vectorbtpro
 
[/code]


# Specific release[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#specific-release "Permanent link")

Append `@` followed by [a release name](https://github.com/polakowo/vectorbt.pro/releases) to the command.

For example, to install the release `v2024.1.30`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-11-1)pip install "vectorbtpro[base] @ git+https://github.com/polakowo/vectorbt.pro.git@v2024.1.30"
 
[/code]


# As Python dependency[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#as-python-dependency "Permanent link")

With [setuptools](https://setuptools.readthedocs.io/en/latest/) adding vectorbtpro as a dependency to your Python package can be done by listing it in setup.py or in your [requirements files](https://pip.pypa.io/en/latest/user_guide/#requirements-files):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-1)# setup.py
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-2)setup(
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-3) # ...
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-4) install_requires=[
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-5) "vectorbtpro @ git+https://github.com/polakowo/vectorbt.pro.git"
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-6) ]
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-7) # ...
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-12-8))
 
[/code]


# With git[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#with-git "Permanent link")

Of course, you can pull vectorbtpro directly from `git`:

HTTPSSSH
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-13-1)git clone https://github.com/polakowo/vectorbt.pro.git vectorbtpro
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-14-1)git clone git@github.com:polakowo/vectorbt.pro.git vectorbtpro
 
[/code]

Install the package:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-15-1)pip install -e vectorbtpro
 
[/code]


# Shallow clone[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#shallow-clone "Permanent link")

The command above takes around 1GB of disk space, to create a shallow clone:

HTTPSSSH
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-16-1)git clone https://github.com/polakowo/vectorbt.pro.git vectorbtpro --depth=1
 
[/code]
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-17-1)git clone git@github.com:polakowo/vectorbt.pro.git vectorbtpro --depth=1
 
[/code]

To convert the clone back into a complete one:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-18-1)git pull --unshallow
 
[/code]


# With Docker[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#with-docker "Permanent link")

Using [Docker](https://www.docker.com/) is a great way to get up and running in a few minutes, as it comes with all dependencies pre-installed.

[Docker image of vectorbtpro](https://github.com/polakowo/vectorbt.pro/blob/main/Dockerfile) is based on [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) \- a set of ready-to-run Docker images containing Jupyter applications and interactive computing tools. Particularly, the image is based on [jupyter/scipy-notebook](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook), which includes a minimally-functional JupyterLab server and preinstalled popular packages from the scientific Python ecosystem, and extends it with Plotly and Dash for interactive visualizations and plots, and vectorbtpro and most of its optional dependencies. The image requires the source of vectorbtpro to be available in the current depository.

Before proceeding, make sure to [have Docker installed](https://docs.docker.com/install/).

Launch Docker using Docker Desktop.


# Building[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#building "Permanent link")

Clone the vectorbtpro repository (if not already). Run this from a directory where you want vectorbtpro to reside, for example, in Documents/GitHub:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-19-1)git clone git@github.com:polakowo/vectorbt.pro.git vectorbtpro --depth=1
 
[/code]

Go into the directory:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-20-1)cd vectorbtpro
 
[/code]

Build the image (can take some time):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-21-1)docker build . -t vectorbtpro
 
[/code]

Create a working directory inside the current directory:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-22-1)mkdir work
 
[/code]


# Running[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#running "Permanent link")

Start a container running a JupyterLab Server on the port 8888:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-23-1)docker run -it --rm -p 8888:8888 -v "$PWD/work":/home/jovyan/work vectorbtpro
 
[/code]

Info

The use of the `-v` flag in the command mounts the current working directory on the host (`{PWD/work}` in the example command) as `/home/jovyan/work` in the container. The server logs appear in the terminal. Due to the usage of [the flag --rm](https://docs.docker.com/engine/reference/run/#clean-up---rm) Docker automatically cleans up the container and removes the file system when the container exits, but any changes made to the `~/work` directory and its files in the container will remain intact on the host. [The -it flag](https://docs.docker.com/engine/reference/commandline/run/#assign-name-and-allocate-pseudo-tty---name--it) allocates pseudo-TTY.

Alternatively, if the port 8888 is already in use, use another port (here 10000):
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-24-1)docker run -it --rm -p 10000:8888 -v "$PWD/work":/home/jovyan/work vectorbtpro
 
[/code]

Once the server has been launched, visit its address in a browser. The address is printed in the console, for example: `http://127.0.0.1:8888/lab?token=9e85949d9901633d1de9dad7a963b43257e29fb232883908`

Note

Change the port if necessary.

This will open JupyterLab where you can create a new notebook and start working with vectorbtpro ![🎉](https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.0.3/assets/svg/1f389.svg)

To make use of any files on the host, put them into to the working directory `work` on the host and they will appear in the file browser of JupyterLab. Alternatively, you can drag and drop them directly into the file browser of JupyterLab.


# Stopping[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#stopping "Permanent link")

To stop the container, first hit `Ctrl`+`C`, and then upon prompt, type `y` and hit `Enter`


# Updating[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#updating_1 "Permanent link")

To upgrade the Docker image to a new version of vectorbtpro, first, update the local version of the repository from the remote:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-25-1)git pull
 
[/code]

Then, rebuild the image:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-26-1)docker build . -t vectorbtpro
 
[/code]

Info

This won't rebuild the entire image, only the vectorbtpro installation step.


# Manually[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#manually "Permanent link")

In case of connectivity issues, the package can be also installed manually:

 1. Go to <https://github.com/polakowo/vectorbt.pro>
 2. Click on the `Code` dropdown button and then "Download ZIP"
 3. Unzip the downloaded archive
 4. Open the unzipped folder using terminal
 5. Install the package using pip:

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-27-1)pip install ".[base]"
 
[/code]


# Custom release[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#custom-release "Permanent link")

To install a custom release:

 1. Go to <https://github.com/polakowo/vectorbt.pro/releases>
 2. Select a release
 3. Download the file with the suffix `.whl`
 4. Open the folder with the wheel file using terminal
 5. Install the wheel using pip:

[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-28-1)pip install wheel
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-28-2)pip install "filename.whl[base]"
 
[/code]

Replace `filename` with the actual file name.

Note

If the file name ends with `(1)` because there's already a file with the same name, make sure to remove the previous file and remove the `(1)` suffix from the newer one.


# Google Colab[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#google-colab "Permanent link")

[ Notebook](https://colab.research.google.com/drive/1A9RxtYgGkUT_NbRxp3Z8h-fTRnVR3WRa?usp=sharing)


# Troubleshooting[¶](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#troubleshooting "Permanent link")

 * [TA-Lib](https://github.com/mrjbq7/ta-lib#dependencies)
 * [Jupyter Notebook and JupyterLab](https://plotly.com/python/getting-started/#jupyter-notebook-support)
 * [Apple M1](https://github.com/polakowo/vectorbt/issues/320)
 * ["fatal error: 'H5public.h' file not found"](https://stackoverflow.com/a/71340786)
 * ["RuntimeError: CMake must be installed to build qdldl"](https://github.com/robertmartin8/PyPortfolioOpt/issues/274#issuecomment-1551221810)
 * pybind11:

If you're getting the error "ModuleNotFoundError: No module named 'pybind11'", install `pybind11` prior to the installation of vectorbtpro:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-29-1)pip install pybind11
 
[/code]

 * llvmlite:

If you're getting the error "Cannot uninstall 'llvmlite'", install `llvmlite` prior to the installation of vectorbtpro:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-30-1)pip install --ignore-installed 'llvmlite'
 
[/code]

 * Plotly:

If image generation hangs (such as when calling `show_svg()`), downgrade the Kaleido package:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-31-1)pip install kaleido==0.1.0post1
 
[/code]

 * osqp:

If you're on a Mac and encountering an error during the installation of the osqp package, install `cmake`:
[code] 
 [](https://vectorbt.pro/pvt_7a467f6b/getting-started/installation/#__codelineno-32-1)brew install cmake
 
[/code]