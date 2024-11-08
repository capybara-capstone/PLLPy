#importing pandas as pd 
import pandas as pd 
import sys 

def main():
  args = sys.argv[1:]

  read_file = pd.read_excel(f"{args[0]}") 
  print(f"{args}")
  read_file.to_csv (f"{args[1]}",  
                  index = None, 
                  header=True) 
   
if __name__ == "__main__":
  main()
