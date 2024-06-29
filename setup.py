from setuptools import setup, find_packages

setup(
    name='wordle-quordle-solver',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'tkinter',  # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'wordle_solver_gui=gui.wordle_gui:main',
            'quordle_solver_gui=gui.quordle_gui:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['frequencyMaps/*.txt', 'frequencyMaps/*.json'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
