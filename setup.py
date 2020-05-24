import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='ppgm',  
     version='0.0.3',
     author="Avinash Kori",
     author_email="koriavinash1@gmail.com",
     description="Graphical model analysis toolbox.",
     long_description=open("README.md").read(),
   long_description_content_type="text/markdown",
     url="https://github.com/koriavinash1/pgm",
     packages=setuptools.find_packages(),
     install_requires = [
         'pandas',
	 'numpy'
         ],
     classifiers=[
         "Programming Language :: Python :: 3.5",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
