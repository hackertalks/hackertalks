try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='hackertalks',
    version='0.2',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "Jinja2",
        "docutils>=0.5",
        "sqlalchemy-migrate>=0.5.3",
        "WebHelpers",
        "ToscaWidgets",
        "tw.forms",
        "psycopg2",
        "fixture",
        "feedparser",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'hackertalks': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'hackertalks': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = hackertalks.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    
    [paste.paster_command]
    upload_dir = hackertalks.ht_commands.upload_dir:Upload_Dir
    import_blipuser = hackertalks.ht_commands.import_blipuser:Import_BlipUser
    """,
)
