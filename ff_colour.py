# ╭──────────────────────────────────────────────────────────────────────────────╮
# │                                                                              │
# │                        Change the video Aspect Ratio                         │
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
    parser.add_argument('-b', '--brightness', type=float, default=0.0,   help='Change the brightness value from -1.0 to 1.0.')
    parser.add_argument('-c', '--contrast',   type=float, default=1.0,   help='Change the contrast value from -1000.0 to 1000.0.')
    parser.add_argument('-m', '--gamma',      type=float, default=1.0,   help='Change the gamma value from 0.1 to 10.0.')
    parser.add_argument('-s', '--saturation', type=float, default=1.0,   help='Change the saturation value from 0.0 to 3.0.')
    parser.add_argument('-w', '--weight',     type=float, default=1.0,   help='Change the gamma weight value from 0.0 to 1.0.')
    parser.add_argument('-C', '--config',      type=str,  default="",             help='Supply a config.json file with settings instead of command-line. Requires JQ installed.')
    parser.add_argument('-l', '--loglevel',   type=str,  default="error",        help='The FFMPEG loglevel to use. Default is "error" only.', \
                                                                                            choices=["quiet", "panic", "fatal", "error", "warning", "info", "verbose", "debug", "trace"])
    parser.add_argument('-ud', '--use_docker', action='store_true', help='Use FFMPEG from docker container')
    args = parser.parse_args()
    return args



def launch_command(args):
    print("ff_colour.py - Changing the colour of the video.")
    if args.use_docker:
        # https://docs.docker.com/engine/install/linux-postinstall/
        # https://hub.docker.com/r/jrottenberg/ffmpeg/
        command = ["docker", "run", "-it", "-v", os.getcwd()+":"+os.getcwd(), '-w', os.getcwd(), "jrottenberg/ffmpeg"]
    else:
        command = ["ffmpeg"]
    eq = "eq=brightness="+str(args.brightness)+":contrast="+str(args.contrast)+":gamma="+str(args.gamma)+":saturation="+str(args.saturation)+":gamma_weight="+str(args.weight)
    command += ["-v", args.loglevel, "-i", args.input, "-vf", eq, "-c:a", "copy", args.output]

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
