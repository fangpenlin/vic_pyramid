# -*- coding: utf8 -*-
import unittest


class TestScaffolds(unittest.TestCase):
    def setUp(self):
        import sys
        import os
        import subprocess
        import vic_pyramid
        self.pkg_dir, _ = os.path.split(os.path.dirname(vic_pyramid.__file__))
        self.version = open(os.path.join(self.pkg_dir, 'VERSION')).read()

        # create source distribute
        if sys.platform == 'win32':
            ext = 'zip'
        else:
            ext = 'tar.gz'
        self.pkg_filename = os.path.join(self.pkg_dir, 'dist', 'vic_pyramid-%s.%s' % (self.version, ext))
        if os.path.exists(self.pkg_filename):
            os.remove(self.pkg_filename)
        subprocess.check_call([sys.executable, 'setup.py', 'sdist'], shell=False, cwd=self.pkg_dir)

        # create test folder
        self.test_folder = os.path.join(self.pkg_dir, 'test_folder')
        if not os.path.exists(self.test_folder):
            os.mkdir(self.test_folder)

        # install virtualenv
        subprocess.check_call(['virtualenv', '--no-site-packages', 'env'], shell=False, cwd=self.test_folder)

        if sys.platform == 'win32':
            self.test_scripts_folder = os.path.join(self.test_folder, 'env', 'Scripts')
        else:
            self.test_scripts_folder = os.path.join(self.test_folder, 'env', 'bin')
        self.test_python = os.path.join(self.test_scripts_folder, 'python')
        self.test_pip = os.path.join(self.test_scripts_folder, 'pip')
        self.test_pcreate = os.path.join(self.test_scripts_folder, 'pcreate')

        # install vic_pyramid
        subprocess.call([self.test_pip, 'uninstall', '-y', 'vic_pyramid'], shell=False, cwd=self.test_folder)
        subprocess.check_call([self.test_pip, 'install', self.pkg_filename], shell=False, cwd=self.test_folder)

        # create a helloworld project
        subprocess.check_call([self.test_pcreate, '-s', 'vic_pyramid', 'helloworld'], 
            shell=False, cwd=self.test_folder)
        self.helloworld_folder = os.path.join(self.test_folder, 'helloworld')
        
    def tearDown(self):
        pass

    def assert_exists(self, *path):
        import os
        self.assert_(os.path.exists(os.path.join(self.test_folder, *path)))

    def test_scaffolds(self):
        import subprocess
        # make sure some files exist
        self.assert_exists('helloworld', 'helloworld', 'locale')
        for ext in ['eot', 'svg', 'ttf', 'woff']:
            self.assert_exists('helloworld', 'helloworld', 'static', 'font-awesome', 'font', 'fontawesome-webfont.' + ext)
        self.assert_exists('helloworld', 'helloworld', 'static', 'font-awesome', 'font', 'FontAwesome.otf')

        # install the project
        subprocess.check_call([self.test_python, 'setup.py', 'develop'], 
            shell=False, cwd=self.helloworld_folder)

        # test the project
        subprocess.check_call([self.test_python, 'setup.py', 'nosetests', '-v'], 
            shell=False, cwd=self.helloworld_folder)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestScaffolds))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
