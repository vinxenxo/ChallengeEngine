shader_type canvas_item;

// C6-F0.8-D5: Contract Parameters from Logical Layer State
uniform float time_cycle = 0.0;
uniform float dispersion = 0.0;
uniform float particle_count = 16.0;
uniform float global_rotation = 0.0;
uniform float zoom = 1.0;
uniform vec4 base_color : source_color = vec4(0.3, 0.9, 0.5, 1.0);

float rand(vec2 co){
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void fragment() {
    vec2 uv = UV - 0.5;
    
    float s = sin(global_rotation);
    float c = cos(global_rotation);
    uv = vec2(uv.x * c - uv.y * s, uv.x * s + uv.y * c);
    uv *= (1.0 / max(zoom, 0.001));
    
    float accum = 0.0;
    
    for(float i = 0.0; i < 64.0; i++) {
        if(i >= particle_count) break;
        
        float seed_x = rand(vec2(i, 1.0));
        float seed_y = rand(vec2(i, 2.0));
        vec2 p_origin = vec2(seed_x - 0.5, seed_y - 0.5) * dispersion;
        
        float speed_mult = 0.5 + rand(vec2(i, 3.0)) * 1.5;
        vec2 velocity = vec2(cos(time_cycle * speed_mult + i), sin(time_cycle * speed_mult + i)) * 0.3;
        vec2 p_pos = p_origin + velocity * mod(time_cycle * speed_mult, 1.0);
        
        float dist = length(uv - p_pos);
        float particle = smoothstep(0.04, 0.01, dist);
        accum += particle;
    }
    
    COLOR = vec4(base_color.rgb, clamp(accum, 0.0, 1.0) * base_color.a);
}