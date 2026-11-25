# Overview
This section contains preliminary familiarisation steps with the core libraries of the project. It is also designed to complement (and satisfy) the performance requirements of the preliminary assessment.

## Required performance demonstration

You must demonstrate your ability at:

- Determining an organisation’s technology, development tools, and UI platform
- Enabling interprocess communication in Python while using third-party libraries and referencing third-party documentation


## Instructions

1. Complete the knowledge section (Word document) available via Blackboard
2. Fork this repository
3. Clone the repository to your local computer
4. Install `uv` and check that it is running with `uv --version`
5. Obtain a video that can be used to test the functionality and place in the `resources` folder - your instructor will provide you with one
6. Follow the steps in the remainder of the guide insuring your commit to git whenever prompted
7. Submit a `zip` of this repository along with the `.git` folder. **Do not include your `venv/`**. Ensure your submission includes the assessment Word document with all of the questions in it attempted.


## Steps
Complete the steps below and fill in the `> block` sections
> If you see a section like this, fill it in!


### Installing and running OpenCV

1. Examine the `pyproject.toml` what dependencies does it currently identify?
>currently there are no dependencies
>
2. Create a `.venv` in this folder using `uv venv`
3. Activate the `venv` as instructed by `uv`
4. In order to complete the project, we need to install OpenCV. Fill in the following:
  - What role does OpenCV have in this project?
  >
  - What is the `uv pip` command to install OpenCV?
  > `uv pip install opencv-python
  - What is the URL of this library's git repo?
  > [(https://github.com/opencv/opencv/releases/tag/5.1.0)](https://github.com/opencv/????-?????)
5. Add OpenCV to your project using the `uv add` command:
  > `uv add name-of-open-cv-library

6. Have the dependencies in the `pyproject.toml` changed? If so, how?
  >Yes, dependencies are now: dependencies = [
    "opencv-python>=5.1.0.95",
]
  >
7. Why did we use `uv add` over `uv pip`?
  >using 'uv add' also adds the dependencies to the pyproject.toml file and updates the uv.lock file as well as what uv pip does - installs the package in the virtual environment. It essentially helps to manage the dependencies so that the project can be reproduced reliably.
  >
8. The `numpy` library is required for OpenCV. Should you add an explicit requirement for it? Why/Why not?
  >Yes, although it is already declared as a dependency in opencv-python, it is better to explicitly add it as this will help to avoid any version conflicts that may arise, especially if using other packages in the same project. 
  >
9. Commit the changes so far to git. Use the message `chore: add OpenCV dependency`
10. Go to `preliminary/library_basics.py` and complete the required functionality.
11. Commit your changes with `feat: save video frames`


### Installing and running Tesseract

[Tesseract OCR](https://github.com/tesseract-ocr/tesseract) provides optical character recognition (OCR) functionality needed for the project.

Tesseract consists of both an OCR Engine and a command line program. It is predominantly written in C++.

1. Examine the [Readme](https://github.com/tesseract-ocr/tesseract?tab=readme-ov-file) and find a list of Python wrappers.

2. What is the URL that lists Python wrappers for Tesseract?
  > [[<url-here>]]https://tesseract-ocr.github.io/tessdoc/AddOns.html#tesseract-wrappers

3. Select a Python wrapper. What wrapper did you choose and why? Ensure you address each element below in your answer
> name of the python library: pytesseract
> how long ago was a commit made to the library: 18th February 2025 (~9 months ago)
> does it have external dependencies: It requires python 3.6 or later, it is just a wrapper and still requires the tesseract ocr engine, and it uses the Python Imaging Library (PIL / pillow).
> how does it suit the project requirements

4. Use UV to add the dependency to your project and your `pyproject.toml`

5. If your library has additional requirements (e.g. installing tesseract binaries), note it in your README.md

6. Commit the new dependency `chore: add tesseract dependency`

7. Add a new method in `library_basics.py` that returns the text of a given frame/time/image (you decide!)

8. Commit the changes as `feat: OCR an image


### Install and run FastAPI

FastAPI will allow us to enable communication with our OCR service from other processes on the current machine or across a network.

1. Add the requirement for FastAPI using UV. FastAPI has optional requirements so the command is a little different:
`uv add fastapi --extra standard`
2. Commit the new dependency `chore: add FastAPI dependency`
3. Run in development mode using:
`uv run fastapi dev preliminary/simple_api.py`
4. Run the following curl command (may require git bash on Windows):
`curl 127.0.0.1:8000/video`
5. Confirm that a list of videos and URLs is returned by copying the output below:
> {"count":1,"videos":[{"id":"demo","path":"..\\resources\\oop.mp4","_links":{"self":"/video/demo","frame_example":"/video/demo/frame/1.0"}}]}
6. What are the names of the two processes that just communicated?
>A HTTP client-server communication. The curl command was run in a terminal - this is the client sending the get request to the server (uvicorn) running the fastapi, and getting a response (JSON)
6. Modify the simple_api.py so that it works correctly with your implementation and complete any TODO markers
7. Demonstrate the use of at least two other end points below:
>http://127.0.0.1:8000/video/demo:
>{"fps":23.976023976023978,"frame_count":15152,"duration_seconds":631.9646666666666}
>http://127.0.0.1:8000/video/demo/frame/42:
><img width="1151" height="695" alt="image" src="https://github.com/user-attachments/assets/ed18171b-98e4-4023-ad13-d2eee5e90ad4" />
http://127.0.0.1:8000/video/demo/frame/42/ocr:
{"text":"I finally saw The Matrix today.\nIt was the best documentary\nI've ever seen.\n\n"}
>
>
