shader_type canvas_item;

// C6-F0.8-E3: Pursuit Drill Shader Contract
uniform float pursuit_variant = 0.0;
uniform float progress = 0.0;
uniform vec2 stimulus_pos = vec2(0.5, 0.5);
uniform vec4 base_color : source_color = vec4(0.9, 0.4, 0.2, 1.0);

void fragment() {
    vec2 uv = UV;
    float dist = distance(uv, stimulus_pos);
    
    // Patrón de persecución dinámico modulado por pursuit_variant
    float wave = sin(dist * (20.0 + pursuit_variant * 10.0) - progress * TAU * 3.0);
    float core = smoothstep(0.08, 0.02, dist);
    float halo = smoothstep(0.2, 0.1, dist) * abs(wave);
    
    float alpha = max(core, halo);
    COLOR = vec4(base_color.rgb, alpha * base_color.a);
}