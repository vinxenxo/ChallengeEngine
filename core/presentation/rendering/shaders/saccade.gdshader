shader_type canvas_item;

// C6-F0.8-E4: Saccade Drill Shader Contract
uniform float saccade_variant = 0.0;
uniform float progress = 0.0;
uniform vec2 stimulus_pos = vec2(0.5, 0.5);
uniform vec4 base_color : source_color = vec4(0.8, 0.2, 0.9, 1.0);

void fragment() {
    vec2 uv = UV;
    float dist = distance(uv, stimulus_pos);
    
    float flash = step(0.5, sin(progress * TAU * (10.0 + saccade_variant * 5.0)));
    float core = smoothstep(0.12, 0.02, dist) * flash;
    float ring = smoothstep(0.25, 0.2, dist) * (1.0 - flash);
    
    float alpha = max(core, ring);
    COLOR = vec4(base_color.rgb, alpha * base_color.a);
}