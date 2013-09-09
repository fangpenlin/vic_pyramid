# -*- coding: utf8 -*-
import os
import sys
import shutil
import unittest
import subprocess


class TestScaffolds(unittest.TestCase):
    def setUp(self):
        import vic_pyramid
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
            'vic_pyramid-%s.%s' % (self.version, ext)
        )
        if os.path.exists(self.pkg_filename):
            os.remove(self.pkg_filename)
        subprocess.check_call(
            [sys.executable, 'setup.py', 'sdist'], 
            shell=False, 
            cwd=self.pkg_dir,
        )

        # create test folder
        self.test_folder = os.path.join(self.pkg_dir, 'test_folder')
        if not os.path.exists(self.test_folder):
            os.mkdir(self.test_folder)

        # create virtualenv
        subprocess.check_call(
            ['virtualenv', '--no-site-packages', 'env'], 
            shell=False, 
            cwd=self.test_folder,
        )

        if sys.platform == 'win32':
            self.test_scripts_folder = os.path.join(self.test_folder, 'env', 'Scripts')
        else:
            self.test_scripts_folder = os.path.join(self.test_folder, 'env', 'bin')
        self.test_python = os.path.join(self.test_scripts_folder, 'python')
        self.test_pip = os.path.join(self.test_scripts_folder, 'pip')
        self.test_pcreate = os.path.join(self.test_scripts_folder, 'pcreate')

        # install vic_pyramid
        subprocess.call(
            [self.test_pip, 'uninstall', '-y', 'vic_pyramid'], 
            shell=False, 
            cwd=self.test_folder,
        )
        subprocess.check_call(
            [self.test_pip, 'install', self.pkg_filename], 
            shell=False, 
            cwd=self.test_folder,
        )

        self.helloworld_folder = os.path.join(self.test_folder, 'helloworld')
        # remove old project
        if os.path.exists(self.helloworld_folder):
            shutil.rmtree(self.helloworld_folder)
        # create a helloworld project
        subprocess.check_call(
            [self.test_pcreate, '-s', 'vic_pyramid', 'helloworld'], 
            shell=False, cwd=self.test_folder
        )

    def test_flake8(self):
        # install flake8
        subprocess.call(
            [self.test_pip, 'install', 'flake8'], 
            shell=False, 
            cwd=self.test_folder,
        )

        flake8 = os.path.join(self.test_scripts_folder, 'flake8')
        subprocess.check_call(
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
        subprocess.check_call(
            [
                self.test_pip, 'install', '-r', 
                os.path.join(self.helloworld_folder, 'requirements.txt')
            ], 
            shell=False, cwd=self.helloworld_folder
        )

        # install testing requirements
        subprocess.check_call(
            [
                self.test_pip, 'install', '-r', 
                os.path.join(self.helloworld_folder, 'test_requirements.txt')
            ], 
            shell=False, cwd=self.helloworld_folder
        )

        # install the project
        subprocess.check_call(
            [self.test_python, 'setup.py', 'develop'], 
            shell=False, cwd=self.helloworld_folder
        )

        # test the project
        subprocess.check_call(
            [self.test_python, 'setup.py', 'nosetests', '-v'], 
            shell=False, cwd=self.helloworld_folder
        )


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestScaffolds))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
