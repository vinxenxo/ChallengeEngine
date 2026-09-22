shader_type canvas_item;

// C11-C.4 v1.6 — Living Particles visual grammar engine.
// Presentation-only. Deterministic analytic particle ecology.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform int grammar_mode = 0;
uniform float particle_count = 144.0;
uniform float glow_strength = 0.78;
uniform vec2 attractor_a = vec2(-0.105, -0.035);
uniform vec2 attractor_b = vec2(0.130, 0.080);
uniform float swirl_bias = 1.0;
uniform float particle_spread = 1.0;
uniform float turbulence = 0.025;
uniform float attractor_strength = 1.0;
uniform float particle_size_scale = 1.0;
uniform float phase_rate = 1.0;
uniform float collision_strength = 1.0;
uniform float core_scale = 1.0;
uniform float density_bias = 1.0;
uniform float color_diversity = 0.82;
uniform float color_phase = 0.0;
uniform vec4 background_color : source_color = vec4(0.0, 0.0, 0.0, 1.0);
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

vec2 mode_position(float id, float local_phase) {
    vec2 h = hash2(id);
    float ang = C11C_TAU * h.x;
    float rad = 0.06 + 0.40 * pow(h.y, 0.68);
    vec2 p = rad * particle_spread * vec2(cos(ang), sin(ang));
    float cycle = fract(local_phase / C11C_TAU);

    if (grammar_mode == 0) {
        // SWARM — collective cloud with a gentle moving centroid.
        vec2 drift = 0.035 * vec2(sin(local_phase * 1.0 + seed_phase), cos(local_phase * 1.0 - seed_phase));
        p += drift * (0.35 + 0.65 * h.x);
        p = rotate2(p, 0.08 * sin(local_phase * 1.0 + h.x * C11C_TAU));
    } else if (grammar_mode == 1) {
        // VORTEX — particles orbit an attractor with radius-dependent angular velocity.
        vec2 center = attractor_a * 0.62;
        float turns = 0.22 + 0.95 * h.y;
        float radius = mix(0.035, 0.34 * particle_spread, h.y);
        float swirl_cycles = float(clamp(int(round(swirl_bias)), 1, 2));
        float theta = ang + local_phase * swirl_cycles;
        p = center + radius * vec2(cos(theta), sin(theta));
        p += attractor_b * 0.10 * sin(local_phase * 1.0 + h.x * C11C_TAU);
        p *= 0.92 + 0.08 * sin(C11C_TAU * cycle + h.x * C11C_TAU + seed_phase);
    } else if (grammar_mode == 2) {
        // COLLISION CLOUD — two populations converge, collide, deflect and separate.
        float side = step(0.5, h.x);
        vec2 left = vec2(-0.28, -0.02) + vec2(0.025, 0.035) * vec2(sin(local_phase + h.y * 7.0), cos(local_phase * 1.0 + h.x * 9.0));
        vec2 right = vec2(0.28, 0.02) + vec2(-0.025, 0.035) * vec2(sin(local_phase * 1.0 + h.y * 8.0), cos(local_phase * 1.0 + h.x * 11.0));
        vec2 source = mix(left, right, side);
        vec2 target = mix(right, left, side);
        float collide = smoothstep(0.10, 0.48, 0.5 + 0.5 * sin(C11C_TAU * cycle - C11C_PI * 0.5));
        vec2 q = mix(source, target, collide * 0.92);
        vec2 tangent = normalize(vec2(-(target - source).y, (target - source).x) + vec2(0.0001));
        q += tangent * sin(local_phase * 1.0 + h.x * C11C_TAU) * collide * collision_strength * 0.065;
        if (collide > 0.82) {
            vec2 away = normalize(q - vec2(0.0) + vec2(0.0001));
            q += away * (collide - 0.82) * 0.23 * collision_strength;
        }
        p = q + vec2((h.y - 0.5) * 0.09, (h.x - 0.5) * 0.05);
        p *= particle_spread * (0.92 + 0.16 * h.y);
    } else if (grammar_mode == 3) {
        // ORGANIC PULSE — a living central mass that breathes and sheds peripheral matter.
        float breath = 0.72 + 0.22 * sin(local_phase * 1.0 + seed_phase);
        float radius = mix(0.025, 0.31, pow(h.y, 0.95)) * (0.86 + 0.16 * breath);
        float radial_wave = 0.018 * sin(local_phase * 1.0 + h.x * C11C_TAU * 2.0 + radius * 16.0);
        p = vec2(cos(ang), sin(ang)) * (radius + radial_wave);
        p *= particle_spread;
        p += 0.045 * vec2(sin(local_phase * 1.0), cos(local_phase * 1.0)) * (1.0 - h.y);
    } else {
        // MAGNETIC FILAMENT CLOUD — density follows a soft dipolar/curling field.
        vec2 da = p - attractor_a;
        vec2 db = p - attractor_b;
        float wa = exp(-dot(da, da) * 17.0);
        float wb = exp(-dot(db, db) * 15.0);
        vec2 va = vec2(-da.y, da.x) * wa * 1.55 * attractor_strength;
        vec2 vb = vec2(db.y, -db.x) * wb * 1.25 * attractor_strength;
        float mix_w = 0.5 + 0.5 * sin(local_phase * swirl_bias + id * 0.21);
        p += va * mix_w * 0.42 + vb * (1.0 - mix_w) * 0.42;
        p += turbulence * 2.2 * vec2(sin(5.0 * p.y + local_phase + id * 0.13), cos(4.0 * p.x - 0.8 * local_phase));
        p = rotate2(p, 0.12 * sin(local_phase * 1.0 + seed_phase));
    }

    // Shared soft-field turbulence; it never draws line geometry.
    p += turbulence * 0.85 * vec2(
        sin(3.7 * p.y + local_phase * 1.0 + id * 0.17),
        cos(3.2 * p.x - local_phase * 1.0 + id * 0.11)
    );
    return p;
}

float soft_blob(vec2 p, vec2 center, float size, float anisotropy, float angle) {
    vec2 q = rotate2(p - center, angle);
    q.x *= anisotropy;
    float d = length(q);
    return exp(-pow(d / max(size, 0.0001), 2.15));
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    float r = length(p);

    vec3 rgb = background_color.rgb;
    float density = 0.0;
    float hero = 0.0;
    float active_collision = 0.0;

    float master_breath = 0.84 + 0.16 * sin(phase * 1.0 + seed_phase);

    for (int i = 0; i < 180; i++) {
        if (float(i) < particle_count) {
            float id = float(i);
            vec2 h = hash2(id);
            float particle_phase = phase * phase_rate + C11C_TAU * hash1(id + 48.0);
            vec2 head = mode_position(id, particle_phase);

            float depth = hash1(id + 71.0);
            float size = particle_size_scale * mix(0.0033, 0.0105, depth) * (0.86 + 0.30 * hash1(id + 101.0));
            float anisotropy = mix(0.85, 1.85, hash1(id + 131.0));
            float particle_angle = particle_phase + hash1(id + 151.0) * C11C_TAU;
            float core = soft_blob(p, head, size, anisotropy, particle_angle);

            float halo = soft_blob(p, head, size * 2.8, 1.0, 0.0) * 0.22;
            float contribution = (core + halo) * (0.74 + 0.42 * depth) * density_bias;
            float warm_state = 0.5 + 0.5 * sin(particle_phase * 1.0 + id * 0.31 + seed_phase);

            float particle_color = fract(hash1(id + 401.0 + color_phase * 3.1) + 0.23 * warm_state);
            vec3 low_color = mix(deep_color.rgb, mid_color.rgb, smoothstep(0.0, 0.55, particle_color));
            vec3 high_color = mix(mid_color.rgb, bright_color.rgb, smoothstep(0.40, 1.0, particle_color));
            vec3 particle_color_rgb = mix(low_color, high_color, step(0.5, particle_color));
            particle_color_rgb = mix(mid_color.rgb, particle_color_rgb, color_diversity);

            vec3 c = mix(particle_color_rgb, bright_color.rgb, core * (0.36 + 0.30 * warm_state));
            c = mix(c, highlight_color.rgb, pow(core, 3.2) * 0.76);

            if (grammar_mode == 2) {
                active_collision += core * (0.50 + 0.50 * sin(phase + id));
                c = mix(c, highlight_color.rgb, pow(core, 2.0) * 0.48);
            }

            density += contribution;
            hero += core;
            rgb += c * contribution;
        }
    }

    vec2 ca = p - attractor_a;
    vec2 cb = p - attractor_b;
    float attractor_glow = exp(-dot(ca, ca) * 170.0) + 0.72 * exp(-dot(cb, cb) * 190.0);
    float core_glow = exp(-r * 15.0 / max(core_scale, 0.25));

    rgb += bright_color.rgb * attractor_glow * 0.045;
    rgb += highlight_color.rgb * pow(clamp(hero * 0.06, 0.0, 1.0), 1.8) * (0.11 + 0.10 * glow_strength);
    rgb += highlight_color.rgb * pow(clamp(active_collision * 0.018, 0.0, 1.0), 1.7) * 0.20;
    rgb += mid_color.rgb * core_glow * 0.012;

    float vignette = smoothstep(0.67, 0.10, r);
    rgb *= 0.92 + 0.08 * vignette;

    COLOR = vec4(clamp(rgb, 0.0, 1.0), 1.0);
}
