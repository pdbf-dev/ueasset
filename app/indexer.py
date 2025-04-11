import os
import re
from db import Session, File, Tag
from yaml import safe_load


# App configuration
with open(f"app/config.yaml", "r") as _f:
    config = safe_load(_f)
path_to_files = config["file_archive_path"]

# Tag-to-regex mappings
with open(f"app/regex_tags.yaml", "r") as _f:
    tag_regexes = safe_load(_f)

def index_files(base_dir):
    session = Session()

    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.uasset') and (
                '_sk_' in filename.lower() or
                '_sm_' in filename.lower()
            ):
                path = os.path.abspath(os.path.join(root, filename))
                file_obj = session.query(File).filter_by(path=path).first()
                if not file_obj:
                    file_obj = File(path=path)
                    session.add(file_obj)

                # Automatic tagging
                for tag_name, regex_list in tag_regexes.items():
                    for regex in regex_list:
                        if re.match(regex, filename, re.I):
                            tag_obj = session.query(Tag).filter_by(name=tag_name).first()
                            if not tag_obj:
                                tag_obj = Tag(name=tag_name)
                                session.add(tag_obj)
                            if tag_obj not in file_obj.tags:
                                file_obj.tags.append(tag_obj)
                            break

    session.commit()
    session.close()

if __name__ == '__main__':
    index_files(path_to_files)
