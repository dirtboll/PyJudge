import psutil, os, sys, shutil, time, argparse, difflib
from concurrent.futures import ThreadPoolExecutor, as_completed
from subprocess import PIPE
from colorama import Fore, Style
_TWO_20 = float(2 ** 20)
_ROOT_DIR = os.getcwd()
_TMP_FOLDER = ".tmp"
_TMP_DIR = _ROOT_DIR + "/" + _TMP_FOLDER
_HTML_FOLDER = "Difference Table"
_HTML_DIR = _ROOT_DIR + "/" + _HTML_FOLDER
_OUT = ".out.tmp"

src_file = "test.java"
tc_dir = "tc"

def judge(class_name, i):
    wa = False
    tle = False
    rte = False

    inp = open(tc_dir + f"/in{str(i)}")
    my_out = f"{_OUT}.{str(i)}"
    out = open(my_out, "w+")
    out.close()
    out = open(my_out, "r+")

    ps = psutil.Popen(f"java {class_name}", stdin=inp, stdout=out, stderr=PIPE)
    tim = time.time()
    fin_time = time.time() - tim
    maxmem = 0
    while True:
        try:
            maxmem = max(maxmem, getattr(ps,"memory_info")()[0] / _TWO_20)
        except psutil.NoSuchProcess:
            break
        finally:
            fin_time = time.time() - tim
            if fin_time > 4:
                tle = True
                break
    if ps.is_running():
        ps.kill()
    
    err = ps.communicate()[1].decode('utf-8')
    if err != '':
        rte = True

    out.seek(0)
    output = "\n".join([x.strip() for x in out.readlines()])
    with open(tc_dir + f"/out{str(i)}") as f:
        tcoutput = "\n".join([x.strip() for x in f])
    if difflib.SequenceMatcher(None, output, tcoutput).ratio() != 1.0:
        wa = True
        with open(f"{_HTML_DIR}/myout{str(i)}.html", "w+") as f:
            f.write(difflib.HtmlDiff().make_file(output, tcoutput))

    print(f"{'TC' + str(i):>5}: {fmt(Fore.RED,'RTE') if rte else fmt(Fore.RED,'TLE') if tle else fmt(Fore.RED,'WA') if wa else fmt(Fore.GREEN,'AC')}" + " | " \
          f"{fmt(Fore.YELLOW, f'{maxmem:>6.2f}')}MB {fmt(f'{Fore.RED if tle else Fore.YELLOW}', f'{fin_time:>5.3f}')}s" + " | " \
          f"{'DiffTable at ' + fmt(Fore.CYAN, f'/{_HTML_FOLDER}/myout{str(i)}.html') if wa and not (tle or rte) else ''}\n{err}",end="")

def fmt(color, val):
    return f"{color}{str(val)}{Style.RESET_ALL}"

def _aquit():
    os.chdir(_ROOT_DIR)
    if(os.path.exists(_TMP_DIR)):
        shutil.rmtree(_TMP_DIR)
    sys.exit()

def main():
    global src_file, tc_dir, thread
    skip = False
    parser = argparse.ArgumentParser()
    parser.add_argument("javaFile", help="Java source code file.")
    parser.add_argument("testCaseDir", help="Test Case directory. Format test case file: in<i> and out<i>. (e.g. in4 and out4)")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use.")

    if len(sys.argv) != 3:
        parser.print_help()
        return

    options = parser.parse_args()
    tc_dir = options.testCaseDir
    src_file = options.javaFile
    numthread = options.threads
    if not os.path.exists(src_file):
        print(f"Can't find {src_file}")
        return
    if not os.path.exists(tc_dir):
        print(f"Can't find {tc_dir}")
        return

    tc_dir = os.path.abspath(tc_dir) 
    src_path = os.path.abspath(src_file)
    class_name = os.path.splitext(os.path.basename(src_path))[0]

    if not os.path.exists(_TMP_DIR):
        os.makedirs(_TMP_DIR)
    if not os.path.exists(_HTML_DIR):
        os.makedirs(_HTML_DIR)

    if psutil.Popen(f"javac -d \"{_TMP_DIR}\" \"{src_path}\"").wait():
        _aquit()
    os.chdir(_TMP_DIR)

    tcs = [x.strip("in") for x in os.listdir(tc_dir) if "in" in x]
    with ThreadPoolExecutor(max_workers=numthread) as executor:
        futures = [executor.submit(judge, class_name, i) for i in tcs]
        for future in as_completed(futures):
            pass

    os.chdir("..")
    shutil.rmtree(_TMP_DIR)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        _aquit()
        