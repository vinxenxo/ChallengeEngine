shader_type canvas_item;

// C6-F0.8-D4: Contract Parameters from Logical Layer State
uniform float flow_angle = 0.0;
uniform float turbulence = 0.0;
uniform float grid_density = 10.0;
uniform float global_rotation = 0.0;
uniform float zoom = 1.0;
uniform vec4 base_color : source_color = vec4(0.8, 0.3, 0.5, 1.0);

// Basic 2D pseudo-random based on UV
float random(vec2 uv) {
    return fract(sin(dot(uv.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

void fragment() {
    // 1. Centrar UV y aplicar geometría básica
    vec2 uv = UV - 0.5;
    
    // 2. Global Transform (Rotación + Zoom)
    float s = sin(global_rotation);
    float c = cos(global_rotation);
    uv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);
    uv *= (1.0 / max(zoom, 0.001));
    
    // 3. Grid Quantization (para crear las "celdas" del campo)
    vec2 grid_uv = fract(uv * grid_density) - 0.5;
    vec2 cell_id = floor(uv * grid_density);
    
    // 4. Vector math per cell
    // Generar un offset procedural por celda mezclado con el flow_angle
    float cell_rand = random(cell_id) * turbulence;
    float local_angle = flow_angle + cell_rand;
    vec2 flow_dir = vec2(cos(local_angle), sin(local_angle));
    
    // 5. Dibujar la flecha/línea del vector
    // Proyección del píxel local sobre la dirección del vector
    float projection = dot(grid_uv, flow_dir);
    float line_dist = abs(dot(grid_uv, vec2(-flow_dir.y, flow_dir.x)));
    
    // Antialiasing pseudo-analítico para la línea
    float line_mask = smoothstep(0.05, 0.03, line_dist);
    // Acotar la línea al centro de la celda
    line_mask *= smoothstep(0.4, 0.3, abs(projection));
    
    // Añadir una "cabeza" direccional simple
    float head_mask = smoothstep(0.1, 0.05, length(grid_uv - flow_dir * 0.2));
    
    float final_mask = max(line_mask, head_mask);
    
    COLOR = vec4(base_color.rgb, final_mask * base_color.a);
}