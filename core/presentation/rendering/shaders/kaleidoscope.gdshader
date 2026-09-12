shader_type canvas_item;

// C6-F0.8-D6: Contract Parameters from Logical Layer State
uniform float rotation_angle = 0.0;
uniform float symmetry_folds = 6.0;
uniform float zoom = 1.0;
uniform vec4 base_color : source_color = vec4(0.9, 0.2, 0.2, 1.0);

void fragment() {
    vec2 uv = UV - 0.5;
    uv *= (1.0 / max(zoom, 0.001));
    
    // Transformación a coordenadas polares
    float r = length(uv);
    float a = atan(uv.y, uv.x) + rotation_angle;
    
    // Plegado simétrico caleidoscópico
    float segment = TAU / max(symmetry_folds, 1.0);
    a = mod(a, segment);
    a = abs(a - segment * 0.5);
    
    // Reconstrucción cartesiana simétrica
    vec2 p = vec2(cos(a), sin(a)) * r;
    
    // Padrón geométrico interno basado en interferencia armónica
    float pattern = sin(p.x * 20.0 + rotation_angle) * cos(p.y * 20.0 - rotation_angle);
    float mask = smoothstep(0.4, 0.1, r) * abs(pattern);
    
    COLOR = vec4(base_color.rgb * (0.5 + 0.5 * pattern), mask * base_color.a);
}