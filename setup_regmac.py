from cx_Freeze import setup, Executable  
  
  
setup(name='test to exe',  
      version = '0.1',  
      description='test from py file to exe file',  
      executables = [Executable("regmac.py")]  
  
      )  