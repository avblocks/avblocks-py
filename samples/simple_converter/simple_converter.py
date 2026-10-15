#!/usr/bin/env python3
"""
Transcode a media file from H.264/AVC to H.265/HEVC.

This sample demonstrates the basic AVBlocks transcoding workflow with
hardcoded input and output file paths.
"""

import sys

from avblocks import (
    Library, MediaInfo, MediaSocket, Transcoder,
    StreamType, StreamSubType
)


def main():
    Library.initialize()

    # Set license information. To run AVBlocks in demo mode, comment the next line out
    # Library.set_license("<license-string>")

    input_file = "Wildlife_h264_aac.mp4"
    output_file = "Wildlife_h265_aac.mp4"

    with MediaInfo() as input_info:
        input_info.inputs[0].file = input_file

        if input_info.open():
            input_socket = MediaSocket.from_media_info(input_info)

            # Start with same output as the input, which is MP4 / H.264 + AAC
            output_socket = input_socket.clone()

            # Get the output video stream info
            out_video_stream = output_socket.pins[0].stream_info

            # Change the video stream type to H.265 (HEVC)
            # and the stream subtype to HEVC Annex B
            out_video_stream.stream_type = StreamType.H265
            out_video_stream.stream_sub_type = StreamSubType.HEVC_Annex_B

            # Input is H.264/AVC at 700 kbps.
            # With H.265/HEVC we can use lower bitrate, e.g. 500 kbps.
            out_video_stream.bitrate = 500000

            # Change the output file name to Wildlife_h265_aac.mp4
            output_socket.file = output_file

            # Create Transcoder and configure it with
            # the input and output sockets
            with Transcoder() as transcoder:
                transcoder.inputs.add(input_socket)
                transcoder.outputs.add(output_socket)

                # Allow demo mode for the transcoder when
                # using the demo version of the library
                transcoder.allow_demo_mode = True

                # Run the transcoder
                if transcoder.open():
                    transcoder.run()
                    transcoder.close()
                else:
                    print(f"transcoder.open() failed: {transcoder.error.message}", file=sys.stderr)
        else:
            print(f"input_info.open() failed: {input_info.error.message}", file=sys.stderr)

    Library.shutdown()
    return 0


if __name__ == '__main__':
    sys.exit(main())
