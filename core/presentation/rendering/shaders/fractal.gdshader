shader_type canvas_item;

// C6-F0.8-D2-C: Contract Parameters from Logical Layer State
uniform float zoom = 1.0;
uniform float rotation = 0.0;
uniform float phase = 0.0;
uniform float complexity = 1.0;
uniform vec4 base_color : source_color = vec4(0.2, 0.6, 0.9, 1.0);

void fragment() {
    // 1. Centrar UV
    vec2 uv = UV - 0.5;
    
    // 2. Aplicar rotación (matriz 2D)
    float s = sin(rotation);
    float c = cos(rotation);
    uv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);
    
    // 3. Aplicar zoom
    uv *= (1.0 / max(zoom, 0.001));
    
    // 4. Matemáticas de Fractal Procedural Simulado
    // Utilizamos phase y complexity para animar la topología de forma continua
    float d = length(uv);
    vec3 col = base_color.rgb * (0.5 + 0.5 * cos(phase + complexity * d * 10.0 + vec3(0.0, 2.0, 4.0)));
    
    // Atenuación suave en los bordes para integrarse en el content_rect
    float alpha = smoothstep(0.5, 0.4, d);
    
    COLOR = vec4(col, alpha * base_color.a);
}