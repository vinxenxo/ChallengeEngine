shader_type canvas_item;

uniform float pattern_variant = 0.0;
uniform float amplitude_variant = 0.5;
uniform float progress = 0.0;
uniform vec2 stimulus_pos = vec2(0.0, 0.0);
uniform vec4 base_color : source_color = vec4(0.2, 0.8, 0.6, 1.0);

void fragment() {
    vec2 uv = UV - 0.5;
    float dist = length(uv - stimulus_pos);
    float scan_ring = sin(dist * (10.0 + pattern_variant * 5.0) - progress * TAU * 2.0);
    float alpha = smoothstep(0.4, 0.1, dist) * abs(scan_ring) * amplitude_variant;
    
    COLOR = vec4(base_color.rgb, alpha * base_color.a);
}