shader_type canvas_item;

// C6-F0.8-D7: Contract Parameters from Logical Layer State
uniform float rotation_angle = 0.0;
uniform float sides = 4.0;
uniform float zoom = 1.0;
uniform vec4 base_color : source_color = vec4(0.6, 0.3, 0.9, 1.0);

void fragment() {
    vec2 uv = UV - 0.5;
    uv *= (1.0 / max(zoom, 0.001));
    
    // Rotación
    float s = sin(rotation_angle);
    float c = cos(rotation_angle);
    uv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);
    
    // Distancia poligonal aproximada en coordenadas polares
    float a = atan(uv.y, uv.x);
    float r = length(uv);
    
    float segment = TAU / max(sides, 3.0);
    float d = cos(floor(0.5 + a / segment) * segment - a) * r;
    
    float shape_mask = smoothstep(0.3, 0.28, d);
    
    COLOR = vec4(base_color.rgb, shape_mask * base_color.a);
}