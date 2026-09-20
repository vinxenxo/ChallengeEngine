shader_type canvas_item;

// C11-C.4 — Living Particles v1. Analytic particle-flow artwork.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform float particle_count = 72.0;
uniform float trail_length = 0.12;
uniform float glow_strength = 0.78;
uniform vec2 attractor_a = vec2(-0.105, -0.035);
uniform vec2 attractor_b = vec2(0.130, 0.080);
uniform float swirl_bias = 1.0;
uniform vec4 deep_color : source_color = vec4(0.04, 0.28, 0.24, 1.0);
uniform vec4 mid_color : source_color = vec4(0.07, 0.71, 0.64, 1.0);
uniform vec4 bright_color : source_color = vec4(0.22, 0.90, 0.77, 1.0);
uniform vec4 highlight_color : source_color = vec4(0.84, 1.0, 0.96, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float hash1(float x) {
    return fract(sin(x * 127.1 + seed_phase * 19.3) * 43758.5453123);
}

vec2 hash2(float x) {
    return vec2(hash1(x + 1.7), hash1(x + 9.2));
}

vec2 rotate2(vec2 v, float a) {
    float s = sin(a);
    float c = cos(a);
    return vec2(v.x * c - v.y * s, v.x * s + v.y * c);
}

vec2 flow_position(float id, float local_phase) {
    vec2 h = hash2(id);
    float ang = C11C_TAU * h.x;
    float rad = 0.07 + 0.39 * pow(h.y, 0.72);
    vec2 p = rad * vec2(cos(ang), sin(ang));

    // Two attractors create a gentle magnetic dipole.
    
    vec2 da = p - attractor_a;
    vec2 db = p - attractor_b;
    float wa = exp(-dot(da, da) * 17.0);
    float wb = exp(-dot(db, db) * 15.0);
    vec2 va = vec2(-da.y, da.x) * wa * 1.45;
    vec2 vb = vec2(db.y, -db.x) * wb * 1.15;

    float swirl = 0.55 + 0.40 * sin(local_phase * swirl_bias + id * 0.21);
    p += va * swirl * 0.30 + vb * (1.0 - swirl) * 0.30;
    p += 0.025 * vec2(sin(5.0*p.y + local_phase + id*0.13), cos(4.0*p.x - 0.8*local_phase));
    p = rotate2(p, 0.08 * sin(local_phase * 0.5 + seed_phase));
    return p;
}

float segment_distance(vec2 p, vec2 a, vec2 b) {
    vec2 pa = p - a;
    vec2 ba = b - a;
    float denom = max(dot(ba, ba), 0.00001);
    float h = clamp(dot(pa, ba) / denom, 0.0, 1.0);
    return length(pa - ba * h);
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    float r = length(p);

    vec3 rgb = vec3(0.010, 0.022, 0.024);
    float density = 0.0;
    float hero = 0.0;

    float master_breath = 0.82 + 0.18 * sin(phase * 0.7 + seed_phase);

    for (int i = 0; i < 84; i++) {
        if (float(i) < particle_count) {
            float id = float(i);
            float particle_phase = phase * (0.82 + 0.24 * hash1(id + 22.0)) + C11C_TAU * hash1(id + 48.0);
            vec2 head = flow_position(id, particle_phase);
            vec2 tail = flow_position(id, particle_phase - trail_length);

            float depth = hash1(id + 71.0);
            float size = mix(0.0040, 0.0095, depth) * (0.90 + 0.25 * sin(particle_phase + id));
            float trail = 1.0 - smoothstep(size * 0.65, size * 3.6, segment_distance(p, tail, head));
            float core = 1.0 - smoothstep(size * 0.55, size * 2.0, length(p - head));
            trail *= 0.35 + 0.65 * (1.0 - depth);
            core *= 0.60 + 0.40 * master_breath;

            vec3 c = mix(deep_color.rgb, mid_color.rgb, 0.35 + 0.55 * depth);
            c = mix(c, bright_color.rgb, core * 0.88);
            c = mix(c, highlight_color.rgb, pow(core, 3.0) * 0.65);

            float contribution = max(trail * 0.36, core);
            density += contribution;
            hero += core;
            rgb += c * contribution * (0.34 + 0.82 * depth);
        }
    }

    vec2 ca = p - attractor_a;
    vec2 cb = p - attractor_b;
    float attractor_glow = exp(-dot(ca, ca) * 170.0) + 0.72 * exp(-dot(cb, cb) * 190.0);
    attractor_glow *= 0.10 + 0.05 * sin(phase * 1.3);

    float vignette = smoothstep(0.65, 0.10, r);
    rgb += deep_color.rgb * 0.08 * vignette;
    rgb += bright_color.rgb * attractor_glow;
    rgb += highlight_color.rgb * pow(clamp(hero * 0.09, 0.0, 1.0), 2.0) * 0.10 * glow_strength;

    COLOR = vec4(clamp(rgb, 0.0, 1.0), 1.0);
}
