# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │      Change the video FPS (Frames per second) without changing the time      │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯
import os
import sys
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-i', '--input',    type=str,  required=True, help='The name of an input file.')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-f', '--fps',      type=int,  default=30,    help='The frames per second the video should be converted to. \
                                                                        The default value is 30. The length of the video will not change, but frames will either be added or removed')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args




def launch_command(args):
    print("ff_fps.py - Changing the FPS of video.")

    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]

    command += ["-v", args.loglevel, '-i', args.input, '-vf', 'fps='+str(args.fps), args.output]
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
