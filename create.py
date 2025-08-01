import argparse
import os
import shutil


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Создание папки и файловой структуры для задачи")
    parser.add_argument("number", type=int, default=0, help="Номер задачи")
    parser.add_argument("only_style", type=bool, default=True, help="Изменить только стиль")
    args = parser.parse_args()
    
    already_created = os.listdir("problems")
    if args.number != 0:
        if str(args.number) not in already_created:
            os.mkdir(f"problems/{args.number}")
        if "img" not in os.listdir(f"problems/{args.number}"):
            os.mkdir(f"problems/{args.number}/img")
        if "main.tex" not in os.listdir(f"problems/{args.number}"):
            shutil.copy("sample.tex", f"problems/{args.number}/main.tex")
        if "DayProblem.sty" not in os.listdir(f"problems/{args.number}") or args.only_style:
            shutil.copy("DayProblem.sty", f"problems/{args.number}/DayProblem.sty")
    elif args.only_style:
        print(already_created)
        for i in already_created:
            shutil.copy("DayProblem.sty", f"problems/{i}/DayProblem.sty")