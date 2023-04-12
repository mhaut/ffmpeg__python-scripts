# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │              Overlay a video at specific time on the video                    │
# │              Allows for transparent videos and animations                    │
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
    parser.add_argument('-v', '--overlay',  type=str,  required=True, help='Note that you CAN use videos as the overlay. Image/Video to use for the overlay.')
    parser.add_argument('-S', '--start',    type=int,  required=True, help='Start time in seconds of when to show overlay.')
    parser.add_argument('-E', '--end',      type=int,  required=True, help='End time in seconds of when to show overlay.')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args




def launch_command(args):
    print("ff_overlay.py - Overlaying a video on top.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]


    commovie = "movie="+args.overlay+" [a];[a]setpts=PTS-STARTPTS+"+str(args.start)+"/TB[top]; [in][top] overlay=0:0:enable='between(t,"+str(args.start)+","+str(args.end)+")' [c]"
    command2 = ["-v", args.loglevel, "-i", args.input, "-vf", commovie, args.output]

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
