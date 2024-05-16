from setuptools import setup, find_packages

setup(
    name='django_sql_query_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
    ],
    entry_points={
        'console_scripts': [
            'manage = django.core.management:execute_from_command_line',
        ],
    },
)
