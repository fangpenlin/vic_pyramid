from __future__ import unicode_literals
import os
import sys


def replace_package_lines(lines, project_name):
    for line in lines:
        l = line
        l = l.replace('{{package}}', project_name)
        l = l.replace('{{project}}', project_name)
        l = l.replace('{{package_logger}}', project_name)
        yield l


def get_diff(scaffolds_dir, target_dir, project_name, ext=None):
    ext = ext or ['.py', '.ini', '.genshi']
    for dirpath, dirname, filenames in os.walk(target_dir):
        for filename in filenames:
            work_fullpath = os.path.join(dirpath, filename)
            work_relpath = os.path.relpath(work_fullpath, target_dir)

            _, e = os.path.splitext(work_fullpath)
            if e not in ext:
                continue

            if '.egg' in work_fullpath:
                continue

            with open(work_fullpath, 'rt') as f:
                work_lines = list(f.readlines())

            tmpl = False
            for line in work_lines:
                if project_name in line:
                    tmpl = True

            sc_relpath = work_relpath.replace(project_name, '+package+')
            if tmpl:
                sc_relpath = sc_relpath + '_tmpl'
            sc_fullpath = os.path.join(scaffolds_dir, sc_relpath)

            stack = []
            current_path = sc_fullpath
            while True:
                base, name = os.path.split(current_path)
                if os.path.exists(base):
                    break
                stack.append(base)
                current_path = base

            for dirname in stack[::-1]:
                os.mkdir(dirname)

            with open(sc_fullpath, 'wt') as f:
                for line in work_lines:
                    l = line
                    l = l.replace(project_name, '{{package}}')
                    f.write(l)


def main():
    from vic_pyramid import scaffolds 
    scaffolds_dir = os.path.dirname(scaffolds.__file__)
    scaffolds_dir = os.path.join(scaffolds_dir, 'vic_pyramid')
    get_diff(scaffolds_dir, sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
