"""
Constants and Enumerations used in AVBlocks.
"""

from enum import IntFlag, IntEnum

class LicenseStatusFlags(IntFlag):
    """Defines the AVBlocks license status.
    
    When a license is set it may take some time until the license is resolved by the library.
    """
    
    Ready = 0
    """The licensed state is permanent. It can be changed only by calling Library.set_license.
    
    Note: The Ready status does not imply that the library or any component is successfully licensed.
    """
    
    ValidationInProgress = 1
    """The license is being validated and the current licensed state in AVBlocks is temporary."""
    
    DemoBuild = 2
    """This is a Demo build of AVBlocks. The library cannot be licensed and always operates in Demo mode."""


class ErrorFacility(IntEnum):
    """Describes the AVBlocks facilities that could generate errors.
    
    Each facility represents either an external component or a component implemented by AVBlocks.
    
    Note: Often error codes will have the same value, but different meaning depending on the facility that generated the error.
    """
    
    Success = 0
    """Not a facility. This is a special value that indicates a successful operation."""
    
    SystemWindows = 1
    """Windows System Error"""
    
    SystemMacOSStatus = 2
    """MacOS Status (Mac)"""
    
    SystemMacMach = 3
    """Mach Error (Mac)"""
    
    SystemPosix = 4
    """POSIX Error (Linux, Mac)"""
    
    AVBlocks = 5
    """AVBlocks API error. The error code is a value from the AVBlocksError enum."""
    
    Transcoder = 6
    """Transcoder error. The error code is a value from the TranscoderError enum."""
    
    Codec = 9
    """Codec error. The error code is a value from the CodecError enum."""


class AVBlocksError(IntEnum):
    """Defines API usage errors.
    
    These errors are raised when the AVBlocks API is used incorrectly.
    """
    
    UnlicensedFeature = 9
    """A required feature (codec/format) is not licensed and demo mode is not enabled."""
    
    LibraryNotInitialized = 10
    """Library is not initialized."""


class TranscoderError(IntEnum):
    """Defines Transcoder specific errors.
    
    The Transcoder may also return errors like AVBlocksError, CodecError and others.
    """
    
    NoChain = 1
    """The transcoder could not build a processing chain based on its inputs and outputs.
    Either the transcoder inputs and outputs are not configured properly or they are not compatible with each other.
    This error is returned by Transcoder.open."""
    
    UndefinedSocketType = 2
    """The stream type of a MediaSocket is not defined.
    When a media socket describes a file, the stream type is deduced from the file extension.
    When a media socket describes a stream the stream type must be set explicitly.
    This error is returned by Transcoder.open."""
    
    UnsupportedInterlacedConversion = 3
    """It is not possible to convert from progressive to interlaced video.
    Also it is not possible to switch interlace type from top-first to bottom-first or vice versa.
    This error is returned by Transcoder.open."""
    
    NoCodec = 4
    """A required encoder or decoder is not available."""
    
    UnsupportedVideoConversion = 5
    """It is not possible to convert from one uncompressed video format to another."""
    
    InputFull = 6
    """Cannot accept more input through Transcoder.push. Call Transcoder.pull to obtain output samples."""
    
    InputNeeded = 7
    """Cannot return output through Transcoder.pull. Call Transcoder.push to provide input samples."""


class CodecError(IntEnum):
    """Common errors for encoders, decoders, muxers, demuxers and other A/V components."""
    
    Init = 1
    """Failed to initialize or open a codec."""
    
    NoConfigData = 2
    """Decoder config data is required, but missing."""
    
    NoOutput = 3
    """No output has been generated."""
    
    OutputBufferNotEnough = 4
    """The output buffer is not big enough for the generated output data."""
    
    Unsupported = 5
    """Unsupported format or operation."""
    
    Failed = 6
    """The operation failed for unknown reason."""
    
    NotInitialized = 7
    """The operation cannot be completed because the component is not initialized."""
    
    Null = 8
    """One or more of the input parameters are null but are expected to be valid pointers/references."""
    
    EOS = 9
    """End of stream; no more data."""
    
    Alloc = 10
    """Failed to allocate memory."""
    
    InvalidStream = 11
    """Invalid bitstream."""
    
    NotImplemented = 12
    """The operation is not implemented yet."""
    
    InvalidParams = 13
    """At least one of the input parameters has an invalid value for the specified operation.
    Check ErrorInfo.hint for details."""
    
    InvalidOperation = 14
    """The operation is not allowed.
    Check ErrorInfo.hint for details."""
    
    MissingDependency = 15
    """A required library/dependency is not present.
    Check ErrorInfo.hint for details."""
    
    StreamOpen = 16
    """Could not open a user stream."""
    
    StreamRead = 17
    """Could not read from a user stream."""
    
    StreamWrite = 18
    """Could not write to a user stream."""
    
    StreamSeek = 19
    """Could not seek in a user stream."""
    
    BufferFull = 20
    """One of the input/output buffers is full and cannot accept more data."""
    
    MissingHardwareIntelQuickSync = 21
    """Intel QuickSync Video hardware not found."""
    
    MissingHardwareAmdVce = 22
    """AMD VCE hardware not found."""
    
    MissingHardwareNvidiaNVENC = 23
    """NVIDIA NVENC hardware not found."""


class StreamType(IntEnum):
    """Defines major audio and video stream types, and file formats (a.k.a. containers)."""
    
    Unknown = 0
    """The stream type is not defined or is unknown."""
    
    BEGIN_AUDIO = 0x1000
    """This constant marks the start of audio elementary streams. It is not a valid stream type on its own."""
    
    LPCM = 0x1001
    """Audio encoded using pulse code modulation (PCM) with linear quantization."""
    
    ALAW_PCM = 0x1002
    """A-law PCM."""
    
    MULAW_PCM = 0x1003
    """Mu-law PCM."""
    
    VIDEO_DVD_PCM = 0x1004
    """LPCM with specific sample packing for Video-DVD."""
    
    AC3 = 0x1005
    """Dolby Digital Audio (a.k.a. AC-3). AC-3 is defined in ATSC A/52-A and A/52-B."""
    
    DTS = 0x1006
    """DTS (Digital Theater Systems) Coherent Acoustics codec, transportable through S/PDIF and used on DVDs, CD-DAs, LDs, and in wave files."""
    
    MPEG_Audio = 0x1007
    """MPEG-1 or MPEG-2 Audio, Layer I, II and III."""
    
    Vorbis = 0x1008
    """Vorbis Audio Codec. This is an open standard audio codec developed by the Xiph.Org Foundation."""
    
    AAC = 0x1009
    """Advanced Audio Coding.
    Initially it was defined in Part 7 of the MPEG-2 standard (known formally as ISO/IEC 13818-7) which is now obsolete.
    Currently it is defined in Part 3 of the MPEG-4 standard (known formally as ISO/IEC 14496-3)."""
    
    AMRNB = 0x100A
    """Adaptive Multi-Rate audio (Narrow Band)."""
    
    AMRWB = 0x100B
    """Adaptive Multi-Rate audio (Wide Band)."""
    
    G726_ADPCM = 0x100C
    """G.726 ITU-T ADPCM."""
    
    WMA = 0x100D
    """Microsoft Windows Media Audio."""
    
    WMA_Professional = 0x100E
    """Microsoft Windows Media Audio Professional."""
    
    WMA_Lossless = 0x100F
    """Microsoft Windows Media Audio Lossless."""
    
    END_AUDIO = 0x1FFF
    """This constant marks the end of audio elementary streams. It is not a valid stream type on its own."""
    
    BEGIN_VIDEO = 0x2000
    """This constant marks the start of video elementary streams. It is not a valid stream type on its own."""
    
    UncompressedVideo = 0x2001
    """Uncompressed video stream."""
    
    MPEG1_Video = 0x2002
    """MPEG-1 Video is defined in Part 2 of the MPEG-1 standard (known formally as ISO/IEC-11172-2)."""
    
    MPEG2_Video = 0x2003
    """MPEG-2 Video is defined in Part 2 of the MPEG-2 standard (known formally as ISO/IEC 13818-2 and as ITU-T H.262)."""
    
    MPEG4_Video = 0x2004
    """MPEG-4 Video is defined in Part 2 of the MPEG-4 standard (known formally as ISO/IEC 14496-2)."""
    
    H261 = 0x2005
    """H.261 Video is defined in the ITU-T H.261 standard."""
    
    H263 = 0x2006
    """H.263 Video is defined in the ITU-T H.263 standard."""
    
    H264 = 0x2007
    """H.264 Video (also known as MPEG-4 AVC / Advanced Video Codec).
    Defined in Part 10 of the MPEG-4 standard (known formally as ISO/IEC 14496-10 and as ITU-T H.264)."""
    
    AVC = 0x2007
    """Alias. Same as H264."""
    
    WMV = 0x2008
    """Microsoft Windows Media Video."""
    
    MJPEG = 0x2009
    """Motion JPEG (M-JPEG)."""
    
    VC1 = 0x200A
    """VC-1 Video is defined in the SMPTE 421M-2006 standard."""
    
    AVS = 0x200B
    """Advanced Video Standard (Chinese national standard)"""
    
    VP8 = 0x200C
    """VP8 is an open video codec released by Google, originally created by On2 Technologies. VP8 is part of the WebM format."""
    
    Theora = 0x200D
    """Theora Video Codec. This is an open standard video codec developed by the Xiph.Org Foundation."""
    
    H265 = 0x200E
    """H.265 Video (also known as MPEG-H HEVC / High Efficiency Video Codec)
    Defined in Part 2 of the MPEG-H standard (known formally as ISO/IEC 23008-2 and as ITU-T H.265)."""
    
    HEVC = 0x200E
    """Alias. Same as H265."""
    
    END_VIDEO = 0x2FFF
    """This constant marks the end of the elementary video streams. It is not a valid stream type on its own."""
    
    BEGIN_CONTAINER = 0x3000
    """This constant marks the start of file formats (a.k.a. containers). It is not a valid stream type on its own."""
    
    AVI = 0x3001
    """Audio Video Interleave (AVI) multimedia container format."""
    
    MP4 = 0x3002
    """MPEG-4 multimedia container format specified in Part 14 of the MPEG-4 standard (formally ISO/IEC 14496-14:2003)."""
    
    ASF = 0x3003
    """Advanced Systems Format (formerly Advanced Streaming Format, Active Streaming Format) (ASF)."""
    
    MPEG_PS = 0x3004
    """MPEG Program Stream."""
    
    MPEG_TS = 0x3005
    """MPEG Transport Stream."""
    
    MPEG_PES = 0x3006
    """MPEG Packetized Elementary Stream (PES)."""
    
    WAVE = 0x3007
    """Waveform Audio file format (WAV, WAVE)."""
    
    FLV = 0x3008
    """Adobe Flash Video container format (FLV).
    This should not be confused with F4V which is a newer Flash Video container format based on ISO/IEC 14496-12 (MPEG-4 Part 12)."""
    
    OGG = 0x3009
    """Open standard container format developed by the Xiph.Org Foundation."""
    
    WebM = 0x300A
    """Open standard container format released by Google and based on a profile of Matroska."""
    
    IVF = 0x300B
    """IVF (Interactive Video Format) is a simple file format that transports raw VP8, VP9, and AV1 video only."""
    
    END_CONTAINER = 0x3FFF
    """This constant marks the end of audio/video containers. It is not a valid stream type on its own."""
    
    BEGIN_IMAGE = 0x4000
    """This constant marks the start of image types. It is not a valid stream type on its own."""
    
    BMP = 0x4001
    """BMP image."""
    
    PNG = 0x4002
    """PNG image."""
    
    JPEG = 0x4003
    """JPEG image."""
    
    TIFF = 0x4004
    """TIFF image."""
    
    GIF = 0x4005
    """GIF image."""
    
    END_IMAGE = 0x4FFF
    """This constant marks the end of image types. It is not a valid stream type on its own."""
    
    BEGIN_DATA = 0x5000
    """This constant marks the start of various data types. It is not a valid stream type on its own."""
    
    Teletext = 0x5001
    """Teletext data."""
    
    MPEG_PSI_PACKETS = 0x5002
    """MPEG Transport Stream Program Specific Information"""
    
    MPEG_TS_PACKETS = 0x5003
    """MPEG Transport Stream packets.
    This is not a complete transport stream but rather a subset of the complete transport stream."""
    
    END_DATA = 0x5FFF
    """This constant marks the end of various data types. It is not a valid stream type on its own."""


class StreamSubType(IntEnum):
    """Defines audio and video stream subtypes."""
    
    Unknown = 0
    """The stream subtype is not defined or is unknown."""
    
    None_ = 65535
    """No stream sub type is defined."""
    
    AAC_ADTS = 1
    """Audio Data Transport Stream: AAC data in frames, similar to mp3. Somewhat compliant.
    Defined in Part 7 of the MPEG-2 standard (known formally as ISO/IEC 13818-7)."""
    
    AAC_ADIF = 2
    """Audio Data Interchange Format: AAC data with a single header. Worst compliance.
    Defined in Part 7 of the MPEG-2 standard (known formally as ISO/IEC 13818-7)."""
    
    AAC_MP4 = 3
    """AAC data packed in MPEG-4 container (MP4). Best compliance."""
    
    AVCC = 4
    """H.264/AVC bitstream without start codes.
    This is how the bitstream is stored in a MPEG-4 container (MP4).
    Instead of start codes, each NALU is prefixed by a length field, which gives the length of the NALU in bytes.
    The size of the length field can vary, but is typically 1, 2, or 4 bytes.
    Defined in ISO 14496-15."""
    
    AVC1 = 4
    """Alias. Same as AVCC."""
    
    MPEG_TS_BDAV = 5
    """MPEG2 transport stream with valid packet time stamps."""
    
    MPEG_Audio_Layer1 = 6
    """MPEG-1 Audio Layer I is commonly abbreviated to MP1. MPEG-1 Layer I is defined in ISO/IEC 11172-3.
    MPEG-2 Layer I is defined in the MPEG-2 Part 3 standard (known formally as ISO/IEC 13818-3)."""
    
    MPEG_Audio_Layer2 = 7
    """MPEG-1 Audio Layer II is commonly abbreviated to MP2. MP2 is a dominant standard for audio broadcasting. MPEG-1 Layer II is defined in ISO/IEC 11172-3.
    MPEG-2 Layer II is defined in the MPEG-2 Part 3 standard (known formally as ISO/IEC 13818-3)."""
    
    MPEG_Audio_Layer3 = 8
    """MPEG-1 Audio Layer III is commonly abbreviated to MP3. MPEG-1 Layer III is defined in ISO/IEC 11172-3.
    MPEG-2 Layer III is defined in the MPEG-2 Part 3 standard (known formally as ISO/IEC 13818-3)."""
    
    G726_RFC3551 = 9
    """G.726 stream packed according to RFC 3551.
    This type of packetization is used in RTP."""
    
    G726_PACKED_RFC3551 = 9
    """Alias. Same as G726_RFC3551."""
    
    G726_AAL2 = 10
    """G.726 stream packed according to ITU-T I.366.2 (AAL type 2).
    This type of packetization is used in Wave files."""
    
    G726_PACKED_AAL2 = 10
    """Alias. Same as G726_AAL2."""
    
    MPEG1_System = 11
    """MPEG-1 Program Stream as specified in MPEG-1 Part 1 (ISO/IEC 11172-1).
    This stream subtype can be used only with the MPEG_PS stream type."""
    
    MPEG2_System = 12
    """MPEG-2 Program Stream as specified in MPEG-2 Part 1 (ISO/IEC 13818-1).
    This stream subtype can be used only with the MPEG_PS stream type."""
    
    AVC_Annex_B = 13
    """H.264 bitstream with start codes (Annex B of ITU-T Rec. H.264).
    H.264 bitstreams are transmitted in this format over the air, or contained in MPEG-2 program or transport streams.
    The H.264 bitstream is formatted as described in Annex B of ITU-T Rec. H.264. According to this specification,
    the bitstream consists of a sequence of NALUs (Network Abstraction Layer Units).
    Each NALU is prefixed with a start code equal to 0x000001 or 0x00000001."""
    
    AAC_RAW = 14
    """Raw AAC data format: AAC data is stored without headers."""


class ScanType(IntEnum):
    """Defines video interlace/scan types."""
    
    Unknown = 0
    """The interlace/scan type is not specified or not known."""
    
    Progressive = 1
    """Progressive (non-interlaced) video."""
    
    TopFieldFirst = 2
    """Interlaced video, where the dominant (first in time) field is the top field."""
    
    BottomFieldFirst = 3
    """Interlaced video, where the dominant (first in time) field is the bottom field."""    


class Use(IntEnum):
    """Specifies whether particular feature should be used."""
    
    Off = 0
    """The feature is OFF."""
    
    On = 1
    """The feature is ON."""
    
    Auto = 2
    """The feature usage is automatic."""


class AlphaCompositingMode(IntEnum):
    """Defines the way a foreground image will be combined with background video."""
    
    Over = 1
    """Foreground over Background - in effect, normal painting operation.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) + (1 - Fa) * (Ba * Brgb)
    
    Normally, alpha blending implies a background alpha of 1.0 (Ba = 1.0), so the compositing result Rrgb becomes:
    Rrgb = (Fa * Frgb) + (1 - Fa) * Brgb
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""
    
    In = 2
    """Foreground in Background - the alpha compositing equivalent of clipping / intersection.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) * Ba
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""
    
    Out = 3
    """Foreground outside Background.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) * (1 - Ba)
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""
    
    Atop = 4
    """Foreground atop Background.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) * Ba + (1 - Fa) * (Ba * Brgb)
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""
    
    Xor = 5
    """Foreground xor Background.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) * (1 - Ba) + (1 - Fa) * (Ba * Brgb)
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""
    
    Plus = 6
    """Foreground plus Background.
    
    If Fa is foreground alpha, Frgb is foreground RGB, Ba is background alpha, Brgb is background RGB, then Rrgb is the compositing result:
    Rrgb = (Fa * Frgb) + (Ba * Brgb)
    
    Fa and Ba are alpha density value with range from 0.0 to 1.0"""


class DeinterlacingMethod(IntEnum):
    """Defines video deinterlacing methods."""
    
    NoDeinterlacing = 0
    """No deinterlacing is performed.
    This can be used to prevent automatic deinterlacing if it's not desired."""
    
    Duplicate = 1
    """Line doubling."""
    
    Blend = 2
    """Motion adaptive deinterlacing."""
    
    Median = 3
    """Calculates the median of consecutive fields"""
    
    EdgeDetect = 4
    """Uses an edge detection filter."""
    
    MedianThreshold = 5
    """Calculates the median of consecutive fields using a threshold."""
    
    CAVT = 6
    """Content adaptive vertical temporal (CAVT) filtering."""

class InterpolationMethod(IntEnum):
    """Defines methods for sample interpolation."""
    
    Unknown = 0
    """The interpolation method is unknown or not set."""
    
    NearestNeighbor = 1
    """Nearest neighbor interpolation"""
    
    Linear = 2
    """Linear interpolation"""
    
    Cubic = 4
    """Cubic convolution interpolation"""
    
    Super = 8
    """Supersampling interpolation"""
    
    Lanczos = 16
    """Interpolation by 3-lobed Lanczos-windowed sinc function."""

class MediaType(IntEnum):
    """Defines media types."""
    
    Unknown = 0
    """The media type is unknown or not specified."""
    
    Audio = 1
    """Audio data."""
    
    Video = 2
    """Video data."""
    
    Text = 3
    """Text data."""
    
    Data = 4
    """Generic data."""    

class ColorFormat(IntEnum):
    """Defines constants for various color formats.
    
    A color format is combination of color space, color depth, chroma sub-sampling, component layout and packing.
    """
    
    Unknown = 0
    """The color format is not specified or unknown."""
    
    YV12 = 1
    """Planar Y, V, U (4:2:0) (note V,U order!)"""
    
    NV12 = 2
    """Planar Y, merged U->V (4:2:0)"""
    
    YUY2 = 3
    """Composite Y->U->Y->V (4:2:2)"""
    
    UYVY = 4
    """Composite U->Y->V->Y (4:2:2)"""
    
    YUV411 = 5
    """Planar Y, U, V (4:1:1)"""
    
    YUV420 = 6
    """Planar Y, U, V (4:2:0)"""
    
    YUV422 = 7
    """Planar Y, U, V (4:2:2)"""
    
    YUV444 = 8
    """Planar Y, U, V (4:4:4)"""
    
    Y411 = 9
    """Composite Y, U, V (4:1:1)"""
    
    Y41P = 10
    """Composite Y, U, V (4:1:1)"""
    
    BGR32 = 11
    """Composite B->G->R"""
    
    BGR24 = 12
    """Composite B->G->R"""
    
    BGR565 = 13
    """Composite B->G->R, 5 bit per B & R, 6 bit per G"""
    
    BGR555 = 14
    """Composite B->G->R->A, 5 bit per component, 1 bit per A"""
    
    BGR444 = 15
    """Composite B->G->R->A, 4 bit per component"""
    
    GRAY = 16
    """Luminance component only."""
    
    YUV420A = 17
    """Planar Y, U, V, Alpha"""
    
    YUV422A = 18
    """Planar Y, U, V, Alpha"""
    
    YUV444A = 19
    """Planar Y, U, V, Alpha"""
    
    YVU9 = 20
    """The vertical subsampling interval is 4. The horizontal subsampling interval is also 4
    This means that a single V and a single U sample are taken for each square block of 16 image pixels.
    Effectively this averages 9 bits per pixel (16 pixels => 16Y + 1V + 1U => 144bits => 9bits/pixel)"""
    
    BGRA32 = 21
    """Composite B->G->R->A"""

class PcmFlags(IntFlag):
    """Defines constants for various LPCM properties.
    
    The constants are expressed as bit flags and can be combined together.
    """
    
    None_ = 0
    """No flag is set."""
    
    Unsigned = 0x1
    """= 0x01

    The audio sample should be interpreted as an unsigned integral value.
    The sample resolution (8-bit, 16-bit, etc.) is a separate LPCM property and is not expressed with PcmFlags.
    This flag is irrelevant when the Float flag is set."""
    
    Float = 0x2
    """
    = 0x2

    The audio sample should be interpreted as a floating point value.
    The sample resolution (32-bit, 64-bit, etc.) is a separate LCPM property and is not expressed with PcmFlags."""
    
    BigEndian = 0x4
    """
    = 0x4

    The sample value is stored in a big endian format.
    When this flag is not set the sample format is little endian."""
    
    NonInterleaved = 0x8
    """
    = 0x8

    When this flag is set audio samples from different channels are not interleaved.
    All samples from channel 0 are first in memory. They are followed by all samples from channel 1 and so on for all channels.
    
    When this flag is not set the samples are interleaved. The first samples from all channels are first in memory.
    They are followed by the second samples from all channels and so on until the last sample in time."""

class AudioChannelFlags(IntFlag):
    """Defines the speaker location of one or more audio channels.
    
    These channel constants are expressed as bit flags and can be combined together.
    A number of common speaker layouts are defined for convenience.
    """
    
    None_ = 0x0
    """No flag is set."""
    
    Left = 0x1
    """Left"""
    
    Right = 0x2
    """Right"""
    
    Center = 0x4
    """Center"""
    
    LFE = 0x8
    """Low-frequency effect. Subwoofer."""
    
    BackLeft = 0x10
    """Back-left. Also known as Left Surround."""
    
    BackRight = 0x20
    """Back-right. Also known as Right Surround."""
    
    LeftCenter = 0x40
    """Front, left of center."""
    
    RightCenter = 0x80
    """Front, right of center."""
    
    BackCenter = 0x100
    """Back-center. Also known as Center Surround."""
    
    SideLeft = 0x200
    """Side-left. Also known as Left Surround Direct."""
    
    SideRight = 0x400
    """Side-right. Also known as Right Surround Direct."""
    
    TopCenter = 0x800
    """Top-center. Also known as Top Center Surround."""
    
    TopFrontLeft = 0x1000
    """Top-front-left. Also known as Vertical Height Left."""
    
    TopFrontCenter = 0x2000
    """Top-front-center. Also known as Vertical Height Center."""
    
    TopFrontRight = 0x4000
    """Top-front-right. Also known as Vertical Height Right."""
    
    TopBackLeft = 0x8000
    """Top-back-left"""
    
    TopBackCenter = 0x10000
    """Top-back-center"""
    
    TopBackRight = 0x20000
    """Top-back-right"""
    
    # Standard layouts
    LayoutMono = Center
    """Mono"""
    
    LayoutStereo = Left | Right
    """Stereo"""
    
    Layout2p1 = Left | Right | LFE
    """Standard 3-channel layout (2.1)"""
    
    LayoutSurround = Left | Right | Center | BackCenter
    """Standard 4-channel layout. Surround."""
    
    LayoutQuad = Left | Right | BackLeft | BackRight
    """Alternative 4-channel layout."""
    
    Layout4p1 = Left | Right | LFE | BackLeft | BackRight
    """Standard 5-channel layout (4.1)"""
    
    Layout5p1 = Left | Right | Center | LFE | BackLeft | BackRight
    """Standard 6-channel layout (5.1)"""
    
    Layout7p1Surround = Left | Right | Center | LFE | BackLeft | BackRight | SideLeft | SideRight
    """Standard 8-channel layout (7.1). Surround."""
    
    Layout5p1Surround = Left | Right | Center | LFE | SideLeft | SideRight
    """Alternative 6-channel layout (5.1). Surround."""
    
    Layout7p1 = Left | Right | Center | LFE | BackLeft | BackRight | LeftCenter | RightCenter
    """Alternative 8-channel layout (7.1)"""

class BitrateMode(IntEnum):
    """Defines the bitrate mode of the audio/video stream."""
    
    Unknown = 0
    """The bitrate mode is not specified or unknown."""
    
    CBR = 1
    """Constant bitrate.
    For uncompressed audio/video with constant bitrate the quality is also constant.
    For compressed audio/video with constant bitrate the quality may be constant or variable."""
    
    VBR = 2
    """Variable bitrate - quality oriented. Constant quality (more or less)."""
    
    ABR = 3
    """Average bitrate.
    Guarantees a predictable audio/video size similar to CBR.
    The bitrate changes to achieve the best quality within the available bitrate capacity."""

class MediaSampleFlags(IntFlag):
    """Defines various media sample features.
    
    These features are expressed as bit flags and can be combined together.
    """
    
    None_ = 0x0
    """No feature is specified."""
    
    KeyFrame = 0x1
    """The media sample / frame can be decoded on its own. It does not depend on previous or subsequent samples / frames."""
    
    Bos = 0x2
    """Beginning of stream"""
    
    Eos = 0x4
    """End of stream"""

class PictureType(IntEnum):
    """Defines video picture types (I/P/B)"""
    
    None_ = 0
    """Picture type is unknown or not specified."""
    
    I = 1
    """I Picture"""
    
    P = 2
    """P Picture"""
    
    B = 3
    """B Picture"""
    
    D = 4
    """D Picture (MPEG-1 only)"""

class FrameType(IntEnum):
    """Defines frame types for audio codecs, particularly for G.711 encoding.
    
    These types indicate the nature of the encoded frame, such as voice activity,
    silence, or errors, and are used to optimize transmission and decoding.
    Values are based on ITU-T G.711 standards and related codecs like G.729 Annex B for VAD.
    
    Added in version 3.2
    """
    
    None_ = 0
    """Alias for Unknown."""

    Unknown = 0
    """Unknown frame type or frame type is not specified.
    Used when the frame type cannot be determined or is undefined."""

    G711BadFrame = 1
    """G.711 bad frame: Indicates a corrupted or invalid frame that cannot be decoded.
    This may occur due to transmission errors or data loss."""
    
    G711UntransmittedFrame = 2
    """G.711 untransmitted frame: Represents a frame that was not transmitted,
    often due to silence or inactivity in VAD-enabled modes.
    Equivalent to no data sent, saving bandwidth."""
    
    G711SIDFrame = 3
    """G.711 SID (Silence Insertion Descriptor) frame: A compact frame describing silence.
    Contains parameters (e.g., from G.729 Annex B VAD) to reconstruct background noise,
    used when voice activity is low to reduce bitrate."""
    
    G711VoiceFrame = 5
    """G.711 voice frame: A full voice/active frame encoded in G.711 A-law or μ-law.
    Contains compressed PCM data for speech or active audio segments.
    Frame size is 80 bytes (10ms at sampling rate 8kHz, 8 bits per sample)."""
    
    G726VoiceFrame = 105
    """G.726 voice frame: A full voice/active frame encoded in G.726 Adaptive Differential Pulse Code Modulation (ADPCM).
    This is the only supported frame type for G.726 codec.
    Frame size varies based on the bitrate: 20, 30, 40 or 50 bytes for 16, 24, 32 or 40 kbps respectively (10ms at sampling rate 8kHz, 2, 3, 4, 5 bits per sample).
    Voice Activity Detection (VAD) and Packet Loss Concealment (PLC) are not supported for G.726."""

class TranscoderStatus(IntEnum):
    """
    Defines the status of a transcoder operation.
    
    It is sent with the Transcoder.on_status event.
    
    See Also:
        Transcoder.on_status
        TranscoderStatusEventArgs
    """
    
    #: Transcoder.run has completed successfully.
    Completed = 0

class H264Profile(IntEnum):
    """
    Defines H.264/AVC profiles
    
    Notes:
        The constants follow the H.264 spec for the element "profile_idc"
    """
    
    #: None/Auto
    None_ = 0
    
    #: Baseline profile
    Baseline = 66
    
    #: Main profile
    Main = 77
    
    #: High profile
    High = 100
    
    #: High 10
    High10 = 110
    
    #: High 4:2:2
    High422 = 122
    
    #: High 4:4:4
    High444 = 144

class H264EntropyCodingMode(IntEnum):
    """
    Defines H.264/AVC entropy coding modes
    
    Notes:
        The constants follow the H.264 spec for the element "entropy_coding_mode_flag"
    """
    
    #: Context-Adaptive Variable-Length Coding (CAVLC)
    CAVLC = 0
    
    #: Context-Adaptive Binary Arithmetic Coding (CABAC)
    CABAC = 1

class H264DeblockingFilter(IntEnum):
    """
    Defines H.264/AVC deblocking filter mode.
    
    Notes:
        The constants follow the H.264 spec for the element "disable_deblocking_filter_idc"
    """
    
    #: Deblocking filter is applied on all luma and chroma block edges of the slice.
    All = 0
    
    #: Deblocking filter is disabled for all block edges of the slice.
    Off = 1
    
    #: Deblocking filter is applied on all luma and chroma block edges of the slice 
    #: with exception of the block edges that coincide with slice boundaries.
    InSlice = 2

class H264DirectPredMode(IntEnum):
    """
    Defines H.264/AVC direct prediction mode.
    
    Notes:
        The constants follow the H.264 spec for the element "direct_spatial_mv_pred_flag"
    """
    
    #: Temporal direct mode prediction
    Temporal = 0
    
    #: Spatial direct mode prediction
    Spatial = 1

class H264MeSplitMode(IntEnum):
    """
    Defines the block sizes for which motion estimation should be done.
    
    Notes:
        Used when encoding H.264/AVC.
    """
    
    #: Analyze only 16x16 blocks for motion estimation
    Only16x16 = 0
    
    #: Analyze all blocks down to 8x8 (16x16, 16x8, 8x16, 8x8)
    DownTo8x8 = 1
    
    #: Analyze all blocks down to 4x4 (16x16, 16x8, 8x16, 8x8, 8x4, 4x8, 4x4).
    #: This partitioning mode is very slow.
    DownTo4x4 = 2

class H264MeMethod(IntEnum):
    """
    Defines the motion estimation methods used when encoding H.264/AVC
    """
    
    #: Full (slowest)
    Full = 0
    
    #: TDL (Two Dimensional Logarithmic Search)
    ClassicLog = 1
    
    #: Log
    Log = 2
    
    #: EPZS (Enhanced Predictive Zonal Search)
    EPZS = 3
    
    #: OSA (Full orthogonal)
    FullOrthogonal = 4
    
    #: Log orthogonal
    LogOrthogonal = 5
    
    #: UMH (Uneven Multi-Hexagon Search)
    UMH = 8

class H264PicCodingType(IntEnum):
    """
    Defines the picture coding type when encoding H.264/AVC
    """
    
    #: Video pictures are coded as frames (progressive video)
    Frames = 0
    
    #: Video pictures are coded as fields (interlaced video)
    Fields = 1

class H264RateControlMethod(IntEnum):
    """
    Defines methods for bitrate control when encoding H.264/AVC
    """
    
    #: Average Bitrate. 
    #: Ensures that the output stream achieves a predictable long-term average bitrate.
    ABR = 2
    
    #: Constant Quantization.
    #: Encodes the video to a constant quantizer. The encoder uses the specified target quantizer, not a target bitrate.
    #: The quantizer is a measure for the amount of data loss: a higher quantizer means that more data will be lost,
    #: which results in a better compression, but also delivers worse visual quality.
    #: This method could be used when a certain level of quality is required and the final bitrate is not a concern.
    #: The bitrate is unpredictable in this mode.
    ConstantQuant = 3

class HardwareEncoder(IntEnum):
    """
    Defines known hardware encoders.
    """
    
    #: Hardware encoders are disabled.
    Off = 0
    
    #: The encoder is selected automatically depending on the available hardware.
    #: The order of preference is: Intel QuickSync, Nvidia NVENC, AMD VCE.
    #: If none of the known encoders are available then a software encoder is used.
    Auto = 1
    
    #: AMD Video Coding Engine (VCE)
    AMD = 2
    
    #: Intel QuickSync Video
    Intel = 3
    
    #: Nvidia NVENC
    Nvidia = 4

class PinConnection(IntEnum):
    """
    Defines pin connection disposition. These constants are used as special values of MediaPin.Connection.
    
    The transcoder tries to connect the input/output pins depending on the values of MediaPin.Connection.
    A value greater than 0 specifies that the media pin participates in explicit mapping.
    """
    
    Disabled = -1
    """The media pin does not participate in pin mapping and is never connected. The pin is ignored by the transcoder."""
    
    Auto = 0
    """
    The media pin participates in an automatic (implicit) mapping.
    When 2 pins are automatically connected by the transcoder MediaPin.Connection is updated with a value greater than 0.
    """

class MetaPictureType(IntEnum):
    """
    Picture type defined as in ID3.
    """
    
    Other = 0
    """Unknown or unspecified picture type"""
    
    FileIcon = 1
    """32x32 pixels 'file icon' (PNG only); only one in a ID3 tag"""
    
    OtherFileIcon = 2
    """Only one in a ID3 tag"""
    
    FrontCover = 3
    """Album/Disc front cover"""
    
    BackCover = 4
    """Album/Disc back cover"""
    
    LeafletPage = 5
    """Album/Disc leaflet page"""
    
    Media = 6
    """Printed on the media (e.g. label side of a CD)"""
    
    LeadArtist = 7
    """Lead artist / Lead performer / Soloist"""
    
    Artist = 8
    """Artist / Performer"""
    
    Conductor = 9
    """Conductor"""
    
    Band = 10
    """Band / Orchestra"""
    
    Composer = 11
    """Composer / Music writer"""
    
    TextWriter = 12
    """Lyricist / Text writer"""
    
    RecordingLocation = 13
    """Location where the music is recorded"""
    
    DuringRecording = 14
    """The picture is made during recording"""
    
    DuringPerformance = 15
    """The picture is made during performance"""
    
    VideoCapture = 16
    """Movie/video screen capture"""
    
    BrightColoredFish = 17
    """A brightly coloured fish :0"""
    
    Illustration = 18
    """Illustration"""
    
    ArtistLogotype = 19
    """Band / Artist logotype"""
    
    PublisherLogotype = 20
    """Publisher / Studio logotype"""

class MimeType:
    """Multipurpose Internet Mail Extensions (MIME) used in AVBlocks"""
    
    Gif: str = "image/gif"
    """GIF MIME type"""
    
    Jpeg: str = "image/jpeg"
    """JPEG MIME type"""
    
    Png: str = "image/png"
    """PNG MIME type"""
    
    Tiff: str = "image/tiff"
    """TIFF MIME type"""

class Meta:
    """Metadata attribute names (tags)"""
    
    Comment: str = "Comment"
    """Comment"""
    
    InvolvedPeople: str = "InvolvedPeople"
    """Involved people"""
    
    PlayCounter: str = "PlayCounter"
    """Play counter"""
    
    Popularimeter: str = "Popularimeter"
    """Popularity meter / rating"""
    
    Album: str = "Album"
    """Album"""
    
    Composer: str = "Composer"
    """Composer"""
    
    Genre: str = "Genre"
    """Genre"""
    
    Copyright: str = "Copyright"
    """Copyright"""
    
    Date: str = "Date"
    """Date (YYYY-MM-DD)"""
    
    EncodedBy: str = "EncodedBy"
    """Encoding software"""
    
    Lyricist: str = "Lyricist"
    """Lyricist / text writer"""
    
    FileType: str = "FileType"
    """File type"""
    
    Time: str = "Time"
    """Time"""
    
    ContentGroup: str = "ContentGroup"
    """Content group"""
    
    Title: str = "Title"
    """Title"""
    
    Subtitle: str = "Subtitle"
    """Subtitle"""
    
    Language: str = "Language"
    """Language"""
    
    MediaType: str = "MediaType"
    """Media type"""
    
    OrigAlbum: str = "OrigAlbum"
    """Original album"""
    
    OrigFileName: str = "OrigFileName"
    """Original file name"""
    
    OrigLyricist: str = "OrigLyricist"
    """Original lyricist / text writer"""
    
    OrigArtist: str = "OrigArtist"
    """Original artist"""
    
    LeadArtist: str = "LeadArtist"
    """Lead artist"""
    
    AlbumArtist: str = "AlbumArtist"
    """Album artist"""
    
    Conductor: str = "Conductor"
    """Conductor"""
    
    RemixArtist: str = "RemixArtist"
    """Remix / cover artist"""
    
    DiscNum: str = "DiscNum"
    """Disc number is 1-based"""
    
    Publisher: str = "Publisher"
    """Publisher"""
    
    TrackNum: str = "TrackNum"
    """Track number is 1-based"""
    
    RecordingDates: str = "RecordingDates"
    """Recording dates"""
    
    InternetRadioStation: str = "InternetRadioStation"
    """Internet radio station name"""
    
    EncoderSettings: str = "EncoderSettings"
    """Encoding software settings"""
    
    Year: str = "Year"
    """Year only (YYYY)"""
    
    UserText: str = "UserText"
    """User text"""
    
    UnsyncedLyrics: str = "UnsyncedLyrics"
    """Unsynced lyrics"""
    
    UrlCommercialInfo: str = "UrlCommercialInfo"
    """URL pointing at a web page with information such as where the album can be bought"""
    
    UrlCopyright: str = "UrlCopyright"
    """URL pointing at a web page where the terms of use and ownership of the file is described"""
    
    UrlAudioFile: str = "UrlAudioFile"
    """URL pointing at a file specific web page"""
    
    UrlArtist: str = "UrlArtist"
    """URL pointing at the artist's official web page.
    There may be more than one attributes with this name if the audio contains more than one performer"""
    
    UrlAudioSource: str = "UrlAudioSource"
    """URL pointing at the official web page for the source of the audio file, e.g. a movie"""
    
    UrlRadioPage: str = "UrlRadioPage"
    """URL pointing at the homepage of the Internet radio station"""
    
    UrlPayment: str = "UrlPayment"
    """URL pointing at a web page that will handle the process of paying for this file"""
    
    UrlPublisher: str = "UrlPublisher"
    """URL pointing at the official web page for the publisher"""
    
    UrlUser: str = "UrlUser"
    """User URL"""
    
    Private: str = "Private"
    """Private comment"""
    
    BeatsPerMinute: str = "BeatsPerMinute"
    """Beats per minute"""

class HwEngine(IntEnum):
    """Hardware engine for encoding/decoding/processing."""
    
    None_ = 0
    """HwEngine not specified"""
    
    QuickSyncVideo = 1
    """Intel Quick Sync Video"""
    
    Nvenc = 2
    """Nvidia NVENC"""
    
    VideoCodingEngine = 3
    """AMD Video Coding Engine (VCE)"""

class HwVendor(IntEnum):
    """Hardware Vendor"""
    
    None_ = 0
    """Hardware Vendor not specified"""
    
    Intel = 1
    """Intel Corporation"""
    
    Nvidia = 2
    """Nvidia Corporation"""
    
    Amd = 3
    """Advanced Micro Devices, Inc."""

class HwCodecType(IntEnum):
    """Hardware Codec type"""
    
    None_ = 0
    """Hardware Codec type not specified"""
    
    H264Encoder = 1
    """H.264/AVC Encoder"""
    
    H265Encoder = 2
    """H.265/HEVC Encoder"""

class HwApi(IntEnum):
    """API for using hardware engines"""
    
    None_ = 0
    """HwApi not specified"""
    
    IntelMedia = 1
    """Intel Media SDK"""
    
    Nvenc = 2
    """NVENC SDK"""
    
    AmdOpenVideo = 3
    """AMD OpenVideo"""
    
    AmdMedia = 4
    """AMF (AMD Media Framework)"""
    
    MediaFoundation = 5
    """Windows Media Foundation"""

class H265Profile(IntEnum):
    """H.265 / HEVC Profiles"""
    
    None_ = 0
    """None/Auto"""
    
    Main = 1
    """Main profile"""
    
    Main10 = 2
    """Main10 profile"""

class H265Level(IntEnum):
    """H.265 / HEVC Levels"""
    
    None_ = 0
    """None / Auto"""
    
    L1 = 30
    """= 30"""
    
    L2 = 60
    """= 60"""
    
    L21 = 63
    """= 63"""
    
    L3 = 90
    """= 90"""
    
    L31 = 93
    """= 93"""
    
    L4 = 120
    """= 120"""
    
    L41 = 123
    """= 123"""
    
    L5 = 150
    """= 150"""
    
    L51 = 153
    """= 153"""
    
    L52 = 156
    """= 156"""
    
    L6 = 180
    """= 180"""
    
    L61 = 183
    """= 183"""
    
    L62 = 186
    """= 186"""

class H265Tier(IntEnum):
    """H.265 / HEVC Tiers"""
    
    Main = 0
    """= 0"""
    
    High = 1
    """= 1"""

class StereoMode(IntEnum):
    """Defines stereo mode in MPEG Audio and AAC."""
    
    None_ = 0
    """None/LR mode is chosen by default"""
    
    LR = 2
    """If MPEG Audio/AAC encoder is used with LR mode the encoding will be done using normal independent coding of left and right channels"""
    
    MidSide = 3
    """If AAC encoder is used with mode MidSide the encoding will be done using Mid/Side coding technique.
    If MPEG Audio encoder is used with this mode:
      - Layers 1 and 2: the encoding will be done using normal independent coding of left and right channels (same as LR mode)
      - Layer 3: the encoding will use Intensity coding technique when the bit rate is lower than 96Kb/s for 2 channel setup
        in combination with normal independent coding of left and right channels, otherwise will use only left and right coding.
      - Layer 3: the encoding of every frame will be done with Mid/Side or Left-Right Stereo coding technique
        depending on the data present in the frame"""
    
    Joint = 4
    """If AAC encoder is used with mode Joint the encoding of every frame will be done with Mid/Side or Left-Right Stereo coding technique
    depending on the data present in the frame.
    If MPEG Audio encoder is used with this mode:
      - Layer 1: the encoding will be done using normal independent coding of left and right channels (same as LR mode).
      - Layer 2: the encoding will use Intensity coding technique when the bit rate is lower than 96Kb/s for 2 channel setup
        in combination with normal independent coding of left and right channels, otherwise will use only left and right coding.
      - Layer 3: the encoding of every frame will be done with Mid/Side or Left-Right Stereo coding technique
        depending on the data present in the frame"""
