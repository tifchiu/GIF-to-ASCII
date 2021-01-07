# GIF-to-ASCII
Converts GIFs to images made with ASCII, frame-by-frame.  
Done in Python.  

Created by University of Waterloo first and second year CS students:

Tiffany Chiu - Lead Software Engineer  
Mark Chen - Software Engineer  
Nicole Shi - Software Engineer  
Ted Weng - Software Engineer  
Bonnie Peng - Software Engineer

See our other project done in parallel which [converts images to ASCII characters.](https://github.com/marko-polo-cheno/Abstract-ASCII-Adapter/)  

### How it works
Pre-condition: we have a GIF called "mood.gif" in the current directory.
![](mood.gif)
1. Install the latest version of the Python Imaging Library and Jinja2  
```
pip install -r installs.txt
```
2. Run  
```
python gifToText.py mood.gif
```
  with any or all of the following command-line flags  
```
-m <n>            ## Maximum width of the output GIF is <n>
-c                ## Generate GIF with colour
-t "<character>"  ## Use create GIF using <character> at every pixel
```
