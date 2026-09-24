shader_type canvas_item;

uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_linear;
uniform vec2 focus_uv = vec2(0.5);
uniform float focus_strength = 0.82;
uniform float focus_radius = 0.16;
uniform float outer_radius = 0.62;
uniform float blur_px = 0.0024;

void fragment() {
    vec2 screen_uv = SCREEN_UV;
    float radial = smoothstep(focus_radius, outer_radius, distance(UV, focus_uv));
    float blur = clamp(radial * focus_strength, 0.0, 0.86);

    vec2 local_dir = normalize((UV - focus_uv) + vec2(0.0001));
    vec2 dir = vec2(local_dir.x, local_dir.y);
    vec2 px = vec2(blur_px);

    vec3 base = texture(screen_texture, screen_uv).rgb;
    vec3 sample_a = texture(screen_texture, screen_uv + dir * px * 1.0).rgb;
    vec3 sample_b = texture(screen_texture, screen_uv - dir * px * 1.5).rgb;
    vec3 sample_c = texture(screen_texture, screen_uv + vec2(-dir.y, dir.x) * px * 1.25).rgb;
    vec3 sample_d = texture(screen_texture, screen_uv + vec2(dir.y, -dir.x) * px * 1.25).rgb;
    vec3 blurred = base * 0.36 + sample_a * 0.16 + sample_b * 0.16 + sample_c * 0.16 + sample_d * 0.16;
    vec3 result = mix(base, blurred, blur);
    COLOR = vec4(result, 1.0);
}
