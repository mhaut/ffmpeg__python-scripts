# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │                        Change the video Aspect Ratio                         │
# │                                                                              │
# ╰──────────────────────────────────────────────────────────────────────────────╯
import sys
import argparse
import subprocess



def get_params():
    parser = argparse.ArgumentParser(description='FFMPEG params')
    parser.add_argument('-i', '--input',    type=str,  required=True, help='The name of an input file.')
    parser.add_argument('-o', '--output',   type=str,  required=True, help='The name of the output file.')
    parser.add_argument('-s', '--strength', type=float, default=0.5,   help='Set horizontal sigma, standard deviation of Gaussian blur (strength).')
    parser.add_argument('-t', '--steps',    type=int,  default=1,     help='Set the number of times to apply blur.')
    parser.add_argument('-C', '--config',    type=str,          default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel', type=str,          default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_blur.py - Changing the blurriness of the video.")
    command = ["ffmpeg", "-v", args.loglevel, "-i", args.input, "-vf", "gblur=sigma={}:steps={}".format(args.strength, args.steps), "-c:a", "copy", args.output]
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
