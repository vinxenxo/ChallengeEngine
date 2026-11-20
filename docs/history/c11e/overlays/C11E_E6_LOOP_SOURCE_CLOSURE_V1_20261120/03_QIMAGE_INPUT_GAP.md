# QImage input gap

The synthetic QImage benchmark validates the destination pixel compositor, not a source decoder. Existing Loop pixel manifests state `source_pixel_format=yuvj420p`, `decode_pixel_format=yuv420p`, `frames_written_to_disk=false`. QImage's exact input contract is `Format_RGB888`, row stride `width*3`, contiguous byte length `width*height*3`. At 720x1280 this is 2160 bytes per row and 2,764,800 bytes per frame.

YUV420P frame bytes are 1,382,400. A color conversion is required. Existing metadata does not state color space/matrix, primaries or transfer; range `pc` alone is insufficient to define conversion. No conversion is authorized or to be improvised.
