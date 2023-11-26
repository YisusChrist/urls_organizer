<p align="center"><img width="750" src="https://i.imgur.com/Scbk7tO.png" alt="Urls_organizer"></p>

<p align="center">
    <a href="https://github.com/yisuschrist/urls_organizer/issues">
        <img src="https://img.shields.io/github/issues/yisuschrist/urls_organizer?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/urls_organizer/forks">
        <img src="https://img.shields.io/github/forks/yisuschrist/urls_organizer?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/urls_organizer/">
        <img src="https://img.shields.io/github/stars/yisuschrist/urls_organizer?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/urls_organizer/actions">
        <img alt="Tests Passing" src="https://github.com/yisuschrist/urls_organizer/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/yisuschrist/urls_organizer/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/yisuschrist/urls_organizer?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/gpl-3-0/">
        <img alt="License" src="https://img.shields.io/github/license/yisuschrist/urls_organizer?color=0088ff">
    </a>
    <!--
    <a href="https://github.com/yisuschrist/urls_organizer/issues/contributors">
        <img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/yisuschrist/urls_organizer" />
    </a>
    -->
</p>

<br>

<p align="center">
    <a href="https://github.com/yisuschrist/urls_organizer/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/yisuschrist/urls_organizer/issues/new/choose">Request Feature</a>
    ·
    <a href="https://github.com/yisuschrist/urls_organizer/discussions">Ask Question</a>
    ·
    <a href="https://github.com/yisuschrist/urls_organizer/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/c3525653303a46af833c14fd7587342852c3d494.svg "Repobeats analytics image")

<br>

Urls_organizer is a Python program that helps to organize a list of URLs. It can read URLs from a file or add a single URL, removes duplicate URLs, and sorts them in natural order.

Additionally, the program can validate the URLs by sending a GET request and checking for the ones that are not available anymore. The program uses **multiprocessing to speed up the validation process**, and the results are saved in a separate file. The output URL list can be saved in a file specified by the user. The program takes command-line arguments for its inputs and parameters.

The purpose of the program is to assist users in managing their lists of URLs by keeping them organized and validating their accuracy.

<br>

<details>
<summary>Table of Contents</summary>

- [Requirements](#requirements)
- [Installation](#installation)
  - [Manual installation](#manual-installation)
- [Execution](#execution)
  - [Example of execution](#example-of-execution)
- [Contributors](#contributors)
  - [How do I contribute to Urls_organizer?](#how-do-i-contribute-to-urls_organizer)
- [TODO](#todo)
- [License](#license)
- [Credits](#credits)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

- [natsort](https://pypi.org/project/natsort) (version 8.4.0)
- [platformdirs](https://pypi.org/project/platformdirs) (version 3.11.0)
- [prettytable](https://pypi.org/project/prettytable) (version 3.9.0)
- [pyfiglet](https://pypi.org/project/pyfiglet) (version 0.8.post1)
- [requests](https://pypi.org/project/requests) (version 2.31.0)
- [rich](https://pypi.org/project/rich) (version 13.5.2)
- [rich-argparse-plus](https://pypi.org/project/rich-argparse-plus) (version 0.3.1.4)
- [string-grab](https://pypi.org/project/string-grab) (version 1.3.0)
- [termcolor](https://pypi.org/project/termcolor) (version 2.3.0)
- [tqdm](https://pypi.org/project/tqdm) (version 4.66.1)
- [validators](https://pypi.org/project/validators) (version 0.22.0)

These packages can be installed using the following command:

```bash
pip3 install -r requirements.txt
```

This will install all the packages and their dependencies listed in the requirements.txt file. Make sure you have Python and pip installed on your system before running this command.

> Note: The software has been developed and tested using Python 3.10.10. The minimum required version to run the software is Python 3.6. Although the software may work with previous versions, it is not guaranteed.

## Installation

Urls_organizer can be installed by running one of the following commands in your terminal. You can install this via the command-line with either `curl`, `wget` or another similar tool.

| Method    | Command                                                                                              |
| :-------- | :--------------------------------------------------------------------------------------------------- |
| **curl**  | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/yisuschrist/urls_organizer/main/install.sh)"` |
| **wget**  | `sh -c "$(wget -O- https://raw.githubusercontent.com/yisuschrist/urls_organizer/main/install.sh)"`   |
| **fetch** | `sh -c "$(fetch -o - https://raw.githubusercontent.com/yisuschrist/urls_organizer/main/install.sh)"` |

#### Manual installation

If you prefer to install the program manually, follow these steps:

> Note: This will install the version from the latest commit, not the latest release.

1. Download the latest version of [urls_organizer](https://github.com/yisuschrist/urls_organizer) from this repository:

```bash
git clone https://github.com/yisuschrist/urls_organizer
cd urls_organizer
```

2. Install the dependencies:

```bash
pip3 install -r requirements.txt
```

3. Run the following commands to install urls_organizer in your `/usr/bin/` directory:

```bash
sudo chmod +x urls_organizer
sudo cp urls_organizer /usr/bin/
```

The program can now be ran from a terminal with the `urls_organizer` command.

## Execution

To run the `urls_organizer` script, you can use the following command:

```bash
python3 -m urls_organizer [OPTIONS]
```

where `[OPTIONS]` are the command line options described below:

```
usage: urls_organizer [-sf SAVEFILE] [-rf READFILE] [-u URL] [-w NUMWORKERS] [-h] [-v] [-d] [-V]

Organize your URL saved like a pro!

OPTIONS TO ADD URLS
  -sf, --saveFile SAVEFILE
                        File with the URLs result. Argument is required
  -rf, --readFile READFILE
                        File with the URLs to add. Argument is required if -u is not used.
  -u, --url URL         Single URL to add. Argument is required if -rf is not used.
  -w, --numWorkers NUMWORKERS
                        Number of workers to use. Default is the number of CPU cores * 2.

MISCELLANEOUS OPTIONS
  -h, --help            Show this help message and exit.
  -v, --verbose         Show log messages on screen. Default is False.
  -d, --debug           Activate debug logs. Default is False.
  -V, --version         Show version number and exit.
```

#### Example of execution

Content of _`urls.txt`_:

```txt
https://www.youtube.com
http://www.google.com
https://www.facebook.coma
https://www.youtube.com
```

Execute the program with the following command:

```bash
urls_organizer -rf urls.txt -sf urls_organized.txt -w 10
```

Content of _`urls_organized.txt`_:

```txt
https://google.com
https://youtube.com
```

Content of _`invalid_urls.txt`_:

```txt
https://www.facebook.coma
```

## Contributors

<a href="https://github.com/yisuschrist/urls_organizer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yisuschrist/urls_organizer" />
</a>

### How do I contribute to Urls_organizer?

Before you participate in our delightful community, please read the [code of conduct](.github/CODE_OF_CONDUCT.md).

I'm far from being an expert and suspect there are many ways to improve – if you have ideas on how to make the configuration easier to maintain (and faster), don't hesitate to fork and send pull requests!

We also need people to test out pull requests. So take a look through [the open issues](https://github.com/yisuschrist/urls_organizer/issues) and help where you can.

See [Contributing](.github/CONTRIBUTING.md) for more details.

## TODO

Planing to add the following features:

- [ ] Add support for multiple input/output files
- [ ] Add a full documentation in Wiki section
- [ ] Add uninstall bash script
- [ ] Add a Changelog / Release Notes

## License

Urls_organizer is released under the [GPL-3.0 License](https://opensource.org/licenses/GPL-3.0)

## Credits

<img src="https://avatars.githubusercontent.com/u/31022056?v=4" width="100px;" alt="Marvin Wendt" border-radius="50% !important;" />

Thanks to [Marvin Wendt](https://github.com/MarvinJWendt) for the installation script template. Original code of the **Instl** project can be found [here](https://github.com/installer/instl).

I made a few modifications to the original script to fit my needs (error control, fetching of repository release content and installation of required dependencies) because I found problems when running the autogenerated script.
