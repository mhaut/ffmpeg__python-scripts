# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │              Download a video or file to use in the scriptflow                 │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯

import os
import sys
import argparse
import subprocess
import datetime


def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-i', '--input',   type=str,  required=True,  help='The input url to download.')
    parser.add_argument('-o', '--output',  type=str,  default="ff_download.mp4",  help='The name of the output file.')
    parser.add_argument('-s', '--start',   default="00:00:00",  type=lambda d: datetime.datetime.strptime(d, '%H:%M:%S').time(), \
                        help='When to start the cut. Format is HH:MM:SS. Default is the beginning of the video.')
    parser.add_argument('-e', '--end',     default="00:00:10",  type=lambda d: datetime.datetime.strptime(d, '%H:%M:%S').time(), \
                        help='When to finish the cut. Format is HH:MM:SS. Default is 10 seconds into the video.')

    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_download.py - Download a video/file for usage in scriptflow.")

    if "vimeo" in args.input:
        from vimeo_downloader import Vimeo
        v = Vimeo(args.input)
        s = v.streams
        try:
            s[-1].download(download_directory='./', filename=args.output)
        except:
            print("Error")
    else:
        command = ['curl', '--insecure', '--silent', '--show-error', '--url', args.input, '--output', args.output]
        print(command)

        result = subprocess.run(command)
        if result.returncode == 0:
            print("✅ {}".format(args.output))
        else:
            print("❌ Error: {}".format(args.output))


def main():
    args = get_params()
    launch_command(args)




if __name__ == '__main__':
    main()
