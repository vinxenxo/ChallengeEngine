# C11-C Video Delivery — Meta Reels Review

## Important distinction

The C11-C 2.16 frozen profile is a **manufacturing/review master**, not the final Meta-specific delivery profile.

## Current frozen output versus project target

| Property | Frozen C11-C 2.16 | Meta final target |
|---|---|---|
| Container | MP4 | MP4 |
| Aspect | 9:16 | 9:16 |
| Resolution | 720×1280 | 1080×1920 |
| FPS | 30 fixed | 30 fixed |
| Duration | C11-C-specific; Longform internal | ≤90 s for the supplied Facebook Reels target |
| Video codec | H.264 | H.264 |
| Chroma | yuv420p / 4:2:0 | 4:2:0 |
| GOP | not explicitly closed 2–5 s in frozen encoder | explicit closed 3 s |
| Audio bitrate | 192 kbps on Loop path; 128 kbps on older Drill review path | 192 kbps target |
| Channels | stereo | stereo |
| AAC profile | not explicitly forced to AAC-LC | AAC-LC |
| Sample rate | 44.1 kHz | 48 kHz |
| Progressive | encoder path | progressive |

## Conclusion

The frozen files satisfy the supplied minimum 540×960 resolution and the core vertical H.264/yuv420p/30-FPS delivery shape. They do **not** match the recommended 1080×1920 target, 48 kHz audio target or explicit closed-GOP target.

The correct engineering choice is an additive `META_REELS_FINAL_V1` delivery profile rather than reopening the frozen C11-C review master. The final profile should render at 1080×1920 directly where possible; a 720→1080 upscale is a diagnostic fallback, not the canonical final render.

Meta's current public Reels guidance emphasizes vertical 9:16 creative, audio and keeping key creative elements within the Reels safe zone. The detailed encoding table used here is maintained as the project's technical target and should be checked against the live Meta Ads Guide before final release.


## Verification note

The frozen C11-C review master remains 720×1280 / 30 FPS. It is intentionally not rewritten merely to match the final Meta delivery profile.

The current Meta for Business Reels guidance emphasizes vertical 9:16 creative, audio and keeping key messaging within the safe zone, and links creators to Meta's Video Ads Guide for specifications. See: https://www.facebook.com/business/ads-guide.

For a final Meta delivery profile we require an explicit encoder contract for 1080×1920, H.264/yuv420p, fixed 30 FPS, closed 3-second GOP, AAC-LC, 48 kHz stereo and 192 kbps audio.
