# PyLessons v1.1

## W.I.P.
Currently working on integration with [destreamer](https://github.com/snobu/destreamer) so you can use this providing the link to the lesson or a file with the links of multiple lessons, instead of having to download the lessons separately.

## Things to know
Currently working with **.mkv** video files only

## Prereqs
- [**Python 3.x**](https://www.python.org/): you will need python installed on your system. (Developed with python 3.9.4).
- [**ffmpeg**](https://www.ffmpeg.org/): a recent version (year 2019 or above), in `$PATH` or the .exe in the same directory as this README file (project root).

## Setup
You will need to install all the python dependencies of the project, so i recommend creating a venv for this.
```sh
$ python -m venv my-env
$ ./my-env/Scripts/activate
```
Install dependencies from the *requirements.txt*. You **MUST** be in the same folder as the .txt
```sh
$ pip install -r requirements.txt
```

## How to use

Open cmd (or any terminal) and go to the project folder

```sh
$ cd D:\Documents\Dev\py-lessons
```
Launch the "py-lesson.py" and give as first parameter **the path** to the folder with the video lessons

```sh
$ .\pylesson.py D:\Documents\Destream\destreamer\videos
```
