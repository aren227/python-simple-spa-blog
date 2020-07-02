# python-simple-spa-blog

Static site generator using Python. This is a personal project for building my own blog on github.io.
It just converts markdown files to html files and builds posts.json file which includes information of all posts.

Template is required for deploying a fully functional blog.

### Features
 - Simple static site builder like Jekyll.
 - Single-page application.
 - Project and tags support.
 - File creation/modification time management.

### Requirements
 - markdown2

### How to use
 1. Write a post in markdown format. There are no rules about file names, but you have to write a file header like this:
    ```
    ---
    title: Hello, World!
    project: python-simple-spa-blog (optional)
    tags: Python, JSON (optional)
    ---
    Contents...
    ```
 2. If you need another resource like image, put it into same folder or its subfolder.
 3. Run ```build.py <POSTS FOLDER PATH> <TEMPLATE FOLDER PATH>```
