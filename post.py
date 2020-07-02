import time
import os
import hashlib
import random
import re

class Post:

    def __init__(self, path):
        self.path = path

        file = open(path, mode='r', encoding='utf-8')
        lines = file.readlines()

        if lines[0].strip() != "---":
            raise RuntimeError("Header not found in " + path)

        header_end = 0
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                header_end = i
                break

        if header_end == 0:
            raise RuntimeError("Header was not closed in " + path)

        self.title = None
        self.project = ""
        self.tags = []

        for i in range(1, header_end):
            spl = lines[i].split(':')
            if len(spl) == 0 or spl[0].strip() not in ("title", "project", "tags"):
                print("Invalid line detected in " + path, "Ignoring...")
                continue

            if spl[0].strip() == "title":
                self.title = ":".join(spl[1:]).strip()
            if spl[0].strip() == "project":
                self.project = ":".join(spl[1:]).strip()
            if spl[0].strip() == "tags":
                tags = (":".join(spl[1:])).split(",")
                self.tags = [tag.strip() for tag in tags]

        if self.title is None:
            raise RuntimeError("Title was not found in " + path)

        self.content = "\n".join(lines[header_end + 1:])
        self.content = re.sub(r"!\[(.*?)\]\((.*?)\)", r"![\1](posts__/\2)", self.content)  # prefix posts__/ to img path

        file.close()

        self.id = None
        self.hash = None
        self.creation_time = None
        self.modification_time = None

        self.read_meta()
        if self.id is None:
            self.create_meta()

    def read_meta(self):
        if os.path.isfile(self.path + ".meta"):
            meta_file = open(self.path + ".meta", mode='r', encoding='utf-8')
            lines = meta_file.readlines()
            meta_file.close()

            if len(lines) < 3 or len(lines) > 4:
                print("Invalid meta file detected:", self.path + ".meta", "Recreating...")
                return

            self.id = lines[0].strip()
            self.hash = lines[1].strip()
            self.creation_time = int(lines[2].strip())
            if len(lines) > 3:
                self.modification_time = int(lines[3].strip())

            new_hash = hashlib.md5(self.content.encode('utf-8')).hexdigest()
            if self.hash != new_hash:
                self.hash = new_hash
                self.modification_time = int(time.time())
                meta_file = open(self.path + ".meta", mode='w', encoding='utf-8')
                meta_file.write(self.id + "\n" + self.hash + "\n" + str(self.creation_time) + "\n" + str(self.modification_time))
                meta_file.close()

    def create_meta(self):
        meta_file = open(self.path + ".meta", mode='w', encoding='utf-8')

        self.id = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789') for _ in range(8))
        self.hash = hashlib.md5(self.content.encode('utf-8')).hexdigest()
        self.creation_time = int(time.time())

        meta_file.write(self.id + "\n" + self.hash + "\n" + str(self.creation_time))
        meta_file.close()

    def get_preview(self, length=100):
        content = self.content.replace('\n', ' ')
        return content[:length]

    def get_thumbnail(self):
        result = re.search(r"!\[.*?\]\((.*?)\)", self.content)
        if result is None:
            return None
        return result.group(1)  # First occurrence
