import argparse
import logging
import signal
import sys
from argparse import RawTextHelpFormatter
from multiprocessing import Manager, Pool

import requests
from natsort import natsorted  # pip install natsort
from tqdm import tqdm  # pip install tqdm

manager = Manager()
invalid_url_list = manager.list()


extension_rules = ["/?", "?ch", "?pb", "?utm", "?ad", "?wid"]


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def remove_url_extensions(s):
    s = s.replace("/www.", "/")
    s = s.replace("/m.", "/")
    s = s.replace("/es.", "/")
    s = s.replace("http:", "https:")
    return s


def remove_url_duplicates(url_list):
    return list(set(url_list))


def parse_url(url):
    # Remove whitespaces to avoid errors
    url = url.strip()

    url = url.replace("/?", "//?")

    # Remove URL additional media data
    for r in extension_rules:
        url = url.split(r, 1)[0]

    # Remove unnecessary URL extensions
    url = remove_url_extensions(url)
    return url


def validate_url(url):
    # Making a get request
    url = url.split(" (")[0]
    try:
        response = requests.get(url, timeout=10)
    except OSError:
        invalid_url_list.append(url)
    else:
        # print response
        if response.status_code == 404:
            invalid_url_list.append(url)


def get_file(fname, mode):
    try:
        open(fname, mode)  # Beware of file not closing
    except OSError:
        print("Could not open/read file:", fname)
        sys.exit()


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is not a valid value" % value)
    return ivalue


def main():
    parser = argparse.ArgumentParser(
        description="Organize your URL saved",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--saveFile", dest="saveFile", default=False, help="File with the URLs result"
    )
    parser.add_argument(
        "--readFile", dest="readFile", default=False, help="File with the URLs to add"
    )
    parser.add_argument("--url", dest="url", default=False, help="Single URL to add")
    parser.add_argument(
        "--numWorkers",
        dest="numWorkers",
        default=0,
        type=check_positive,
        help="Number of workers to use",
    )
    args = parser.parse_args()

    if args.saveFile is False:
        logging.error("No destination file specified")
        parser.print_help()
        sys.exit(-1)

    if args.readFile is False and args.url is False:
        logging.error("No source file or URL specified")
        parser.print_help()
        sys.exit(-1)

    if args.readFile:
        get_file(args.readFile, "rb")
        with open(args.readFile, encoding="utf-8") as f:
            url_list = []
            for line in f:
                new_url = parse_url(line)
                url_list.append(new_url)

    elif args.url:
        url_list = [parse_url(args.url)]
        print("The new URL is", url_list)

    get_file(args.saveFile, "r")
    with open(args.saveFile, encoding="utf-8") as f:
        # Merge the URL list
        if args.saveFile != args.readFile and args.readFile or args.url:
            aux_list = f.readlines()
            aux_list = [line.rstrip("\n") for line in aux_list]
            url_list += aux_list

        url_list = remove_url_duplicates(url_list)
        url_list = natsorted(url_list)

    if args.numWorkers > 0:
        try:
            pool = Pool(processes=args.numWorkers, initializer=init_worker)
            for _ in tqdm(
                pool.imap_unordered(validate_url, url_list), total=len(url_list)
            ):
                pass
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            pool.terminate()
            pool.join()
        else:
            pool.close()
            pool.join()

        print(
            "Found %s invalid URLs out of %s" % (len(invalid_url_list), len(url_list))
        )

        for u in invalid_url_list:
            url_list.remove(u)

        with open("invalid_urls.txt", "w") as f:
            f.writelines(line + "\n" for line in invalid_url_list)

    with open(args.saveFile, mode="w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in url_list)

    print("\n > Operation finished!\n")


if __name__ == "__main__":
    main()
