shader_type canvas_item;

// C11-C.3 v1.6 — Sacred Symmetry visual grammar engine.
// Presentation-only. Exact radial symmetry is preserved within each grammar.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform int grammar_mode = 0;
uniform float segment_count = 12.0;
uniform float ring_bias = 0.55;
uniform float glow_strength = 0.72;
uniform float gear_inner = 2.0;
uniform float gear_outer = 1.0;
uniform float ring_scale = 1.0;
uniform float core_scale = 1.0;
uniform float tick_density = 1.0;
uniform float mechanical_rate = 1.5;
uniform float macro_scale = 1.0;
uniform float node_density = 1.0;
uniform float fold_depth = 1.0;
uniform float color_diversity = 0.82;
uniform float color_phase = 0.0;
uniform vec4 primary_color : source_color = vec4(0.70, 0.48, 0.17, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.86, 0.60, 0.24, 1.0);
uniform vec4 highlight_color : source_color = vec4(0.95, 0.78, 0.43, 1.0);
uniform vec4 white_gold_color : source_color = vec4(1.0, 0.95, 0.84, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float hash1(float x) {
    return fract(sin(x * 127.1 + seed_phase * 17.7) * 43758.5453);
}

float ring_line(float r, float radius, float width) {
    float aa = max(fwidth(r) * 1.7, 0.0011);
    return 1.0 - smoothstep(width, width + aa, abs(r - radius));
}

float line_angle(float a, float target, float width) {
    float d = abs(atan(sin(a - target), cos(a - target)));
    return 1.0 - smoothstep(width, width + max(fwidth(a), 0.0010), d);
}

float radial_line(vec2 p, float angle, float r0, float r1, float width) {
    float a = atan(p.y, p.x);
    float d = abs(atan(sin(a - angle), cos(a - angle)));
    float rr = length(p);
    float angular = 1.0 - smoothstep(width, width + 0.0012, d);
    float radial = step(r0, rr) * step(rr, r1);
    return angular * radial;
}

float polygon_edge(vec2 p, float sides, float radius, float width, float rotation) {
    float r = length(p);
    float a = atan(p.y, p.x) - rotation;
    float sector = C11C_TAU / sides;
    float local_a = mod(a + 0.5 * sector, sector) - 0.5 * sector;
    float boundary = radius * cos(0.5 * sector) / max(cos(local_a), 0.001);
    return ring_line(r, boundary, width);
}

float gear_teeth(vec2 p, float sides, float base_r, float tooth_depth, float width, float rotation) {
    float r = length(p);
    float a = atan(p.y, p.x) - rotation;
    float sector = C11C_TAU / sides;
    float cell = mod(a + 0.5 * sector, sector) - 0.5 * sector;
    float tooth = pow(max(0.0, cos(cell * sides)), 8.0);
    float target = base_r + tooth_depth * tooth;
    return ring_line(r, target, width);
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    p *= macro_scale;
    float r = length(p);
    float a = atan(p.y, p.x);

    float mech = 0.5 + 0.5 * sin(phase * mechanical_rate + seed_phase);
    float slow = 0.5 + 0.5 * cos(phase * 0.5 * gear_inner + seed_phase);
    float counter = 0.5 + 0.5 * cos(phase * 0.75 * gear_outer - seed_phase * 0.31);

    float sector = C11C_TAU / max(segment_count, 1.0);
    float symmetry_angle = mod(a, sector);
    symmetry_angle = abs(symmetry_angle - 0.5 * sector);

    float structure = 0.0;
    float secondary = 0.0;
    float nodes = 0.0;
    float core = exp(-r * 22.0 / max(core_scale, 0.2));

    if (grammar_mode == 0) {
        // ASTROLABE — precision rings/axes/orbital markers.
        float r0 = 0.078 * ring_scale;
        float r1 = 0.152 * ring_scale;
        float r2 = 0.236 * ring_scale;
        float r3 = 0.322 * ring_scale;
        float r4 = 0.412 * ring_scale;
        structure += ring_line(r, r0, 0.0020);
        structure += ring_line(r, r1, 0.0020);
        structure += ring_line(r, r2, 0.0021);
        structure += ring_line(r, r3, 0.0022);
        structure += ring_line(r, r4, 0.0020);
        structure += radial_line(p, 0.0 + phase * 0.05 * gear_outer, 0.055, r4, 0.0035) * 0.72;
        structure += radial_line(p, 0.5 * C11C_PI + phase * 0.05 * gear_outer, 0.055, r4, 0.0035) * 0.72;
        for (int i = 0; i < 64; i++) {
            if (float(i) < segment_count * 4.0 * tick_density) {
                float ang = C11C_TAU * float(i) / max(segment_count * 4.0 * tick_density, 1.0) + phase * 0.12 * gear_outer;
                float tick_weight = 0.55;
                if (mod(float(i), 4.0) < 0.5) {
                    tick_weight = 1.0;
                }
                structure += radial_line(p, ang, 0.382, 0.423, 0.0065) * tick_weight;
            }
        }
        float orbit_a = a - phase * 0.11 * gear_outer;
        float orbit = 0.31 + 0.027 * sin(orbit_a * segment_count + phase * 0.45 * gear_inner);
        secondary += ring_line(r, orbit, 0.0028);
        nodes += exp(-abs(r - 0.31) * 76.0) * pow(max(0.5 + 0.5 * cos(segment_count * a - phase * 0.8 + seed_phase), 0.0), 14.0) * node_density;
    } else if (grammar_mode == 1) {
        // GEAR TRAIN — multiple exact radial gear profiles at integer/fractional rotational ratios.
        float rot_a = phase * 0.11 * gear_outer;
        float rot_b = -phase * 0.055 * gear_inner;
        structure += gear_teeth(p, segment_count, 0.14 * ring_scale, 0.030, 0.0020, rot_a) * 1.1;
        structure += gear_teeth(p, segment_count, 0.29 * ring_scale, 0.038, 0.0021, rot_b) * 0.92;
        structure += gear_teeth(p, segment_count, 0.405 * ring_scale, 0.018, 0.0020, rot_a * -0.5) * 0.72;
        structure += ring_line(r, 0.07 * core_scale, 0.0022);
        structure += ring_line(r, 0.23 * ring_scale, 0.0016);
        for (int i = 0; i < 32; i++) {
            if (float(i) < segment_count * 2.0) {
                float ang = C11C_TAU * float(i) / max(segment_count * 2.0, 1.0) + rot_a;
                structure += radial_line(p, ang, 0.10, 0.42, 0.0052) * 0.46;
            }
        }
        nodes += exp(-r * 36.0) * node_density * (0.6 + 0.4 * mech);
    } else if (grammar_mode == 2) {
        // POLYGON ORRERY — regular polygons orbit as exact symmetrical bodies.
        float rot_a = phase * 0.09 * gear_outer;
        float rot_b = -phase * 0.045 * gear_inner;
        structure += polygon_edge(p, segment_count, 0.16 * ring_scale, 0.0020, rot_a) * 1.12;
        structure += polygon_edge(p, segment_count, 0.27 * ring_scale, 0.0020, rot_b) * 0.94;
        structure += polygon_edge(p, segment_count, 0.405 * ring_scale, 0.0018, rot_a * -0.5) * 0.72;
        structure += ring_line(r, 0.065 * core_scale, 0.0020);
        for (int i = 0; i < 24; i++) {
            if (float(i) < segment_count * 2.0) {
                float ang = C11C_TAU * float(i) / max(segment_count * 2.0, 1.0) + rot_a;
                float rr = 0.20 + 0.13 * (0.5 + 0.5 * sin(float(i) * 1.7 + seed_phase));
                nodes += radial_line(p, ang, rr - 0.018, rr + 0.018, 0.0072) * node_density;
            }
        }
    } else if (grammar_mode == 3) {
        // ORIGAMI MANDALA — mirrored folds, diamonds and stepped opening without organic noise.
        float fold_phase = 0.5 + 0.5 * sin(phase * 0.85 + seed_phase);
        float fold_r = 0.12 + 0.13 * fold_phase * fold_depth;
        float fold_line = line_angle(a, 0.5 * C11C_PI / segment_count, 0.009);
        float mirror_line = line_angle(a, 1.5 * C11C_PI / segment_count, 0.006);
        structure += ring_line(r, fold_r, 0.0023);
        structure += ring_line(r, fold_r * 1.56, 0.0019);
        structure += fold_line * smoothstep(0.05, 0.43, r) * 0.95;
        structure += mirror_line * smoothstep(0.09, 0.39, r) * 0.72;
        float diamond = 1.0 - smoothstep(0.0, 0.012, abs(cos(a * segment_count) * r - 0.215));
        structure += diamond * 0.40;
        nodes += pow(max(0.5 + 0.5 * cos(segment_count * a - phase * 0.55), 0.0), 20.0) * smoothstep(0.08, 0.34, r) * node_density;
    } else {
        // CELESTIAL CHART — sectors, orbital paths and exact radial points.
        float sector_lines = 1.0 - smoothstep(0.006, 0.012, symmetry_angle);
        float radial_window = smoothstep(0.06, 0.41, r) * (1.0 - smoothstep(0.42, 0.48, r));
        structure += sector_lines * radial_window * 0.62;
        structure += ring_line(r, 0.12 * ring_scale, 0.0018);
        structure += ring_line(r, 0.20 * ring_scale, 0.0018);
        structure += ring_line(r, 0.33 * ring_scale, 0.0020);
        structure += ring_line(r, 0.43 * ring_scale, 0.0018);
        float chart_wave = 0.5 + 0.5 * sin(segment_count * a + phase * gear_outer);
        float orbit_r = 0.285 + 0.055 * chart_wave;
        secondary += ring_line(r, orbit_r, 0.0018);
        nodes += exp(-abs(r - orbit_r) * 86.0) * pow(max(chart_wave, 0.0), 16.0) * node_density;
        for (int i = 0; i < 36; i++) {
            if (float(i) < segment_count * 3.0) {
                float ang = C11C_TAU * float(i) / max(segment_count * 3.0, 1.0) + phase * 0.08;
                structure += radial_line(p, ang, 0.395, 0.438, 0.0046) * 0.60;
            }
        }
    }

    // Shared exact-symmetry active highlights and contained glow.
    float align = pow(max(0.0, cos(symmetry_angle * segment_count)), 18.0);
    float mechanical_breath = 0.5 + 0.5 * sin(phase * mechanical_rate + seed_phase);
    structure = clamp(structure, 0.0, 1.0);
    secondary = clamp(secondary, 0.0, 1.0);

    // Exact-symmetry chromatic modulation: every sector repeats the same color field.
    float color_band = 0.5 + 0.5 * cos(segment_count * a + color_phase);
    float radial_band = 0.5 + 0.5 * cos(r * 38.0 - color_phase * 0.7);
    float color_mix = clamp(0.28 + color_diversity * (0.22 + 0.62 * color_band) + 0.08 * radial_band, 0.0, 1.0);
    vec3 gold = mix(primary_color.rgb, secondary_color.rgb, color_mix);
    gold = mix(gold, highlight_color.rgb, clamp(align * 0.55 + nodes * 0.20, 0.0, 1.0));
    gold = mix(gold, white_gold_color.rgb, clamp(nodes * 0.70 + core * 0.42, 0.0, 1.0));

    vec3 bg = vec3(0.008, 0.007, 0.006);
    bg += primary_color.rgb * (0.015 + 0.020 * smoothstep(0.52, 0.04, r));

    float vignette = smoothstep(0.62, 0.10, r);
    float glow = pow(core, 0.52) * (0.06 + 0.04 * mechanical_breath) + pow(nodes, 0.50) * 0.12;

    vec3 final_rgb = bg + gold * structure * (0.82 + 0.12 * counter);
    final_rgb += secondary_color.rgb * secondary * 0.30;
    final_rgb += white_gold_color.rgb * glow * glow_strength;
    final_rgb *= 0.92 + 0.08 * vignette;

    COLOR = vec4(clamp(final_rgb, 0.0, 1.0), 1.0);
}
