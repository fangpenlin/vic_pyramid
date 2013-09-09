# -*- coding: utf8 -*-
import os
import sys
import shutil
import unittest
import subprocess
import logging


class TestScaffolds(unittest.TestCase):
    def setUp(self):
        import vic_pyramid
        # redirect messages to logger
        self.stdout_logger = logging.getLogger('stdout')
        self.stderr_logger = logging.getLogger('stderr')

        self.pkg_dir, _ = os.path.split(os.path.dirname(vic_pyramid.__file__))
        self.version = open(os.path.join(self.pkg_dir, 'VERSION')).read()

        # create source distribute
        if sys.platform == 'win32':
            ext = 'zip'
        else:
            ext = 'tar.gz'
        self.pkg_filename = os.path.join(
            self.pkg_dir, 
            'dist', 
            'vic_pyramid-{}.{}'.format(self.version, ext)
        )
        if os.path.exists(self.pkg_filename):
            os.remove(self.pkg_filename)
        self.check_call(
            [sys.executable, 'setup.py', 'sdist'], 
            shell=False, 
            cwd=self.pkg_dir,
        )

        # create test folder
        self.test_folder = os.path.join(self.pkg_dir, 'test_folder')
        if not os.path.exists(self.test_folder):
            os.mkdir(self.test_folder)

        # create virtualenv
        self.test_env = os.path.join(self.test_folder, 'env')
        if not os.path.exists(self.test_env):
            self.check_call(
                ['virtualenv', '--no-site-packages', 'env'], 
                shell=False, 
                cwd=self.test_folder,
            )

        if sys.platform == 'win32':
            self.test_scripts_folder = os.path.join(self.test_env, 'Scripts')
        else:
            self.test_scripts_folder = os.path.join(self.test_env, 'bin')
        self.test_python = os.path.join(self.test_scripts_folder, 'python')
        self.test_pip = os.path.join(self.test_scripts_folder, 'pip')
        self.test_pcreate = os.path.join(self.test_scripts_folder, 'pcreate')

        # install vic_pyramid
        try:
            self.check_call(
                [self.test_pip, 'uninstall', '-y', 'vic_pyramid'], 
                shell=False, 
                cwd=self.test_folder,
            )
        except subprocess.CalledProcessError:
            pass
        self.check_call(
            [self.test_pip, 'install', self.pkg_filename], 
            shell=False, 
            cwd=self.test_folder,
        )

        self.helloworld_folder = os.path.join(self.test_folder, 'helloworld')
        # remove old project
        if os.path.exists(self.helloworld_folder):
            shutil.rmtree(self.helloworld_folder)
        # create a helloworld project
        self.check_call(
            [self.test_pcreate, '-s', 'vic_pyramid', 'helloworld'], 
            shell=False, cwd=self.test_folder
        )

    def check_call(self, *args, **kwargs):
        from pyramid.settings import asbool
        echo = asbool(os.environ.get('TEST_ECHO', False))
        if not echo:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE
        proc = subprocess.Popen(*args, **kwargs)
        stdoutdata, stderrdata = proc.communicate()
        if not echo:
            for line in stdoutdata.splitlines():
                line = line.strip()
                self.stdout_logger.info(line)
            for line in stderrdata.splitlines():
                line = line.strip()
                self.stderr_logger.info(line)
        ret = proc.wait()
        if ret:
            raise subprocess.CalledProcessError(
                returncode=ret,
                cmd=proc.cmd,
            )
        return ret

    def test_flake8(self):
        # install flake8
        self.check_call(
            [self.test_pip, 'install', 'flake8'], 
            shell=False, 
            cwd=self.test_folder,
        )

        flake8 = os.path.join(self.test_scripts_folder, 'flake8')
        self.check_call(
            [flake8, 'helloworld', '--ignore=W293,W291,E501', '--show-source'], 
            shell=False, 
            cwd=self.helloworld_folder,
        )

    def test_file_existing(self):
        def assert_exists(*path):
            self.assertTrue(os.path.exists(os.path.join(self.test_folder, *path)))
        assert_exists('helloworld', 'distribute_setup.py')
        assert_exists('helloworld', 'requirements.txt')
        assert_exists('helloworld', 'test_requirements.txt')
        assert_exists('helloworld', 'helloworld', 'locale')
        for ext in ['eot', 'svg', 'ttf', 'woff']:
            assert_exists(
                'helloworld', 
                'helloworld', 
                'static', 
                'font-awesome', 
                'font', 
                'fontawesome-webfont.' + ext
            )
        assert_exists(
            'helloworld', 
            'helloworld', 
            'static', 
            'font-awesome', 
            'font', 
            'FontAwesome.otf',
        )

    def test_scaffolds(self):
        # install requirements
        self.check_call(
            [
                self.test_pip, 'install', '-r', 
                os.path.join(self.helloworld_folder, 'requirements.txt')
            ], 
            shell=False, cwd=self.helloworld_folder
        )

        # install testing requirements
        self.check_call(
            [
                self.test_pip, 'install', '-r', 
                os.path.join(self.helloworld_folder, 'test_requirements.txt')
            ], 
            shell=False, cwd=self.helloworld_folder
        )

        # install the project
        self.check_call(
            [self.test_python, 'setup.py', 'develop'], 
            shell=False, cwd=self.helloworld_folder
        )

        # test the project
        self.check_call(
            [self.test_python, 'setup.py', 'nosetests', '-v'], 
            shell=False, cwd=self.helloworld_folder
        )


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestScaffolds))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
