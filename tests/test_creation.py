import os
import pytest
from subprocess import check_output
from conftest import system_check, args


def no_curlies(filepath):
    """ Utility to make sure no curly braces appear in a file.
        That is, was jinja able to render everthing?
    """
    with open(filepath, 'r') as f:
        data = f.read()

    template_strings = [
        '{{',
        '}}',
        '{%',
        '%}'
    ]

    template_strings_in_file = [s in data for s in template_strings]
    return not any(template_strings_in_file)


@pytest.mark.usefixtures("default_baked_project")
class TestCookieSetup(object):

    def test_project_name(self):
        project = self.path
        if pytest.param.get('project_name'):
            name = system_check(args['project_name'])
            assert project.name == name
        else:
            assert project.name == 'project_name'

    def test_author(self):
        setup_ = self.path / 'setup.py'
        setup_args = ['python', setup_, '--author']
        p = check_output(setup_args).decode('ascii').strip()
        if pytest.param.get('author_name'):
            assert p == args['author_name']
        else:
            assert p == 'Your name (or your organization/company/team)'

    def test_readme(self):
        readme_path = self.path / 'README.md'
        assert readme_path.exists()
        assert no_curlies(readme_path)
        if pytest.param.get('project_name'):
            with open(readme_path) as fin:
                assert next(fin).strip() == args['project_name']

    def test_setup(self):
        setup_ = self.path / 'setup.py'
        setup_args = ['python', setup_, '--version']
        p = check_output(setup_args).decode('ascii').strip()
        assert p == '0.1.0'

    def test_requirements(self):
        reqs_path = self.path / 'requirements.txt'
        assert reqs_path.exists()
        assert no_curlies(reqs_path)

    def test_makefile(self):
        makefile_path = self.path / 'Makefile'
        assert makefile_path.exists()
        assert no_curlies(makefile_path)

    def test_folders(self):
        expected_dirs = [
            'data',
            'data/external',
            'data/interim',
            'data/processed',
            'data/raw',
            'models',
            'notebooks',
            'references',
            'reports',
            'reports/figures',
            'src',
            'src/data',
            'src/features',
            'src/models',
            'src/visualization',
        ]

        ignored_dirs = [
            str(self.path)
        ]

        abs_expected_dirs = [str(self.path / d) for d in expected_dirs]
        abs_dirs, _, _ = list(zip(*os.walk(self.path)))
        assert len(set(abs_expected_dirs + ignored_dirs) - set(abs_dirs)) == 0

