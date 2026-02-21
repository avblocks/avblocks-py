#!/usr/bin/env python3
"""
Decode AAC ADTS file to WAV using pull mode.

This sample decodes an AAC ADTS audio file to a WAV file using the pull mode 
(manually pulling decoded PCM samples and writing to output).
"""

import os
import sys
import click

from avblocks import (
    Library, Transcoder, MediaSocket, MediaPin,
    AudioStreamInfo, MediaSample, StreamType, 
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


def create_decoder_output_socket() -> MediaSocket:
    """Create output socket for decoder (LPCM output)."""
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


def create_wav_writer(output_file: str) -> Transcoder:
    """Create transcoder for writing WAV file."""
    # Input stream info, pin and socket
    infmt = AudioStreamInfo()
    infmt.stream_type = StreamType.LPCM
    infmt.channels = 2
    infmt.sample_rate = 48000
    infmt.bits_per_sample = 16
    
    in_pin = MediaPin()
    in_pin.stream_info = infmt
    
    in_socket = MediaSocket()
    in_socket.stream_type = StreamType.LPCM
    in_socket.pins.add(in_pin)
    
    # Output stream info, pin and socket
    outfmt = AudioStreamInfo()
    outfmt.stream_type = StreamType.LPCM
    outfmt.channels = 2
    outfmt.sample_rate = 48000
    outfmt.bits_per_sample = 16
    
    out_pin = MediaPin()
    out_pin.stream_info = outfmt
    
    out_socket = MediaSocket()
    out_socket.stream_type = StreamType.WAVE
    out_socket.pins.add(out_pin)
    out_socket.file = output_file
    
    # Create transcoder
    wav_writer = Transcoder()
    wav_writer.allow_demo_mode = True
    wav_writer.inputs.add(in_socket)
    wav_writer.outputs.add(out_socket)
    
    return wav_writer


def decode(input_file: str, output_file: str) -> bool:
    """Decode AAC ADTS file to WAV using pull mode."""
    # Transcoder will fail if output exists (by design)
    delete_file(output_file)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create decoder transcoder
    with Transcoder() as decoder:
        decoder.allow_demo_mode = True
        
        input_socket = MediaSocket()
        input_socket.file = input_file
        decoder.inputs.add(input_socket)
        decoder.outputs.add(create_decoder_output_socket())
        
        if not decoder.open():
            print_error("Decoder open", decoder.error)
            return False
        
        # Create WAV writer transcoder
        wav_writer = create_wav_writer(output_file)
        
        if not wav_writer.open():
            print_error("WAV Writer open", wav_writer.error)
            decoder.close()
            return False
        
        # Pull-push decoding loop
        pcm_sample = MediaSample()
        decoder_eos = False
        
        while not decoder_eos:
            # Pull PCM sample from decoder
            res, _ = decoder.pull(pcm_sample)
            
            if res:
                # Push PCM sample to WAV writer
                if not wav_writer.push(0, pcm_sample):
                    print_error("WAV Writer push", wav_writer.error)
                    decoder.close()
                    wav_writer.close()
                    return False
                continue
            
            # No more PCM data from decoder
            error = decoder.error
            if error.facility == ErrorFacility.Codec and error.code == CodecError.EOS:
                # Push None to signal EOS to WAV writer
                wav_writer.push(0, None)
                decoder_eos = True
                continue
            
            # Decoder error
            print_error("Decoder pull", error)
            decoder.close()
            wav_writer.close()
            return False
        
        wav_writer.close()
        decoder.close()
    
    print("Decoding completed successfully.")
    return True


@click.command()
@click.option('-i', '--input', 'input_file', 
              help='Input AAC file',
              type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file',
              help='Output WAV file',
              type=click.Path())
def main(input_file: str, output_file: str):
    """Decode AAC ADTS file to WAV using pull mode."""
    
    # Set default options if not provided
    if not input_file or not output_file:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        if not input_file:
            input_file = os.path.join(script_dir, "../../assets/aud/Hydrate-Kenny_Beltrey.adts.aac")
        if not output_file:
            output_file = os.path.join(script_dir, "../../output/dec_aac_adts_pull/Hydrate-Kenny_Beltrey.wav")
        
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
    
    result = decode(input_file, output_file)
    
    Library.shutdown()
    
    sys.exit(0 if result else 2)


if __name__ == '__main__':
    main()
