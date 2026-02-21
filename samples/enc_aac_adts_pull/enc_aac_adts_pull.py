#!/usr/bin/env python3
"""
Encode WAV file to AAC ADTS using pull mode.

This sample encodes a WAV audio file to AAC ADTS format using the pull mode
(manually pulling encoded samples and writing to output file).
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    AudioStreamInfo, MediaSample, StreamType, StreamSubType, 
    ErrorFacility, CodecError
)


def delete_file(filename: str):
    """Delete a file if it exists."""
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except OSError:
        pass


def print_error(action: str, error) -> None:
    """Print error information."""
    if action:
        print(f"{action}: ", end="")
    
    if error.facility == ErrorFacility.Success:
        print("Success")
        return
    
    print(f"{error.message or ''}, facility:{error.facility} code:{error.code} hint:{error.hint or ''}")


def create_output_socket() -> MediaSocket:
    """Create output socket for AAC ADTS encoding (no file)."""
    socket = MediaSocket()
    socket.stream_type = StreamType.AAC
    socket.stream_sub_type = StreamSubType.AAC_ADTS
    
    pin = MediaPin()
    socket.pins.add(pin)
    
    asi = AudioStreamInfo()
    pin.stream_info = asi
    
    asi.stream_type = StreamType.AAC
    asi.stream_sub_type = StreamSubType.AAC_ADTS
    
    # You can change the number of channels
    # asi.channels = 1
    # or the sampling rate
    # asi.sample_rate = 44100
    
    return socket


def encode(input_file: str, output_file: str) -> bool:
    """Encode WAV file to AAC ADTS using pull mode."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'wb') as outfile:
        # Create input socket
        in_socket = MediaSocket()
        in_socket.file = input_file
        
        # Create output socket (no file - we'll manually write)
        out_socket = create_output_socket()
        
        # Create transcoder
        with Transcoder() as transcoder:
            transcoder.allow_demo_mode = True
            transcoder.inputs.add(in_socket)
            transcoder.outputs.add(out_socket)
            
            if not transcoder.open():
                print_error("Transcoder open", transcoder.error)
                return False
            
            # Encode by pulling encoded samples
            sample = MediaSample()
            
            while True:
                res, _ = transcoder.pull(sample)
                if res:
                    outfile.write(bytes(sample.buffer.data))
                else:
                    break
            
            error = transcoder.error
            print_error("Transcoder pull", error)
            
            success = False
            if error.facility == ErrorFacility.Codec and error.code == CodecError.EOS:
                # ok - end of stream
                success = True
            
            transcoder.close()
            
            return success


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input WAV file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output AAC ADTS file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Encode WAV file to AAC ADTS using pull mode."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/aud/Hydrate-Kenny_Beltrey.wav")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/enc_aac_adts_pull/Hydrate-Kenny_Beltrey.aac")
        
        print("Using default options:")
        print(f"  --input {input_file}")
        print(f"  --output {output_file}")
        print()
    
    # Validate options
    print(f"--input: {input_file}")
    print(f"--output: {output_file}")
    
    Library.initialize()
    
    # Set license information. Without this AVBlocks runs in Demo mode.
    # Library.set_license("<license-string>")
    
    result = encode(input_file, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()
