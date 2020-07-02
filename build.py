import os
from pathlib import Path
import markdown2
import json

from post import Post

if __name__ == '__main__':

    if not os.path.isdir("posts"):
        print("Folder 'posts' not found.")
        exit()

    posts = []

    for file in os.listdir("posts"):
        if file.endswith(".md"):
            posts.append(Post(os.path.join("posts", file)))

    posts = sorted(posts, key=lambda x: x.creation_time, reverse=True)

    print(len(posts), "posts were found")

    Path("result/posts").mkdir(parents=True, exist_ok=True)

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

        jsonObj["posts"].append(postObj)

    json_file = open("result/posts.json", mode='w', encoding='utf-8')
    json_file.write(json.dumps(jsonObj))
    json_file.close()
    print("Done!")

    for post in posts:
        print("Processing " + post.path + "...", end='')

        html = markdown2.markdown(post.content)

        html_file = open(os.path.join("result/posts", post.id + ".html"), mode='w', encoding='utf-8')
        html_file.write(html)
        html_file.close()

        print("Done!")
