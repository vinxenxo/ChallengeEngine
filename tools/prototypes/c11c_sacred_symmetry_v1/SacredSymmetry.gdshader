shader_type canvas_item;

// C11-C.3 — Sacred Symmetry v1. Presentation-only procedural astrolabe.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform float segment_count = 12.0;
uniform float ring_bias = 0.55;
uniform float glow_strength = 0.72;
uniform float gear_inner = 2.0;
uniform float gear_outer = 1.0;
uniform vec4 primary_color : source_color = vec4(0.70, 0.48, 0.17, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.86, 0.60, 0.24, 1.0);
uniform vec4 highlight_color : source_color = vec4(0.95, 0.78, 0.43, 1.0);
uniform vec4 white_gold_color : source_color = vec4(1.0, 0.95, 0.84, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float ring_line(float r, float radius, float width) {
    float aa = max(fwidth(r) * 1.8, 0.0012);
    return 1.0 - smoothstep(width, width + aa, abs(r - radius));
}

float radial_line(vec2 p, float angle, float radius, float length_px) {
    float a = atan(p.y, p.x);
    float d = abs(atan(sin(a - angle), cos(a - angle)));
    float rr = length(p);
    float radial = 1.0 - smoothstep(0.0, 0.0045, d);
    float segment = step(rr, radius) * step(radius - length_px, rr);
    return radial * segment;
}

float periodic_hash(float x) {
    return fract(sin(x * 127.1 + seed_phase * 17.7) * 43758.5453);
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    float r = length(p);
    float a = atan(p.y, p.x);

    float mech = 0.5 + 0.5 * sin(phase);
    float slow = 0.5 + 0.5 * cos(phase * 0.5 * gear_inner + seed_phase);
    float counter = 0.5 + 0.5 * cos(phase * 0.75 - seed_phase * 0.31);

    float symmetry_angle = mod(a + 0.13 * sin(phase * 0.5 * gear_inner + seed_phase), C11C_TAU / segment_count);
    symmetry_angle = abs(symmetry_angle - 0.5 * C11C_TAU / segment_count);

    float core = exp(-r * 19.0);
    float micro_core = exp(-r * 42.0);

    float rings = 0.0;
    float ring_radii[5];
    ring_radii[0] = 0.075;
    ring_radii[1] = 0.145 + 0.010 * ring_bias;
    ring_radii[2] = 0.225;
    ring_radii[3] = 0.315 + 0.008 * sin(seed_phase);
    ring_radii[4] = 0.405;
    for (int i = 0; i < 5; i++) {
        float pulse = 0.0025 * sin(phase * (0.72 + 0.12 * float(i)) * gear_inner + float(i) + seed_phase);
        rings += ring_line(r, ring_radii[i] + pulse, 0.0020 + 0.0008 * float(i));
    }

    float sectors = 1.0 - smoothstep(0.009, 0.015, symmetry_angle);
    float spoke_gate = smoothstep(0.06, 0.39, r) * (1.0 - smoothstep(0.40, 0.48, r));
    float spokes = sectors * spoke_gate;

    float ticks = 0.0;
    float tick_count = segment_count * 4.0;
    for (int i = 0; i < 48; i++) {
        if (float(i) < tick_count) {
            float ang = C11C_TAU * float(i) / tick_count + phase * (0.18 + 0.04 * sin(seed_phase)) * gear_outer;
            ticks += radial_line(p, ang, 0.416, 0.020 + 0.012 * step(0.0, 0.5 - mod(float(i), 4.0)));
        }
    }

    float orbit_angle = a - phase * 0.16 * gear_outer;
    float orbit_radius = 0.30 + 0.035 * sin(orbit_angle * segment_count + phase * 0.5 * gear_inner + seed_phase);
    float orbit = ring_line(r, orbit_radius, 0.0024);
    float orbit2 = ring_line(r, 0.265 + 0.018 * cos(orbit_angle * 2.0 - phase), 0.0018);

    float node_pattern = 0.5 + 0.5 * cos(segment_count * a - phase * 0.8 + seed_phase);
    float nodes = exp(-abs(r - 0.314) * 70.0) * pow(max(node_pattern, 0.0), 14.0);
    nodes += exp(-abs(r - 0.225) * 72.0) * pow(max(0.5 + 0.5 * cos(segment_count * a + phase + seed_phase * 0.6), 0.0), 18.0) * 0.72;

    float blade = exp(-abs(symmetry_angle - 0.5 * C11C_TAU / segment_count * 0.55) * 42.0);
    float blade_mask = smoothstep(0.08, 0.42, r) * (1.0 - smoothstep(0.44, 0.50, r));
    float mechanical_breath = 0.5 + 0.5 * sin(phase * 1.5 + seed_phase);
    float structure = rings * 0.95 + spokes * 0.24 + ticks * 0.78 + orbit * 0.55 + orbit2 * 0.34 + nodes * 1.4 + blade * blade_mask * (0.12 + 0.08 * mechanical_breath);
    structure = clamp(structure, 0.0, 1.0);

    vec3 gold = mix(primary_color.rgb, secondary_color.rgb, 0.5 + 0.5 * slow);
    gold = mix(gold, highlight_color.rgb, clamp(ticks * 0.42 + rings * 0.18, 0.0, 1.0));
    gold = mix(gold, white_gold_color.rgb, clamp(nodes * 0.86 + micro_core * 0.55, 0.0, 1.0));

    vec3 bg = vec3(0.014, 0.012, 0.018);
    bg += primary_color.rgb * (0.020 + 0.018 * smoothstep(0.52, 0.05, r));
    bg += secondary_color.rgb * (0.008 * slow);

    float vignette = smoothstep(0.58, 0.10, r);
    float glow = pow(core, 0.55) * (0.08 + 0.04 * mech) + pow(micro_core, 0.42) * 0.11;
    vec3 final_rgb = bg + gold * structure * (0.82 + 0.12 * counter);
    final_rgb += white_gold_color.rgb * glow * glow_strength;
    final_rgb *= 0.90 + 0.10 * vignette;

    COLOR = vec4(clamp(final_rgb, 0.0, 1.0), 1.0);
}
