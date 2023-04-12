# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │         Trim a video to it's middle part. Remove start / end equally         │
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
    parser.add_argument('-i', '--input',    type=str,  required=True, help='The name of an input file.')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-t', '--trim',     type=int,  default=1,     help='Number of seconds to remove from the start and end of video.')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args




def convert_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s)


def launch_command(args):
    print("ff_middle.py - Trimming input video equally at start and end.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]


    command2 = ['-i', args.input]
    try:
        process = subprocess.Popen(command + command2, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        output = process.communicate()[0]
        result = output.decode()
        duration_index = result.find('Duration')
        duration = result[duration_index+10:duration_index+21]
        duration = float(convert_to_seconds(duration))
    except:
        print("❌ Error reading file " + args.input)
        exit()


    offset = args.trim // 2
    print(offset)
    command2 = ["-v", args.loglevel, "-i", args.input, "-ss", str(round(offset)), "-to", str(round(duration-offset)), "-c", "copy", args.output]
    # print(command + command2)
    result = subprocess.run(command + command2)
    if result.returncode == 0:
        print("✅ {}".format(args.output))
    else:
        print("❌ Error creating file " + args.output)
        exit()






def main():
    args = get_params()
    launch_command(args)




if __name__ == '__main__':
    main()
