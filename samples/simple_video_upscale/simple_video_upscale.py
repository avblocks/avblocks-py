#!/usr/bin/env python3
"""
Scale a 480p (854x480) video up to Full HD 1080p (1920x1080).

This sample demonstrates the basic AVBlocks video upscaling workflow with
hardcoded input and output file paths (no command line parsing).
"""

from avblocks import (
    Library, MediaInfo, MediaSocket, Transcoder,
    VideoStreamInfo, Param, InterpolationMethod, ErrorFacility
)


def print_error(action: str, error) -> None:
    """Print error information."""
    if action:
        print(f"{action}: ", end="")

    if error.facility == ErrorFacility.Success:
        print("Success")
        return

    print(f"{error.message or ''}, facility:{error.facility} code:{error.code} hint:{error.hint or ''}")


def main():
    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")

    input_path = "AndrewConnolly_2014.mp4"
    output_path = "AndrewConnolly_2014_1080p.mp4"

    try:
        with MediaInfo() as media_info:
            media_info.inputs[0].file = input_path
            if not media_info.open():
                print_error("Open MediaInfo", media_info.error)
                return

            input_socket = MediaSocket.from_media_info(media_info)

            output_socket = input_socket.clone()
            output_socket.file = output_path

            out_video_pin = output_socket.pins[0]

            out_video_stream_info = out_video_pin.stream_info
            if isinstance(out_video_stream_info, VideoStreamInfo):
                out_video_stream_info.frame_width = 1920
                out_video_stream_info.frame_height = 1080

            out_video_pin.params[Param.Video.Resize.InterpolationMethod] = int(InterpolationMethod.Cubic)

            with Transcoder() as transcoder:
                transcoder.allow_demo_mode = True

                transcoder.inputs.add(input_socket)
                transcoder.outputs.add(output_socket)

                if transcoder.open():
                    transcoder.run()
                    transcoder.close()
                else:
                    print_error("Transcoder Open", transcoder.error)
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(f"Exception: {ex}")
    finally:
        Library.shutdown()


if __name__ == '__main__':
    main()
