#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
import requests, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--include', dest = 'include', nargs = '+', default = ['.py', '.txt'])
parser.add_argument('url')
parser.add_argument('-o', help = 'Output directory', dest = 'out', default = '.')

def main(args):
    include = args.include
    base_url = args.url
    out_dir = args.out
    try:
        driver = Firefox()
        driver.get(base_url)
        a_tags = driver.find_elements_by_xpath("//a")

        for a_tag in a_tags:
            href = a_tag.get_attribute('href')
            for ext in include:
                if href.endswith(ext):
                    res = requests.get(href)
                    fname = href.split("/")[-1]
                    fpath = os.path.join(out_dir, fname)
                    with open(fpath, 'w') as wf:
                        wf.write(res.content)
    finally:
        driver.close()

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
