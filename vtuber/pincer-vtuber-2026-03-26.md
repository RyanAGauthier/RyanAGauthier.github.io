# Session Summary

**Date:** 2026-03-26

## Activities

### 1. Robot VTuber Model (`vtuber/index.html`)
- Created a web-based VTuber model matching a hand-drawn robot sketch (`robotpngtuber.png`)
- Character features: boxy 3D-perspective head/body, 3 spring-physics antennae, asymmetric eyes with pupils and blink, triangular beak/nose, left arm holding a draped cloth, right arm with 3-finger claw, chunky boots
- Rigging: full transform hierarchy (body > head > eyes/antennae, body > arms > hands), spring physics on antennae, idle breathing/sway/cloth ripple animations
- Tracking: MediaPipe Face Landmarker integration for head pose (yaw/pitch/roll), eye blink, eye gaze, mouth open/close
- Audio reactivity: Web Audio API microphone input as fallback or supplement for mouth movement
- UI: start/stop tracking, enable mic, green screen, transparent background (OBS-ready), webcam preview, sensitivity sliders, keyboard shortcuts

### 2. Crab Stack VTuber Model (`vtuber/crabs.html`)
- Created a second VTuber model featuring a stack of 3 crabs (bottom=large deep red, middle=medium orange-red, top=small bright orange)
- Each crab: dome shell with texture/highlights, two eye stalks with spring physics, two claws with opening/closing pincers (serrated edges), 6 walking legs with phased animation cycles
- Stacking behavior: top crab responds instantly to face tracking, middle crab follows with moderate delay, bottom crab follows with heavy delay — creates a cascading reaction effect
- Claw snapping tied to mouth open tracking (claws open when you talk)
- Ambient underwater bubble particles for atmosphere
- Same full control set as the robot model (tracking, mic, green screen, transparent, settings)

## Architecture Notes

Both models are single-file HTML applications with no build step. They use:
- **Canvas 2D** for rendering with hand-drawn wobbly line style (seeded random for frame consistency)
- **Spring physics** (custom Spring class) for organic secondary motion on appendages
- **MediaPipe Face Landmarker** (CDN) for 52-blendshape face tracking + head pose matrix
- **Web Audio API** analyser for voice-frequency audio reactivity
- Designed for **OBS Browser Source** usage with green screen and transparent background modes

## Files Created/Modified

| Path | Description |
|------|-------------|
| `vtuber/index.html` | Robot VTuber — rigged, face-tracked model matching the reference sketch |
| `vtuber/crabs.html` | Crab Stack VTuber — 3 stacked crabs with cascading tracking, claw snapping, walking legs |
| `sessions/pincer-vtuber-2026-03-26.md` | This session summary |
