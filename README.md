# PyLessons v1.2

## W.I.P.
Currently working on refactoring since we have a nice spaghetti plate here...
<br>Next up : 
  - Better UX
   
## Things to know
Currently working with **.wav** audio files only.

## Prereqs
- [**Python 3.x**](https://www.python.org/): you will need python installed on your system. (Developed with python 3.9.4).
- [**ffmpeg**](https://www.ffmpeg.org/): a recent version (year 2019 or above), in `$PATH` or the .exe in the same directory as this README file (project root).
- [**destream**](https://github.com/snobu/destreamer): needed for downloading lesson videos from microsoft stream

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

Open cmd (or any terminal) and go to the project folder and activate the virtual env

```sh
$ cd D:\Documents\Dev\py-lessons
```
```sh
$ env\Scripts\activate
```
Launch the "py-lesson.py"

```sh
$ python pylesson.py
```
The output file will be at root level of the folder
