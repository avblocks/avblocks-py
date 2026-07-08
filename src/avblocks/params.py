"""
Parameters that can be passed to various AVBlocks components.
"""

class Param:
    """
    Defines parameters that can be passed to the transcoder and to the components that are used in the transcoding process.
    
    A parameter can be used with one or more components like decoders, encoders, demuxers, muxers, and others.
    A parameter can apply to:
    - any component
    - a certain component category like encoders, decoders, demuxers, muxers, etc.
    - a component that handles a specific format like H.264 encoder, MPEG-2 encoder, MPEG-2 muxer, etc.
    - a specific implementation of a component, or a block like PrimoCodecs H.264 encoder
    
    The value representation, range and interpretation is different for each parameter.
    """
    
    ReEncode = "REENCODE_STREAM"
    """
    Specifies whether a stream will be reencoded.
    
    This parameter is an integer.
    The supported values are defined in Use enum.
    The default value is Use.Auto.
    
    If this parameter is Use.Auto the reencoding is done only when the input and the output formats are not equivalent.
    If this parameter is Use.On the reencoding is done always even if the input and the output formats are equivalent.
    The case when this parameter is Use.Off is not implemented.
    """
    
    HardwareEncoder = "HARDWARE_ENCODER"
    """
    Specifies which hardware encoder shall be used.
    
    This parameter is an integer.
    The supported values are defined in HardwareEncoder enum.
    The default value is HardwareEncoder.Off.
    """
    
    HardwareEncoderDevice = "HARDWARE_ENCODER_DEVICE"
    """
    Specifies the device ID that shall be used for hardware encoding.
    
    This parameter is an integer.
    The device ID includes uniquely identified devices that support the hardware encoder 
    specified by the HardwareEncoder parameter.
    The default value is 0.
    """
    
    HardwareEncoderApi = "HARDWARE_ENCODER_API"
    """
    Specifies which hardware API shall be used.
    
    This parameter is an integer.
    The supported values are defined in HwApi enum.
    The default value is HwApi.None which lets AVBlocks select the hardware API.
    """
    
    class Video:
        """Parameters specific to video filters"""
        
        class FrameRateConverter:
            """Parameters specific to video frame rate filter"""
            
            Use = "VIDEO_FRAME_RATE_FILTER"
            """
            Video - Specifies whether a video frame rate filter is inserted in the processing chain.
            The filter converts the input frame rate to the output frame rate.
            
            This parameter is an integer.
            The supported values are defined in Use enum.
            The default value is Use.Auto.
            
            If this parameter is Use.Auto the frame rate conversion is done only when the
            input frame rate differs from the output frame rate.
            """
            
            RealTime = "VIDEO_FRAME_RATE_FILTER_REAL_TIME"
            """
            Video - Specifies whether a video frame rate filter is allowed to drop frames 
            when a video encoder cannot keep up with the input in realtime.
            
            This parameter is a boolean value stored as one of the following:
            bool (True/False) or integral value (1/0).
            The default value is False.
            
            If True the video frame rate filter is allowed to drop frames when a video encoder cannot keep up with the input in realtime.
            If False the video frame rate filter does not drop frames when a video encoder cannot keep up with the input in realtime.
            """
        
        class Deinterlacing:
            """Parameters specific to the video deinterlacing filter"""
            
            Method = "DEINTERLACING_METHOD"
            """
            Video - Specifies the deinterlacing method used by the deinterlacing filter.
            
            This parameter is an integer.
            The supported values are defined in the DeinterlacingMethod enum.
            The default value is DeinterlacingMethod.Blend
            """
            
            Threshold = "DEINTERLACING_THRESHOLD"
            """
            Video - Specifies the deinterlacing threshold that is used by some deinterlacing methods.
            
            The threshold is used by the DeinterlacingMethod.MedianThreshold and 
            DeinterlacingMethod.CAVT.
            
            This parameter is an integer.
            The supported values are in the range from 0 to 255.
            Zero specifies that a default threshold should be used. Each deinterlacing method may have its own default threshold value.
            """
        
        class Resize:
            """Parameters specific to the video resizing filter"""
            
            InterpolationMethod = "RESIZE_INTERPOLATION_METHOD"
            """
            Video - Specifies the interpolation method that is used for resizing video frames.
            
            This parameter is an integer.
            The supported values are defined in the InterpolationMethod enum.
            The default value is InterpolationMethod.Cubic.
            """
        
        class Overlay:
            """Parameters specific to the video overlay filter"""
            
            Mode = "OVERLAY_MODE"
            """
            Specifies an alpha compositing mode - the way a foreground overlay image is combined with the background video.
            
            This is an integer parameter. The acceptable values are defined in the AlphaCompositingMode enum.
            The default value is AlphaCompositingMode.Over (Foreground over Background), in effect, a normal painting operation.
            """
            
            LocationX = "OVERLAY_LOCATION_X"
            """
            Specifies the X coordinate of the location where the overlay is applied on the frame.
            
            This is an integer parameter.
            X increases from left to right.
            The top left point in the frame is the origin and has coordinates (0,0).
            """
            
            LocationY = "OVERLAY_LOCATION_Y"
            """
            Specifies the Y coordinate of the location where the overlay is applied on the frame.
            
            This is an integer parameter.
            Y increases from top to bottom.
            The top left point in the frame is the origin and has coordinates (0,0).
            """
            
            BackgroundAlpha = "OVERLAY_BACKGROUND_ALPHA"
            """
            Specifies the alpha value for all pixels in the background.
            
            This is a float parameter with range from 0.0 to 1.0. The default value is 1.0.
            """
            
            ForegroundBuffer = "OVERLAY_FOREGROUND_BUFFER"
            """
            Specifies the foreground that should be overlaid with the background.
            
            This is a MediaBuffer parameter.
            """
            
            ForegroundBufferFormat = "OVERLAY_FOREGROUND_BUFFER_FORMAT"
            """
            Specifies the format of the foreground buffer.
            
            This is a VideoStreamInfo parameter.
            """
            
            ForegroundAlpha = "OVERLAY_FOREGROUND_ALPHA"
            """
            Specifies the alpha value for all pixels in the foreground.
            
            This is a float parameter with range from 0.0 to 1.0.
            The default value is 1.0 which in combination with other overlay parameters 
            results in showing the foreground and hiding the background.
            """
        
        class Crop:
            """Parameters specific to video cropping"""
            
            Left = "CROP_LEFT"
            """Video - Specifies the area to be cropped inside the left edge of the input frame. (integer)"""
            
            Right = "CROP_RIGHT"
            """Video - Specifies the area to be cropped inside the right edge of the input frame. (integer)"""
            
            Top = "CROP_TOP"
            """Video - Specifies the area to be cropped inside the top edge of the input frame. (integer)"""
            
            Bottom = "CROP_BOTTOM"
            """Video - Specifies the area to be cropped inside the bottom edge of the input frame. (integer)"""
        
        class Pad:
            """Parameters specific to video padding"""
            
            Left = "PAD_LEFT"
            """Video - Specifies the area to be padded inside the left edge of the output frame. (integer)"""
            
            Right = "PAD_RIGHT"
            """Video - Specifies the area to be padded inside the right edge of the output frame. (integer)"""
            
            Top = "PAD_TOP"
            """Video - Specifies the area to be padded inside the top edge of the output frame. (integer)"""
            
            Bottom = "PAD_BOTTOM"
            """Video - Specifies the area to be padded inside the bottom edge of the output frame. (integer)"""
            
            Color = "PAD_COLOR"
            """
            Video - Specifies the padding color if any padding is set.
            
            This parameter is an integer.
            The color format is ARGB32: bits 0-7 is blue, bits 8-15 is green, bits 16-23 is red and bits 24-31 is the alpha channel.
            """
    
    class Muxer:
        """Parameters specific to muxers"""
        
        class MP4:
            """Parameters specific to MP4 muxers"""
            
            FastStart = "MUXER_MP4_FAST_START"
            """
            Run a second pass moving the moov atom before the mdat atom.
            
            Unless specified otherwise, the moov atom is normally stored at the end of the file.
            If the planned delivery method is progressive download or streaming, the moov atom will
            have to be moved to the beginning of the file.
            
            This parameter is a boolean value stored as one of the following:
            bool (True/False) or integral value (1/0).
            The default value is False.
            
            If True a second pass will reorder the atoms in the file. The atoms will be in the order: moov, mdat.
            If False the atoms in the file will be in the order: mdat, moov.
            """
            
            FastStartUseTempFile = "MUXER_MP4_FAST_START_USE_TEMP_FILE"
            """
            Specifies whether a temp file should be used during the second pass.
            
            This parameter is a boolean value stored as one of the following:
            bool (True/False) or integral value (1/0).
            The default value is False.
            
            If True a temp file will be used to reorder the atoms in the mp4 file.
            If False the atoms reordering will be done inplace.
            """
            
            FastStartTempFileDirectory = "MUXER_MP4_FAST_START_TEMP_FILE_DIRECTORY"
            """
            Specifies the temp file directory. If this parameter is not set then the system temp path will be used.
            
            This parameter type is string.
            """
    
    class Demuxer:
        """Parameters specific to demuxers"""
        
        class Mpeg:
            """Parameters specific to the Mpeg demuxer"""
            
            ProgramNumber = "DEMUXER_MPEG_PROGRAM_NUMBER"
            """
            Specifies the Program Number for which to deliver MPEG TS packets. 
            Only packets that belong to the Program with the specified Program Number will be delivered.
            The Program Number is the field that identifies the program in the Program Association Table (PAT) of a MPEG-2 TS stream.
            
            This parameter is an integer.
            """
            
            PacketId = "DEMUXER_MPEG_PACKET_ID"
            """
            Specifies the Packet ID (PID) of the MPEG TS packets to be delivered. Only packets with the specified PID will be delivered.
            The Packet ID is used to identify Program Specific Info packets, such as PAT, CAT, PMT packets, or elementary stream packets in MPEG-2 TS stream.
            
            This parameter is an integer.
            """
    
    class Decoder:
        """Parameters specific to decoders"""
        
        Config = "DECODER_CONFIG"
        """
        Decoder configuration data.
        
        This parameter is a MediaBuffer object.
        """
        
        class Video:
            """Parameters specific to video decoders"""
            
            ConcealDefects = "DECODER_VIDEO_CONCEAL_DEFECTS"
            """
            Video - Specifies whether to conceal bitstream defects and errors.
            
            This parameter is a boolean value stored as one of the following:
            bool (True/False) or integral value (1/0).
            The default value is True.
            
            If True non-fatal bitstream errors are concealed.
            If False any bitstream error is reported.
            """
            
            class H264:
                """Parameters specific to H.264 decoders"""
                
                class VUI:
                    """
                    Parameters that are part of the Video Usability Information in the H.264 stream.
                    These parameters can aid decoding but a conformant decoder is not required to process them.
                    """
                    
                    MaxDecFrameBuffering = "DECODER_H264_MAX_DEC_FRAME_BUFFERING"
                    """
                    H264 Video: Specifies the requested size of the Decoded Picture Buffer.
                    This parameter can be used to achieve low latency decoding.
                    
                    This parameter is an integer (0-1).
                    
                    A typical usage of this parameter is to set it to 1 or 0.
                    In this case the number of decoding threads is implicitly limited to 1.
                    
                    Zero latency is possible only with progressive streams with no B-frames.
                    The decoder attempts to detect cases when this parameter can break decoding and may adjust it.
                    However it's still possible that certain streams may not decode properly when this setting is too low.
                    """
    
    class Encoder:
        """Parameters specific to encoders"""
        
        class Audio:
            """Parameters specific to audio encoders"""
            
            class MPEG1:
                """Parameters specific to MPEG1 audio encoders"""
                
                ForceV1 = "ENCODER_MPEGAUDIO_FORCE_V1"
                """
                MPEG Audio: Forces MPEG audio to version 1.
                
                This parameter is a boolean value stored as one of the following:
                bool (True/False) or integral value (1/0).
                The default value is False.
                """
                
                StereoMode = "ENCODER_MPEGAUDIO_STEREOMODE"
                """
                MPEG Audio: Specifies the stereo mode.
                
                This parameter is an integer.
                The supported values are defined in StereoMode enum.
                The default value is StereoMode.LR.
                """
            
            class AAC:
                """Parameters specific to AAC audio encoders"""
                
                StereoMode = "ENCODER_AAC_STEREOMODE"
                """
                AAC Audio: Specifies the stereo mode.
                
                This parameter is an integer.
                The supported values are defined in StereoMode enum.
                The default value is StereoMode.LR.
                """
            
            class Vorbis:
                """Parameters specific to Vorbis audio encoders"""
                
                Quality = "ENCODER_VORBIS_QUALITY"
                """
                Vorbis Audio: Specifies the quality of the compressed audio.
                
                This parameter is a floating point value.
                Supported values: from 0.0 (worst quality) to 1.0 (best quality).
                The default value is 0.4.
                """
            
            class WMA:
                """Parameters specific to WMA audio encoders"""
                
                Quality = "ENCODER_WMA_QUALITY"
                """
                Windows Media Audio: Specifies the quality of the compressed audio.
                
                This parameter is an integer.
                Supported values: from 1 (worst quality) to 100 (best quality).
                The default value is 50.
                
                This parameter is used by the Transcoder only when the encoded bitrate mode is
                BitrateMode.VBR, otherwise it is ignored.
                """
            
            class G711:
                """Parameters specific to G.711 audio encoders"""
                
                EnableVAD = "ENCODER_G711_ENABLE_VAD"
                """
                G.711 Audio: Enables Voice Activity Detection (VAD).
                
                This parameter is a boolean value stored as one of the following:
                bool (True/False) or integral value (1/0).
                The default value is False.
                """
        
        class Video:
            """Parameters specific to video encoders"""
            
            class MPEG2:
                """Parameters specific to MPEG-1 and MPEG-2 video encoders"""
                
                GOPSize = "ENCODER_MPEG2VIDEO_GOPSIZE"
                """
                MPEG-1 and MPEG-2 Video: Size of the Group of Pictures (GOP, N).
                
                This parameter is an integer.
                
                The integer value is the distance between two I-pictures (full images).
                The minimum value is 1 which means the stream will contain only I-pictures.
                The maximum value for MPEG-1 is 132.
                
                The default value is 15.
                """
                
                IPDistance = "ENCODER_MPEG2VIDEO_IPDISTANCE"
                """
                MPEG-1 and MPEG-2 Video: Distance between successive reference pictures (GOP, M).
                
                This parameter is an integer.
                
                The integer value is the distance between 2 successive reference pictures: 
                I-I, I-P, P-I or P-P.
                The minimum value is 1 which means that the stream will contain I and P pictures but no B-pictures.
                
                If IPDistance is equal to GOPSize and is greater than 1
                then the stream will contain only I and B pictures, but no P-pictures.
                
                The default value is 3.
                """
                
                VBVBufferSize = "ENCODER_MPEG2VIDEO_VBV_BUFFER_SIZE"
                """
                MPEG-1 and MPEG-2 Video: Size of the internal VBV buffer in units of 16384 bits.
                
                This parameter is an integer.
                
                The default value is 20 for MPEG-1 and 112 for MPEG-2.
                
                A value of 0 means to use the encoder default setting.
                """
            
            class H264:
                """Parameters specific to H.264 encoders"""
                
                Profile = "ENCODER_H264_PROFILE_IDC"
                """
                H.264 Video: Encoding profile.
                
                This parameter is an integer.
                The supported values are defined in H264Profile enum.
                The default value is H264Profile.High.
                
                Sets the value of the profile_idc syntax element.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                EntropyCodingMode = "ENCODER_H264_ENTROPY_CODING_MODE"
                """
                H.264 Video: Entropy coding mode.
                
                This parameter is an integer.
                The supported values are defined in H264EntropyCodingMode enum.
                The default value is H264EntropyCodingMode.CABAC.
                
                CABAC compresses data more efficiently (10-20% typically) than CAVLC but requires considerably more processing to decode.
                CABAC is supported at Main, High, High10, High422 and High444. CABAC is not supported at Baseline profile.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                NumBFrames = "ENCODER_H264_NUM_B_FRAMES"
                """
                H.264 Video: Number of B-frames between consequent I-frames or P-frames.
                
                This parameter is an integer.
                The integer value must be a number that is greater than or equal to zero.
                The default value is 0.
                
                B-frames are supported at Main, High, High10, High422 and High444. B frames are not supported at Baseline profile.
                
                H.264 stream without B frames looks like: IPPPPPPP...PI...
                H.264 stream with B frames (NumBFrames 2) looks like: IBBPBBPBBP...PI
                
                The main advantage of the usage of B frames is coding efficiency. In most cases, B frames will result in less bits being coded overall.
                B-frames can use both previous and forward frames for data reference to get the highest amount of data compression.
                Note: Hardware encoders support: Intel QuickSync, NVIDIA NVENC.
                """
                
                TreatBFramesAsReference = "ENCODER_H264_TREAT_B_FRAMES_AS_REFERENCE"
                """
                H.264 Video: Allows B-pictures to be used as reference pictures.
                
                This parameter is a boolean value stored as one of the following:
                bool (True/False) or integral value (1/0).
                The default value is False.
                Note: Hardware encoders support: Intel QuickSync.
                """
                
                NumRefFrames = "ENCODER_H264_NUM_REF_FRAMES"
                """
                H.264 Video: Maximum number of reference pictures.
                Sets the maximum number of references stored in the Decoded Picture Buffer (DPB) for motion estimation and compensation.
                Essentially sets the syntax element num_ref_frames in the sequence parameter sets.
                
                This parameter is an integer value.
                
                The integer value must be consistent with profile/level parameters for a given frame size, 
                since they determine reference picture and buffer constraints for a decoder.
                If P-pictures are allowed, the number should be greater than 0.
                If B-pictures are allowed, the number should be greater than 1.
                Note: If NumRefFrames is 0 it is automatically determined by the encoder.
                
                The default value is 3. Supported values: from 0 to 16.
                
                This setting controls how many frames can be referenced by P- and B-Frames.
                Higher values will usually result in a more efficient compression, 
                but will also require more time for encoding.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                NumSlices = "ENCODER_H264_NUM_SLICES"
                """
                H.264 Video: Number of slices per frame/field.
                
                This parameter is an integer value.
                A frame/field is divided into equal parts except for the last one that can be shorter.
                The number cannot exceed the number of macro blocks per frame/field.
                The default value is 0 (auto).
                Note: Hardware encoders support: Intel QuickSync, NVIDIA NVENC.
                """
                
                Level = "ENCODER_H264_LEVEL_IDC"
                """
                H.264 Video: Computation level.
                Set the value of the level_idc syntax element.
                
                This parameter is an integer value.
                A level designated as x.y is expressed as an xy integer.
                For example level 1 is expressed as 10, level 1.1 as 11 and so on.
                The level must be in accordance with the H.264 standard.
                It must correspond to the number of reference frames and frame size.
                A value of 0 specifies automatic level computation.
                The default value is 0 (auto).
                
                Note: Similar with the Profile, Level specifies the capabilities a decoder must fulfill to decode a bitstream of a certain level.
                Most level restrictions are driven by memory restrictions and set restrictions such as resolution supported, maximum number of references, frame rate etc.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                DeblockingFilter = "ENCODER_H264_DEBLOCKING_FILTER_IDC"
                """
                H.264 Video: De-blocking filter mode.
                
                The supported values are defined in H264DeblockingFilter enum.
                The default value is H264DeblockingFilter.All.
                
                The in-loop deblocking filter helps prevent the blocking artifacts common to other DCT-based image compression techniques, 
                resulting in better visual appearance and compression efficiency
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                DeblockingFilterAlpha = "ENCODER_H264_DEBLOCKING_FILTER_ALPHA"
                """
                H.264 Video: De-blocking filter strength.
                
                This parameter is an integer value.
                Supported values range from -6 to 6.
                Negative values give a more sharp video, but they also increases the danger of visible block artifacts.
                In contrast positive values result in a smoother video, but they will also remove more details.
                The default value is 0.
                Note: Hardware encoders support: AMD VCE.
                """
                
                DeblockingFilterBeta = "ENCODER_H264_DEBLOCKING_FILTER_BETA"
                """
                H.264 Video: De-blocking filter threshold.
                
                This parameter is an integer value.
                
                The parameter controls the threshold for block detection.
                
                Supported values range from -6 to 6.
                Negative values "save" more details, but more blocks might slip through (especially in flat areas).
                In contrast positive values will remove more details and catch more blocks.
                The default value is 0 and usually it's enough to detect all blocks.
                Note: Hardware encoders support: AMD VCE.
                """
                
                Transform8x8 = "ENCODER_H264_TRANSFORM8X8"
                """
                H.264 Video: Enables 8x8 transform block size.
                
                This parameter is a boolean value expressed as an integer (1|0).
                
                Supported modes are:
                0 - Disabled. Only 4x4 transforms are used.
                1 - Enabled. Allows the additional use of 8x8 transform.
                
                The default is Enabled (1).
                
                Transform 8x8 improves the visual quality at a minor speed cost.
                Transform 8x8 is supported at High, High10, High422 and High444. 8x8 transform is not supported at Main and Baseline profiles.
                Note: Hardware encoders support: NVIDIA NVENC.
                """
                
                DirectPredMode = "ENCODER_H264_DIRECT_PRED_MODE"
                """
                H.264 Video: Direct prediction mode.
                Sets the value of the syntax element direct_spatial_mv_pred_flag.
                
                This parameter is an integer.
                The supported values are defined in H264DirectPredMode enum.
                The default value is H264DirectPredMode.Temporal.
                Note: Hardware encoders support: None.
                """
                
                QualitySpeed = "ENCODER_H264_QUALITY_SPEED"
                """
                H.264 Video: Quality/Speed trade off.
                
                This parameter is an integer value.
                Supported values range from 0 to 6 where 0 means max speed and 6 means max quality.
                The default value is 0.
                Note: Hardware encoders support: Intel QuickSync.
                """
                
                MERangeSearchX = "ENCODER_H264_ME_RANGE_SEARCH_X"
                """
                H.264 Video: Specifies how far motion estimation should be done in a horizontal direction.
                
                This parameter is an integer value.
                The default value is 8.
                Note: Hardware encoders support: AMD VCE.
                """
                
                MERangeSearchY = "ENCODER_H264_ME_RANGE_SEARCH_Y"
                """
                H.264 Video: Specifies how far motion estimation should be done in a vertical direction.
                
                This parameter is an integer value.
                The default value is 8.
                Note: Hardware encoders support: AMD VCE.
                """
                
                MESplitMode = "ENCODER_H264_ME_SPLIT_MODE"
                """
                H.264 Video: Specifies the block size for which motion estimation should be done.
                
                This parameter is an integer.
                The supported values are defined in MESplitMode enum.
                The default value is MESplitMode.Only16x16.
                Note: Hardware encoders support: None.
                """
                
                MEMethod = "ENCODER_H264_ME_METHOD"
                """
                H.264 Video: Motion estimation method.
                
                This parameter is an integer.
                The supported values are defined in MEMethod enum.
                The default value is MEMethod.Log.
                Note: Hardware encoders support: None.
                """
                
                PictureCodingType = "ENCODER_H264_PIC_CODING_TYPE"
                """
                H.264 Video: Picture coding type.
                
                This parameter is an integer.
                The supported values are defined in PictureCodingType enum.
                The default value is PictureCodingType.Frames.
                Note: Hardware encoders support: None.
                """
                
                RateControlMethod = "ENCODER_H264_RATE_CONTROL_METHOD"
                """
                H.264 Video: Rate control method.
                
                This parameter is an integer.
                The supported values are defined in RateControlMethod enum.
                The default value is RateControlMethod.ABR.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                RateControlQuantI = "ENCODER_H264_RATE_CONTROL_QUANT_I"
                """
                H.264 Video: Rate control quantizer for I slices.
                Used only when RateControlMethod is set to Constant Quantization.
                
                This parameter is an integer.
                Supported values range: from 0 to 51. The default value is 20.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                RateControlQuantP = "ENCODER_H264_RATE_CONTROL_QUANT_P"
                """
                H.264 Video: Rate control quantizer for P slices.
                Used only when RateControlMethod is set to Constant Quantization.
                
                This parameter is an integer.
                Supported values range: from 0 to 51. The default value is 20.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                RateControlQuantB = "ENCODER_H264_RATE_CONTROL_QUANT_B"
                """
                H.264 Video: Rate control quantizer for B slices.
                Used only when RateControlMethod is set to Constant Quantization.
                
                This parameter is an integer.
                Supported values range: from 0 to 51. The default value is 20.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                KeyFrameInterval = "ENCODER_H264_KEY_FRAME_INTERVAL"
                """
                H.264 Video: Distance between two sequential I-pictures.
                
                This parameter is an integer value.
                Must be greater than or equal to 0. Both 0 and 1 mean that every picture is coded as I-picture.
                The default value is 250.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE, NVIDIA NVENC.
                """
                
                KeyFrameIDRInterval = "ENCODER_H264_KEY_FRAME_IDR_INTERVAL"
                """
                H.264 Video: Distance between two sequential IDR-pictures in terms of I pictures. IDR stands for Instantaneous Decoding Refresh.
                
                This parameter is an integer value.
                It must be greater or equal to 0.
                
                For example if this parameter is 10 then every tenth I-picture is also an IDR-picture.
                
                An IDR picture is a special kind of I frame used in an H.264 stream.
                Pictures following an IDR-picture may not refer back to pictures preceding the IDR-picture.
                IDR-pictures can be used to create H.264 streams which are more easily edited.
                The default value is 1.
                Note: Hardware encoders support: Intel QuickSync, AMD VCE.
                """
                
                AccessUnitDelimiters = "ENCODER_H264_ACCESS_UNIT_DELIMITERS"
                """
                H.264 Video: Use access unit delimiters.
                
                This parameter is a boolean value stored as one of the following:
                bool (True/False) or integral value (1/0).
                The default value is False.
                Note: Hardware encoders support: Intel QuickSync, NVIDIA NVENC.
                """
                
                FixedFramerate = "ENCODER_H264_FIXED_FRAMERATE"
                """
                H.264 Video: Write timing info with a fixed frame rate in the bitstream.
                
                This parameter is a boolean value expressed as an integer (1|0).
                
                The default value is True (1).
                
                The timing info is written in the bitstream only when this parameter is True and a positive frame rate is specified.
                Note: Hardware encoders support: Intel QuickSync.
                """
            
            class H265:
                """Parameters specific to H.265/HEVC video encoders"""
                
                Profile = "ENCODER_H265_PROFILE_IDC"
                """
                H.265 encoding profile.
                
                This parameter is an integer.
                
                The supported values are defined in the H265Profile enum.
                The default value is H265Profile.Main.
                
                Supported profiles: Main, Main10
                Sets the value of the profile_idc syntax element.
                """
                
                Level = "ENCODER_H265_LEVEL_IDC"
                """
                H.265 computation level.
                
                This parameter is an integer.
                
                Sets the value of the level_idc syntax element.
                
                The default value is H265Level.None (level is selected automatically).
                Note: Similar with the Profile, Level specifies the capabilities a decoder must fulfill to decode a bitstream of a certain level.
                Most level restrictions are driven by memory restrictions and set restrictions such as resolution supported, maximum number of references, frame rate etc.
                """
                
                Tier = "ENCODER_H265_TIER"
                """
                H.265 Video: Bitrate tier.
                
                The supported values are defined in the H265Tier enum.
                The default value is H265Tier.Main
                
                The High tier specifies higher bitrate than the Main tier.
                The High tier is not supported under level 4.
                """
                
                GOPLength = "ENCODER_H265_GOP_LENGTH"
                """
                H.265 Group of Pictures (GOP) size.
                
                This parameter is an integer.
                
                The integer value is the distance between two I-pictures.
                If 1 then stream will contain only I-pictures.
                If 0 then there will be no I-pictures in the stream after the first picture.
                
                The default value is 0.
                """
            
            class VP8:
                """Parameters specific to VP8 video encoders"""
                
                KeyFrameMaxDistance = "ENCODER_VP8_KEY_FRAME_MAX_DISTANCE"
                """
                VP8 Video: Max keyframe distance.
                
                This parameter is an integer.
                
                This value, expressed as a number of frames, forces the encoder to code
                a keyframe if one has not been coded in the last KeyFrameMaxDistance frames.
                
                A value of 0 implies all frames will be keyframes. Set keyframe KeyFrameMinDistance
                equal to KeyFrameMaxDistance for a fixed interval.
                
                The default value is 100.
                """
                
                KeyFrameMinDistance = "ENCODER_VP8_KEY_FRAME_MIN_DISTANCE"
                """
                VP8 Video: Min keyframe distance.
                
                This parameter is an integer.
                
                This value, expressed as a number of frames, prevents the encoder from
                placing a keyframe nearer than KeyFrameMinDistance to the previous keyframe.
                
                At least KeyFrameMinDistance frames non-keyframes will be coded before the next
                keyframe. Set KeyFrameMinDistance equal to KeyFrameMaxDistance for a fixed interval.
                
                The default value is 0.
                """
