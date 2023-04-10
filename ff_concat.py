# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │                     Concatenate multiple files together                       │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯

import os
import sys
import glob
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-i', '--input',    type=str, nargs='+', required=True, help='The name of an input file(s) (can be a wildcard).')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_concat.py - Running video concatenation.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]

    with open('./mylist.txt', 'w') as file:
        for pattern in args.input:
            file.write("file '{}'\n".format(pattern))

    input_files = [glob.glob(pattern) for pattern in args.input]
    command += ["-v", args.loglevel,"-f", "concat", "-safe", "0", "-i", "./mylist.txt", "-c", "copy", args.output]
    print(command)

    result = subprocess.run(command)
    if result.returncode == 0:
        result = subprocess.run(["rm", "./mylist.txt"])
        if result.returncode == 0:
            print("✅ {}".format(args.output))
        else:
            print("✅ {}".format(args.output))
            print("❌ Error removing file mylist.txt")
    else:
        print("❌ Error: {}".format(args.output))


def main():
    args = get_params()
    launch_command(args)




if __name__ == '__main__':
    main()
