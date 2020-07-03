import os
from pathlib import Path
import markdown2
import json
import sys
import shutil

from post import Post

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please provide post and template folder path.")
        print("build.py <POST_FOLDER_PATH> <TEMPLATE_FOLDER_PATH>")
        exit()

    POSTS_FOLDER = sys.argv[1]
    TEMPLATE_FOLDER = sys.argv[2]

    if not os.path.isdir(POSTS_FOLDER):
        print("Posts folder not found: " + POSTS_FOLDER)
        exit()

    if not os.path.isdir(TEMPLATE_FOLDER):
        print("Template folder not found: " + TEMPLATE_FOLDER)
        exit()

    posts = []
    meta_files = []

    for file in os.listdir(POSTS_FOLDER):
        if file.endswith(".md") and file != "README.md":
            posts.append(Post(os.path.join(POSTS_FOLDER, file)))
            meta_files.append(file + ".meta")

    for file in os.listdir(POSTS_FOLDER):
        if file.endswith(".meta") and file not in meta_files:
            os.remove(os.path.join(POSTS_FOLDER, file))

    posts = sorted(posts, key=lambda x: x.creation_time, reverse=True)

    print(len(posts), "posts were found")

    tags = set()
    for post in posts:
        for tag in post.tags:
            tags.add(tag)

    projects = set()
    for post in posts:
        if post.project != "":
            projects.add(post.project)

    tags = sorted(list(tags))
    projects = sorted(list(projects))

    print("Tags:", tags)
    print("Projects:", projects)

    print("Generating posts.json...", end='')

    jsonObj = dict()
    jsonObj["projects"] = projects
    jsonObj["tags"] = tags
    jsonObj["posts"] = []

    for post in posts:
        postObj = dict()
        postObj["id"] = post.id
        postObj["creation_time"] = post.creation_time
        if post.modification_time is not None:
            postObj["modification_time"] = post.modification_time
        postObj["title"] = post.title
        if post.project != "":
            postObj["project"] = post.project
        postObj["tags"] = post.tags
        postObj["preview"] = post.get_preview()

        thumbnail = post.get_thumbnail()
        if thumbnail is not None:
            postObj["thumbnail"] = thumbnail

        jsonObj["posts"].append(postObj)

    json_file = open("posts.json", mode='w', encoding='utf-8')
    json_file.write(json.dumps(jsonObj))
    json_file.close()
    print("Done!")

    print("Cleaning output folder...", end='')
    shutil.rmtree("posts__")
    Path("posts__").mkdir()
    print("Done!")

    for post in posts:
        print("Processing " + post.path + "...", end='')

        html = markdown2.markdown(post.content, extras=['fenced-code-blocks'])

        html_file = open(os.path.join("posts__", post.id + ".html"), mode='w', encoding='utf-8')
        html_file.write(html)
        html_file.close()

        print("Done!")

    print("Placing resource files...", end='')
    for file in os.listdir(POSTS_FOLDER):
        full_path = os.path.join(POSTS_FOLDER, file)
        if os.path.isfile(full_path) and not file.endswith(".md") and not file.endswith(".meta"):
            shutil.copy(full_path, os.path.join("posts__", file))
        elif os.path.isdir(full_path):
            shutil.copytree(full_path, os.path.join("posts__", file))

    print("Placing template files...", end='')
    for file in os.listdir(TEMPLATE_FOLDER):
        full_path = os.path.join(TEMPLATE_FOLDER, file)
        if os.path.isfile(full_path) and file != "README.md":
            shutil.copy(full_path, file)
        elif os.path.isdir(full_path):
            shutil.copytree(full_path, file)
    print("Done!")
