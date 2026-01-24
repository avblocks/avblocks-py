"""
Output presets supported by AVBlocks.
"""

class Preset:
    """
    Defines output presets supported by AVBlocks.
    
    Each preset represents a collection of audio and video properties and parameters.
    It can be used as an easy way to specify the required output of the transcoder.

        ```python
        # Access presets using dot notation
        preset = Preset.Video.Generic.MP4.H264_720p
        print(preset)  # Output: "generic.mp4.h264.720p"

        # Audio presets
        audio_preset = Preset.Audio.Generic.MP3.CD
        print(audio_preset)  # Output: "mp3.audiocd.192kbps"

        # Device-specific presets
        ipad_preset = Preset.Video.iPad.H264_720p
        print(ipad_preset)  # Output: "ipad.mp4.h264.720p"

        # Apple Live Streaming
        streaming_preset = Preset.Video.AppleLiveStreaming.H264_720p
        print(streaming_preset)  # Output: "wifi.wide.h264.1280x720.30p.4500k.aac.128k"
        ```
    """
    
    class Audio:
        """Describes output audio presets structured by codec and device type."""
        
        class Generic:
            """Generic audio presets (unrelated to specific devices)"""
            
            AAC = "aac"
            """AAC stream in ADTS format, stereo, 128 kbps"""
            
            class M4A:
                """M4A presets (AAC audio in MP4 container)"""
                
                LowQuality = "mp4.aac.low.quality"
                """AAC stream in MP4 container, stereo, 96 kbps, CBR"""
                
                GoodQuality = "mp4.aac.good.quality"
                """AAC stream in MP4 container, stereo, 128 kbps, CBR"""
                
                HighQuality = "mp4.aac.high.quality"
                """AAC stream in MP4 container, stereo, 160 kbps, CBR"""
                
                CBR_128kbps = "mp4.aac.44100hz.128kbps"
                """AAC audio stream in MP4 format, 44100 Hz, stereo, 128 kbps"""
                
                CBR_256kbps = "mp4.aac.44100hz.256kbps"
                """AAC audio stream in MP4 format, 44100 Hz, stereo, 256 kbps, CBR"""
            
            class MP3:
                """MP3 presets (MPEG-1 Layer 3)"""
                
                AMRadio = "mp3.am.radio.32kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 32 kbps, mono"""
                
                FMRadio = "mp3.fm.radio.32kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 96 kbps, stereo"""
                
                Voice = "mp3.voice.64kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 64 kbps, mono"""
                
                Radio = "mp3.radio.112kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 112 kbps, stereo"""
                
                Tape = "mp3.tape.128kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 128 kbps, stereo"""
                
                HiFi = "mp3.hi.fi.160kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 160 kbps, stereo"""
                
                CD = "mp3.audiocd.192kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 192 kbps, stereo"""
                
                Studio = "mp3.studio.256kbps"
                """MPEG-1 Layer 3 audio, 44100 Hz, 256 kbps, stereo"""
                
                CBR_128kbps = "mp3.44100hz.128kbps"
                """MPEG-1 Layer 3 audio, 44100Hz, stereo, 128 kbps"""
                
                CBR_256kbps = "mp3.44100hz.256kbps"
                """MPEG-1 Layer 3 audio, 44100Hz, stereo, 256 kbps"""
            
            class WMA:
                """Presets for Windows Media Audio"""
                
                class Standard:
                    """Presets for the WMA standard codec"""
                    
                    CBR_64kbps = "wma.cbr.64kbps"
                    """Audio: Windows Media Audio Standard, CBR, 44100 Hz, stereo, 64 kbps"""
                    
                    CBR_96kbps = "wma.cbr.96kbps"
                    """Audio: Windows Media Audio Standard, CBR, 44100 Hz, stereo, 96 kbps"""
                    
                    CBR_128kbps = "wma.cbr.128kbps"
                    """Audio: Windows Media Audio Standard, CBR, 44100 Hz, stereo, 128 kbps"""
                    
                    CBR_160kbps = "wma.cbr.160kbps"
                    """Audio: Windows Media Audio Standard, CBR, 44100 Hz, stereo, 160 kbps"""
                
                class Professional:
                    """Presets for the WMA Pro codec"""
                    
                    VBR_Q75 = "wma.pro.q75"
                    """Audio: Windows Media Audio Professional, VBR, 44100 Hz, stereo, Quality 75 (0-100)"""
                    
                    VBR_Q90 = "wma.pro.q90"
                    """Audio: Windows Media Audio Professional, VBR, 44100 Hz, stereo, Quality 90 (0-100)"""
                    
                    VBR_Q100 = "wma.pro.q100"
                    """Audio: Windows Media Audio Professional, VBR, 44100 Hz, stereo, Quality 100 (0-100)"""
                
                class Lossless:
                    """Presets for the WMA Lossless codec"""
                    
                    CD = "wma.lossless.audiocd"
                    """Audio: Windows Media Audio Lossless, 44100 Hz, stereo"""
            
            class OggVorbis:
                """Presets for Vorbis audio in Ogg container"""
                
                VBR_Q4 = "ogg.vorbis.q4"
                """Audio: Vorbis, VBR, quality 4 (from -0.1 to 1.0), VBR"""
                
                VBR_Q8 = "ogg.vorbis.q8"
                """Audio: Vorbis, VBR, quality 8 (from -0.1 to 1.0) VBR"""
        
        class AudioCD:
            """Presets for audio compatible with AudioCD (LPCM, 44100 Hz, stereo, 16-bit)"""
            
            WAV = "wav.audiocd"
            """Audio: WAV with parameters as in Audio CD (PCM, 44100 Hz, 16-bit, stereo)"""
        
        class DVD:
            """Presets for audio compatible with DVD-Video"""
            
            MP2 = "mp2.dvd"
            """MPEG-1 Layer 2 audio, 48000Hz (suitable for DVD)"""
    
    class Video:
        """Describes output video presets structured by codec and device type."""
        
        class Generic:
            """Generic video presets. These presets are not related to any specific device."""
            
            class MP4:
                """Generic MP4 presets (audio and video streams in MP4 container)"""
                
                H264_1080p = "generic.mp4.h264.1080p"
                """Video: H.264, 29.97 fps, 1920x1080, bitrate 5400 kbps, profile Baseline, aspect 16:9, Level 4"""
                
                H264_720p = "generic.mp4.h264.720p"
                """Video: H.264, 29.97 fps, 1280x720, bitrate 2400 kbps, profile Baseline, aspect 16:9, Level 3.1"""
                
                H264_Wide_480p = "generic.mp4.h264.wide.480p"
                """Video: H.264, 29.97 fps, 854x480, bitrate 1200 kbps, profile Baseline, aspect 16:9, Level 3.1"""
                
                H264_480p = "generic.mp4.h264.480p"
                """Video: H.264, 29.97 fps, 640x480, bitrate 900 kbps, profile Baseline, aspect 4:3, Level 3"""
                
                H264_Wide_360p = "generic.mp4.h264.wide.360p"
                """Video: H.264, 29.97 fps, 640x360, bitrate 720 kbps, profile Baseline, aspect 16:9, Level 3"""
                
                H264_360p = "generic.mp4.h264.360p"
                """Video: H.264, 29.97 fps, 480x360, bitrate 600 kbps, profile Baseline, aspect 4:3, Level 3"""
                
                H264_240p = "generic.mp4.h264.240p"
                """Video: H.264, 15 fps, 320x240, bitrate 300 kbps, profile Baseline, aspect 4:3, Level 1.3"""
                
                Base_H264_AAC = "mp4.h264.aac"
                """Video: H.264, Audio: AAC, Container: MP4. Does not enforce specific audio and video properties."""
            
            class WebM:
                """WebM presets"""
                
                Base_VP8_Vorbis = "webm.vp8.vorbis"
                """Video: VP8, Audio: Vorbis, Container: WebM"""
                
                VP8_3G_240p_350K_Vorbis_64K = "webm.vp8.3g.240p.350k.vorbis.64k"
                """Video: VP8, 24 fps, 320x240, bitrate 350 kbps, VBR, keyframe distance 120"""
                
                VP8_Wide_3G_240p_350K_Vorbis_64K = "webm.vp8.wide.3g.240p.350k.vorbis.64k"
                """Video: VP8, 24 fps, 426x240, bitrate 350 kbps, VBR, keyframe distance 120"""
                
                VP8_4G_360p_700K_Vorbis_64K = "webm.vp8.4g.360p.700k.vorbis.64k"
                """Video: VP8, 30 fps, 480x360, bitrate 700 kbps, VBR, keyframe distance 150"""
                
                VP8_Wide_4G_360p_700K_Vorbis_64K = "webm.vp8.wide.4g.360p.700k.vorbis.64k"
                """Video: VP8, 30 fps, 640x360, bitrate 700 kbps, VBR, keyframe distance 150"""
                
                VP8_SD_480p_1200K_Vorbis_128K = "webm.vp8.sd.480p.1200k.vorbis.128k"
                """Video: VP8, 30 fps, 640x480, bitrate 1200 kbps, VBR, keyframe distance 300"""
                
                VP8_Wide_SD_480p_1200K_Vorbis_128K = "webm.vp8.wide.sd.480p.1200k.vorbis.128k"
                """Video: VP8, 30 fps, 854x480, bitrate 1200 kbps, VBR, keyframe distance 300"""
                
                VP8_SD_576p_1600K_Vorbis_128K = "webm.vp8.sd.576p.1600k.vorbis.128k"
                """Video: VP8, 25 fps, 720x576, bitrate 1600 kbps, VBR, keyframe distance 250"""
                
                VP8_Wide_SD_576p_1600K_Vorbis_128K = "webm.vp8.wide.sd.576p.1600k.vorbis.128k"
                """Video: VP8, 25 fps, 1024x576, bitrate 1600 kbps, VBR, keyframe distance 250"""
                
                VP8_Wide_HD_720p_2500K_Vorbis_192K = "webm.vp8.wide.hd.720p.2500k.vorbis.192k"
                """Video: VP8, 30 fps, 1280x720, bitrate 2500 kbps, VBR, keyframe distance 300"""
                
                VP8_Wide_HD_1080p_5000K_Vorbis_192K = "webm.vp8.wide.hd.1080p.5000k.vorbis.192k"
                """Video: VP8, 30 fps, 1920x1080, bitrate 5000 kbps, VBR, keyframe distance 300"""
        
        class DVD:
            """Presets for DVD-Video"""
            
            PAL_4x3_MP2 = "dvd.pal.4x3.mp2"
            """Video: MPEG-2, 25 fps, 720 x 576, aspect 4:3"""
            
            PAL_16x9_MP2 = "dvd.pal.16x9.mp2"
            """Video: MPEG-2, 25 fps, 720 x 576, aspect 16:9"""
            
            NTSC_4x3_PCM = "dvd.ntsc.4x3.pcm"
            """Video: MPEG-2, 29.97 fps, 720 x 480, aspect 4:3"""
            
            NTSC_4x3_MP2 = "dvd.ntsc.4x3.mp2"
            """Video: MPEG-2, 29.97 fps, 720 x 480, aspect 4:3"""
            
            NTSC_16x9_PCM = "dvd.ntsc.16x9.pcm"
            """Video: MPEG-2, 29.97 fps, 720 x 480, aspect 16:9"""
            
            NTSC_16x9_MP2 = "dvd.ntsc.16x9.mp2"
            """Video: MPEG-2, 29.97 fps, 720 x 480, aspect 16:9"""
        
        class BDAV:
            """Presets for Blu-ray Disc Audio-Visual MPEG-2 Transport Stream"""
            
            H264_1920x1080_5994i_PCM = "bdav-h264-1920x1080-59.94i-pcm"
            """Video: H.264, 1980 x 1080, 59.94 fps interlaced, aspect ratio 16:9, 25000 kbps"""
            
            H264_1920x1080_50i_PCM = "bdav-h264-1920x1080-50i-pcm"
            """Video: H.264, 1980 x 1080, 50 fps interlaced, aspect ratio 16:9, 25000 kbps"""
            
            H264_1920x1080_24p_PCM = "bdav-h264-1920x1080-24p-pcm"
            """Video: H.264, 1980 x 1080, 24 fps progressive, aspect ratio 16:9, 25000 kbps"""
            
            H264_1920x1080_2398p_PCM = "bdav-h264-1920x1080-23.976p-pcm"
            """Video: H.264, 1980 x 1080, 23.976 fps progressive, aspect ratio 16:9, 25000 kbps"""
            
            H264_1440x1080_5994i_PCM = "bdav-h264-1440x1080-59.94i-pcm"
            """Video: H.264, 1440 x 1080, 59.94 fps interlaced, aspect ratio 16:9, 25000 kbps"""
            
            H264_1440x1080_50i_PCM = "bdav-h264-1440x1080-50i-pcm"
            """Video: H.264, 1440 x 1080, 50 fps interlaced, aspect ratio 16:9, 25000 kbps"""
            
            H264_1440x1080_24p_PCM = "bdav-h264-1440x1080-24p-pcm"
            """Video: H.264, 1440 x 1080, 24 fps progressive, aspect ratio 16:9, 25000 kbps"""
            
            H264_1440x1080_2398p_PCM = "bdav-h264-1440x1080-23.976p-pcm"
            """Video: H.264, 1440 x 1080, 23.976 fps progressive, aspect ratio 16:9, 25000 kbps"""
            
            H264_1280x720_5994p_PCM = "bdav-h264-1280x720-59.94p-pcm"
            """Video: H.264, 1280 x 720, 59.94 fps progressive, aspect ratio 16:9, 15000 kbps"""
            
            H264_1280x720_50p_PCM = "bdav-h264-1280x720-50p-pcm"
            """Video: H.264, 1280 x 720, 50 fps progressive, aspect ratio 16:9, 15000 kbps"""
            
            H264_1280x720_24p_PCM = "bdav-h264-1280x720-24p-pcm"
            """Video: H.264, 1280 x 720, 24 fps progressive, aspect ratio 16:9, 15000 kbps"""
            
            H264_1280x720_2398p_PCM = "bdav-h264-1280x720-23.976p-pcm"
            """Video: H.264, 1280 x 720, 23.976 fps progressive, aspect ratio 16:9, 15000 kbps"""
        
        class HDV:
            """Presets for High-definition video MPEG-2 Transport Stream"""
            
            MPEG_1080i_30p = "hdv.m2t.1080i.30p"
            """Video: MPEG-2, 29.97 fps, 1440x1080, aspect ratio 16:9"""
            
            MPEG_1080i_25p = "hdv.m2t.1080i.25p"
            """Video: MPEG-2, 25 fps, 1440x1080, aspect ratio 16:9"""
            
            MPEG_1080p_30p = "hdv.m2t.1080p.30p"
            """Video: MPEG-2, 29.97 fps, 1440x1080, aspect ratio 16:9"""
            
            MPEG_1080p_25p = "hdv.m2t.1080p.25p"
            """Video: MPEG-2, 25 fps, 1440x1080, aspect ratio 16:9"""
            
            MPEG_1080p_24p = "hdv.m2t.1080p.24p"
            """Video: MPEG-2, 23.976 fps, 1440x1080, aspect ratio 16:9"""
            
            MPEG_720p_60p = "hdv.m2t.720p.60p"
            """Video: MPEG-2, 59.94 fps, 1280x720, aspect 16:9"""
            
            MPEG_720p_50p = "hdv.m2t.720p.50p"
            """Video: MPEG-2, 50 fps, 1280x720, aspect 16:9"""
            
            MPEG_720p_30p = "hdv.m2t.720p.30p"
            """Video: MPEG-2, 29.97 fps, 1280x720, aspect 16:9"""
            
            MPEG_720p_25p = "hdv.m2t.720p.25p"
            """Video: MPEG-2, 25 fps, 1280x720, aspect 16:9"""
            
            MPEG_720p_24p = "hdv.m2t.720p.24p"
            """Video: MPEG-2, 23.976 fps, 1280x720, aspect 16:9"""
        
        class VCD:
            """Presets for Video CD"""
            
            PAL = "vcd.pal"
            """Video: MPEG-1, 25fps, 352 x 288, 1100 kbps"""
            
            NTSC = "vcd.ntsc"
            """Video: MPEG-1, 29.97 fps, 352 x 240, 1100 kbps"""
        
        class iPad:
            """Presets for iPad devices"""
            
            H264_576p = "ipad.mp4.h264.576p"
            """Video: H.264, 30 fps, 768 x 576, 2500 kbps"""
            
            H264_720p = "ipad.mp4.h264.720p"
            """Video: H.264, 30 fps, 1280 x 720, 4000 kbps"""
            
            MPEG4_480p = "ipad.mp4.mpeg4.480p"
            """Video: MPEG-4 Visual, 30 fps, 640 x 480, 2500 kbps"""
        
        class AppleTV:
            """Presets for AppleTV devices"""
            
            H264_480p = "appletv.h264.480p"
            """Video: H.264, 24 fps, 640 x 480, 1500 kbps"""
            
            H264_720p = "appletv.h264.720p"
            """Video: H.264, 24 fps, 1280 x 720, 4000 kbps"""
            
            MPEG4_480p = "appletv.mpeg4.480p"
            """Video: MPEG-4 Visual, 24 fps, 640 x 480, 2000 kbps"""
            
            AppleTV2G_MP4_H264_720p = "appleTV2g.mp4.h264.720p"
            """Video: H.264, 30 fps, 1280x720, bitrate 5000 kbps, profile Main, aspect 16:9, Level 3.1"""
            
            AppleTV3G_MP4_H264_1080p = "appleTV3g.mp4.h264.1080p"
            """Video: H.264, 30 fps, 1920x1080, bitrate 5000 kbps, profile High, aspect 16:9, Level 4"""
        
        class Web:
            """Presets for Facebook, SmugMug, Vimeo, YouTube"""
            
            class MP4:
                """MP4 presets"""
                
                H264_720p = "Web.mp4.h264.720p"
                """Video: H.264, 30 fps, 1280x720, bitrate 2200 kbps, profile Main, aspect 16:9, Level 3.1"""
        
        class Kindle:
            """Presets for Kindle"""
            
            KindleFireHD_8_9_MP4_H264_1080p = "KindleFireHD8.9.mp4.h264.1080p"
            """Video: H.264, 30 fps, 1920x1080, bitrate 5400 kbps, profile Main, aspect 16:9, Level 4"""
            
            KindleFireHD_MP4_H264_720p = "KindleFireHD.mp4.h264.720p"
            """Video: H.264, 30 fps, 1280x720, bitrate 2200 kbps, profile Main, aspect 16:9, Level 4"""
            
            KindleFire_MP4_H264_576p = "KindleFire.mp4.h264.576p"
            """Video: H.264, 30 fps, 1024x576, bitrate 1600 kbps, profile Main, aspect 16:9, Level 3.1"""
        
        class iPhone:
            """Presets for iPhone devices"""
            
            H264_480p = "iphone.mp4.h264.480p"
            """Video: H.264, 25 fps, 640 x 480, 1000 kbps"""
            
            MPEG4_480p = "iphone.mp4.mpeg4.480p"
            """Video: MPEG-4 Visual, 25 fps, 640 x 480, 2000 kbps"""
            
            iPhone4_MP4_H264_720p = "iPhone4.mp4.h264.720p"
            """Video: H.264, 30 fps, 1280x720, bitrate 2200 kbps, profile Main, aspect 16:9, Level 3.1"""
            
            iPhone4S_MP4_H264_1080p = "iPhone4s.mp4.h264.1080p"
            """Video: H.264, 30 fps, 1920x1080, bitrate 5000 kbps, profile High, aspect 16:9, Level 4.1"""
            
            iPhone3GS_MP4_H264_480 = "iPhone3gs.mp4.h264.480p"
            """Video: H.264, 30 fps, 640x480, bitrate 600 kbps, profile Baseline, aspect 4:3, Level 3"""
        
        class iPod:
            """Presets for iPod devices"""
            
            H264_240p = "ipod.mp4.h264.240p"
            """Video: H.264 Baseline Profile, 25 fps, 320 x 240, 300 kbps"""
            
            MPEG4_240p = "ipod.mp4.mpeg4.240p"
            """Video: MPEG-4 Visual, 25 fps, 320 x 240, 600 kbps"""
            
            iPodTouch_MP4_H264_480p = "iPodTouch.mp4.h264.480p"
            """Video: H.264, 30 fps, 640x480, bitrate 1500 kbps, profile Baseline, aspect 4:3, Level 3"""
        
        class AppleLiveStreaming:
            """Presets for Apple Live Streaming"""
            
            WiFi_Wide_H264_1920x1080_30p_11000K_AAC_128K = "wifi.wide.h264.1920x1080.30p.11000k.aac.128k"
            """Apple Live Streaming: 11128 Kbit"""
            
            WiFi_Wide_H264_1280x720_30p_4500K_AAC_128K = "wifi.wide.h264.1280x720.30p.4500k.aac.128k"
            """Apple Live Streaming: 4628 Kbit"""
            
            WiFi_Wide_H264_1280x720_30p_2500K_AAC_128K = "wifi.wide.h264.1280x720.30p.2500k.aac.128k"
            """Apple Live Streaming: 2628 Kbit"""
            
            WiFi_Wide_H264_960x540_30p_1800K_AAC_128K = "wifi.wide.h264.960x540.30p.1800k.aac.128k"
            """Apple Live Streaming: 1928 Kbit"""
            
            WiFi_Wide_H264_640x360_30p_1200K_AAC_96K = "wifi.wide.h264.640x360.30p.1200k.aac.96k"
            """Apple Live Streaming: 1296 Kbit"""
            
            WiFi_Wide_H264_640x360_30p_600K_AAC_96K = "wifi.wide.h264.640x360.30p.600k.aac.96k"
            """Apple Live Streaming: 696 Kbit"""
            
            WiFi_H264_1280x960_30p_4500K_AAC_128K = "wifi.h264.1280x960.30p.4500k.aac.128k"
            """Apple Live Streaming: 4628 Kbit"""
            
            WiFi_H264_960x720_30p_2500K_AAC_128K = "wifi.h264.960x720.30p.2500k.aac.128k"
            """Apple Live Streaming: 2628 Kbit"""
            
            WiFi_H264_960x720_30p_1200K_AAC_96K = "wifi.h264.960x720.30p.1200k.aac.96k"
            """Apple Live Streaming: 1296 Kbit"""
            
            WiFi_H264_640x480_30p_1200K_AAC_96K = "wifi.h264.640x480.30p.1200k.aac.96k"
            """Apple Live Streaming: 1296 Kbit"""
            
            WiFi_H264_640x480_30p_800K_AAC_96K = "wifi.h264.640x480.30p.800k.aac.96k"
            """Apple Live Streaming: 896 Kbit"""
            
            WiFi_H264_640x480_30p_600K_AAC_96K = "wifi.h264.640x480.30p.600k.aac.96k"
            """Apple Live Streaming: 696 Kbit"""
            
            Cellular_Wide_H264_400x224_30p_400K_AAC_40K = "cellular.wide.h264.400x224.30p.400k.aac.40k"
            """Apple HTTP Streaming: 440 Kbit"""
            
            Cellular_H264_400x300_30p_400K_AAC_40K = "cellular.h264.400x300.30p.400k.aac.40k"
            """Apple HTTP Streaming: 440 Kbit"""
            
            # Aliases
            H264_480p = WiFi_H264_640x480_30p_1200K_AAC_96K
            """Alias for WiFi_H264_640x480_30p_1200K_AAC_96K"""
            
            H264_720p = WiFi_Wide_H264_1280x720_30p_4500K_AAC_128K
            """Alias for WiFi_Wide_H264_1280x720_30p_4500K_AAC_128K"""
        
        class AndroidPhone:
            """Presets for Android phones"""
            
            H264_360p = "android-phone.mp4.h264.360p"
            """Video: H264 Baseline Profile, 30 fps, 480 x 360, 800 kbps"""
            
            H264_720p = "android-phone.mp4.h264.720p"
            """Video: H264 Baseline Profile, 30 fps, 1280 x 720, 2000 kbps"""
        
        class AndroidTablet:
            """Presets for Android tablets"""
            
            H264_720p = "android-tablet.mp4.h264.720p"
            """Video: H264 Baseline Profile, 30 fps, 1280 x 720, 4000 kbps"""
            
            WebM_VP8_720p = "android-tablet.webm.vp8.720p"
            """Video: VP8, 30 fps, 1280 x 720, 4000 kbps"""
        
        class Fast:
            """Presets for fastest possible encoding"""
            
            class MP4:
                """Fast MP4 presets (audio and video streams in MP4 container)"""
                
                H264_AAC = "fast.mp4.h264.aac"
                """Video: H.264, Audio: AAC, Container: MP4. Fast H.264 encoding."""
