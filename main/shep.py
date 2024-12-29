# External libs
import argparse
from interactive_interpreter import interactive_interpret
import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "The ShepLang language interpreter.")
    parser.add_argument("-f" ,"--file", help = "Path to the file to run.", type = str, default = "test.shep")
    parser.add_argument("method", help = "What mode to run the interpreter in: 'run' - run the interpreter. 'debug' - run with extra debug info. 'interactive' - run in interactive terminal mode. Also, 'debug' mode gives you a cool logo.", choices = ['run', 'debug', 'interactive'])

    args = parser.parse_args()

    if args.method in ["run", "debug"]:
        if not args.file:
            print("Err - Missing required arguments for single scrape.")
        else:
            if args.file.split(".")[-1] != "shep":
                print(f"Err - please provide a proper '.shep' file! '.{args.file.split('.')[-1]}' files will not suffice!")
            else:
                print(f"Launching ShepLang interpreter for file {args.file}.")
                main.run(args.file, (args.method == "debug")) 
    elif args.method == "interactive":
        interactive_interpret()
    else:
        print(f"Err - unrecognised run method parsed: {args.method}")


