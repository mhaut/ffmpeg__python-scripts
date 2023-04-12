# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │                      Apply a 3DL LUT file to the video.                       │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯
# https://freshluts.com/luts/408

import os
import sys
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('-i', '--input',    type=str,  required=True, help='The name of an input file.')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-t', '--lut',      type=str,  required=True, help='The Look-Up-Table (LUT) should be in a 3DL/Cube format.')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_lut.py - LUT File being applied to video.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]

    command += ["-y", "-v", args.loglevel, "-i", args.input, "-vf", "lut3d=file=" + args.lut, "-c:a", "copy", args.output]
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
