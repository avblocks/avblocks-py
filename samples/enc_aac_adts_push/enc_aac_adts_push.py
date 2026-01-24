#!/usr/bin/env python3
"""
Encode WAV file to AAC ADTS using push mode.

This sample encodes a WAV audio file to AAC ADTS format using the push mode.
It first decodes the WAV file to PCM samples using a "reader" transcoder,
then pushes those PCM samples to an "encoder" transcoder.
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


def create_input_socket() -> MediaSocket:
    """Create input socket for raw PCM data."""
    socket = MediaSocket()
    socket.stream_type = StreamType.LPCM
    
    pin = MediaPin()
    asi = AudioStreamInfo()
    asi.stream_type = StreamType.LPCM
    asi.channels = 2
    asi.sample_rate = 48000
    asi.bits_per_sample = 16
    
    pin.stream_info = asi
    socket.pins.add(pin)
    
    return socket


def create_output_socket(output_file: str) -> MediaSocket:
    """Create output socket for AAC ADTS file."""
    socket = MediaSocket()
    socket.stream_type = StreamType.AAC
    socket.stream_sub_type = StreamSubType.AAC_ADTS
    socket.file = output_file
    
    pin = MediaPin()
    asi = AudioStreamInfo()
    asi.stream_type = StreamType.AAC
    asi.stream_sub_type = StreamSubType.AAC_ADTS
    
    # You can change the sampling rate and the number of the channels
    # asi.channels = 1
    # asi.sample_rate = 44100
    
    pin.stream_info = asi
    socket.pins.add(pin)
    
    return socket


def create_wav_reader(input_file: str) -> Transcoder:
    """Create transcoder for reading WAV file and outputting raw PCM."""
    # Input socket - it will automatically detect stream info from the file
    wav_input_socket = MediaSocket()
    wav_input_socket.file = input_file
    
    # Output stream info
    pcm_asi = AudioStreamInfo()
    pcm_asi.stream_type = StreamType.LPCM
    pcm_asi.channels = 2
    pcm_asi.sample_rate = 48000
    pcm_asi.bits_per_sample = 16
    
    # Output pin
    pcm_pin = MediaPin()
    pcm_pin.stream_info = pcm_asi
    
    # Output socket - we need LPCM stream type
    pcm_output_socket = MediaSocket()
    pcm_output_socket.stream_type = StreamType.LPCM
    pcm_output_socket.pins.add(pcm_pin)
    
    # Create transcoder
    wav_reader = Transcoder()
    wav_reader.allow_demo_mode = True
    wav_reader.inputs.add(wav_input_socket)
    wav_reader.outputs.add(pcm_output_socket)
    
    return wav_reader


def encode(input_file: str, output_file: str) -> bool:
    """Encode WAV file to AAC ADTS using push mode."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create WAV reader transcoder
    wav_reader = create_wav_reader(input_file)
    
    if not wav_reader.open():
        print_error("WAV Reader open", wav_reader.error)
        return False
    
    # Create encoder transcoder
    encoder = Transcoder()
    encoder.allow_demo_mode = True
    encoder.inputs.add(create_input_socket())
    encoder.outputs.add(create_output_socket(output_file))
    
    if not encoder.open():
        print_error("Encoder open", encoder.error)
        wav_reader.close()
        return False
    
    # Pull-push encoding loop
    pcm_sample = MediaSample()
    reader_eos = False
    
    while not reader_eos:
        # Pull PCM sample from WAV reader
        res, _ = wav_reader.pull(pcm_sample)
        
        if res:
            # Push PCM sample to encoder
            if not encoder.push(0, pcm_sample):
                print_error("Encoder push", encoder.error)
                wav_reader.close()
                encoder.close()
                return False
            continue
        
        # No more PCM data from reader
        error = wav_reader.error
        if error.facility == ErrorFacility.Codec and error.code == CodecError.EOS:
            # Flush encoder
            encoder.flush()
            reader_eos = True
            continue
        
        # Reader error
        print_error("WAV Reader pull", error)
        wav_reader.close()
        encoder.close()
        return False
    
    wav_reader.close()
    encoder.close()
    
    print("Encoding completed successfully.")
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input WAV file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output AAC ADTS file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Encode WAV file to AAC ADTS using push mode."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../assets/aud/Hydrate-Kenny_Beltrey.wav")
        if not output_file:
            output_file = os.path.join(script_dir, "../output/enc_aac_adts_push/Hydrate-Kenny_Beltrey.aac")
        
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
