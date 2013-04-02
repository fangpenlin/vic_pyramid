import os
import sys
import difflib


def replace_package_lines(lines, project_name):
    for line in lines:
        l = line
        l = l.replace('{{package}}', project_name)
        l = l.replace('{{project}}', project_name)
        l = l.replace('{{package_logger}}', project_name)
        yield l


def get_diff(scaffolds_dir, target_dir, project_name, ext=None):
    ext = ext or ['.py']
    for dirpath, dirname, filenames in os.walk(scaffolds_dir):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(fullpath, scaffolds_dir)

            tmpl = False
            proj_relpath = relpath.replace('+package+', project_name)
            if proj_relpath.endswith('_tmpl'):
                proj_relpath = proj_relpath[:-len('_tmpl')]
                tmpl = True
            proj_fullpath = os.path.join(target_dir, proj_relpath)

            _, e = os.path.splitext(proj_fullpath)
            if e not in ext:
                continue

            if not os.path.exists(proj_fullpath):
                # TODO: 
                continue

            with open(fullpath, 'wt') as a:
                with open(proj_fullpath, 'rt') as b:
                    for line in b.readlines():
                        l = line
                        l = l.replace(project_name, '{{package}}')
                        a.write(l)

def main():
    from vic_pyramid import scaffolds 
    scaffolds_dir = os.path.dirname(scaffolds.__file__)
    scaffolds_dir = os.path.join(scaffolds_dir, 'vic_pyramid')
    get_diff(scaffolds_dir, sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
