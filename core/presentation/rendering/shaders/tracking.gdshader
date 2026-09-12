shader_type canvas_item;

// C6-F0.8-E2: Tracking Drill Shader Contract
uniform float tracking_variant = 0.0;
uniform float progress = 0.0;
uniform vec2 stimulus_pos = vec2(0.5, 0.5);
uniform vec4 base_color : source_color = vec4(0.2, 0.6, 1.0, 1.0);

void fragment() {
    vec2 uv = UV;
    float dist = distance(uv, stimulus_pos);
    
    // Anillo de seguimiento dinámico modulado por tracking_variant
    float radius = 0.15 + (tracking_variant * 0.05);
    float ring = smoothstep(radius + 0.02, radius, dist) - smoothstep(radius, radius - 0.02, dist);
    
    // Indicador central de estímulo
    float core = smoothstep(0.04, 0.02, dist);
    
    float alpha = max(ring, core);
    COLOR = vec4(base_color.rgb, alpha * base_color.a);
}