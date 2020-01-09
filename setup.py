import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    author='John Jung',
    author_email='jej@uchicago.edu',
    description='Scripts to build IIIF records for digital collections at the University of Chicago.',
    entry_points={
        'console_scripts': [
            'cli_collection_browse = iiif_tools.cli_collection_browse:main',
            'soc_sci_maps_build_manifest = iiif_tools.soc_sci_maps_build_manifest:main',
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='iiif_tools',
    packages=setuptools.find_packages(),
    url='https://github.com/johnjung/iiif_tools',
    version='0.0.1'
)
