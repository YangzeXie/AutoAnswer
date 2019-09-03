from cx_Freeze import setup, Executable  
  
  
setup(name='xg',  
      version = '0.1',  
      description='xg helper',  
      executables = [Executable("xg.py")]  
  
      )  