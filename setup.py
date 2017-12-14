"""setup for gas_monitor"""

from distutils.core import setup
def main():
    setup(
        name="gas_monitor",
        version='0.1',
        install_requires=[
            'pyyaml'
        ]
    )

if __name__ == "__main__":
    main()