# -*- coding: utf-8
import os
import pdfkit
import argparse
import markdown


def md2html(mdstr):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite',
            'markdown.extensions.tables', 'markdown.extensions.toc']

    html = '''
    <html lang="zh-cn">
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="content-type" />
    <link href="markdown.css" rel="stylesheet">
    <link href="github.css" rel="stylesheet">
    </head>
    <body>
    %s
    </body>
    </html>
    '''

    ret = markdown.markdown(mdstr, extensions=exts)
    return html % ret


def do_sth(input_file, output_file, config):
    '''
        this function use markdown to change md to html
        and then use pdfkit to change html to pdf
        you need to download wkhtmltopdf first from below url:
        https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf
    '''
    tmp_html = input_file.replace('md', 'html')
    try:
        with open(input_file, 'r') as f:
            string = f.read()

        with open(tmp_html, 'w') as f:
            f.write(md2html(string))
        config = pdfkit.configuration(wkhtmltopdf=config)
        pdfkit.from_file(tmp_html, output_file, configuration=config)
        os.remove(tmp_html)
    except Exception as e:
        print(f'change to pdf err:{str(e)}')


def test_run():
    test_md = os.path.join(os.getcwd(), 'result', 'test.md')
    out_pdf = os.path.join(os.getcwd(), 'result', 'test.pdf')
    config = r"C:\Program Files\wkhtmltox\bin\wkhtmltopdf.exe"
    do_sth(test_md, out_pdf, config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="run", description="markdown to pdf")
    parser.add_argument("input", help="markdown location")
    parser.add_argument("output", help="pdf location")
    parser.add_argument("config", help="the location of the wkhtmltopdf.exe")
    parser.add_argument("test", help="test mode", choices=['1', '0'])
    args = parser.parse_args()

    if int(args.test):
        test_run()
    else:
        infile, outfile, config = args.input, args.output, args.config
        do_sth(infile, outfile, config)
