# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │                                Crop the video                                │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯

import os
import sys
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('-i', '--input',   type=str,  required=True,  help='The name of an input file.')
    parser.add_argument('-o', '--output',  type=str,  required=True,  help='The name of the output file.')
    parser.add_argument('-w', '--width',   type=float, default=300.0,  help='Width of the output video. Default: 300px.')
    parser.add_argument('-h', '--height',  type=float, default=300.0,  help='Height of the output video. Default: 300px.')
    parser.add_argument('-x', '--xpixels', type=float, default=-1,  help='Where to position the video in the frame on X-Axis from left. Default center: (iw-ow)/2')
    parser.add_argument('-y', '--ypixels', type=float, default=-1,  help='Where to position the video in the frame on Y-Axis from top. Default center: (ih-oh)/2')

    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_convert.py - Converting MOV to MP4.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]


    if args.xpixels == -1:   args.xpixels = "(iw-ow)/2"
    elif args.ypixels == -1: args.ypixels = "(ih-oh)/2"

    command += ["-v", args.loglevel, '-i', args.input, '-vf', "crop=w="+str(args.width)+":h="+str(args.height)+":x="+str(args.xpixels)+":y="+str(args.ypixels), args.output]
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
