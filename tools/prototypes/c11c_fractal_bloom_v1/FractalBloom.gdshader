shader_type canvas_item;

// C11-C.2 — Fractal Bloom v1 isolated presentation prototype.
// Presentation-only. No simulation state, RNG stream or RenderedFrameStream access.
// The entire time domain is driven by an externally supplied periodic phase.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform float color_phase = 0.0;
uniform float zoom_strength = 0.62;
uniform float warp_strength = 0.032;
uniform float bloom_strength = 0.72;
uniform float layer_softness = 0.82;
uniform float julia_x_bias = 0.0;
uniform float julia_y_bias = 0.0;
uniform float zoom_cycles = 1.0;
uniform float warp_frequency = 3.2;
uniform float layer_spread = 0.10;
uniform float breath_strength = 0.08;
uniform int grammar_mode = 0;
uniform float branch_density = 1.0;
uniform float detail_scale = 1.0;
uniform float spiral_amount = 1.0;
uniform float color_diversity = 0.90;
uniform vec4 background_color : source_color = vec4(0.0, 0.0, 0.0, 1.0);
uniform vec4 indigo_color : source_color = vec4(0.14, 0.13, 0.42, 1.0);
uniform vec4 violet_color : source_color = vec4(0.55, 0.24, 0.96, 1.0);
uniform vec4 cyan_color : source_color = vec4(0.10, 0.83, 0.93, 1.0);
uniform vec4 highlight_color : source_color = vec4(0.97, 0.99, 1.0, 1.0);

const float FB_PI = 3.14159265358979323846;
const float FB_TAU = 6.28318530717958647692;
const int FB_MAX_ITERS = 24;

mat2 rot(float a) {
    float s = sin(a);
    float c = cos(a);
    return mat2(vec2(c, -s), vec2(s, c));
}

float hash11(float p) {
    p = fract(p * 0.1031);
    p *= p + 33.33;
    p *= p + p;
    return fract(p);
}

vec2 cmul(vec2 a, vec2 b) {
    return vec2(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x);
}

vec2 cdiv(vec2 a, vec2 b) {
    float d = max(dot(b, b), 0.000001);
    return vec2(
        (a.x * b.x + a.y * b.y) / d,
        (a.y * b.x - a.x * b.y) / d
    );
}

vec4 fractal_field(vec2 p, float local_phase, float layer_scale, float iter_bias) {
    // Seeded Julia constant stays inside a restrained organic range.
    float s0 = hash11(seed_phase * 0.159154943 + 1.7);
    float s1 = hash11(seed_phase * 0.159154943 + 7.3);
    vec2 c = vec2(
        -0.19 + 0.18 * s0 + 0.018 * sin(local_phase * 1.0 + seed_phase),
        0.57 + 0.15 * s1 + 0.014 * cos(local_phase * 1.0 - seed_phase) + julia_y_bias
    );
    c.x += julia_x_bias;

    vec2 q = p * layer_scale;
    float q_radius = max(length(q), 0.0001);
    float q_angle = atan(q.y, q.x);
    if (grammar_mode == 1) {
        float tunnel_twist = spiral_amount * (0.58 + 0.24 * sin(local_phase * 1.0 + seed_phase));
        q = rot(tunnel_twist * log(q_radius + 0.055)) * q;
        q *= 0.92 + 0.14 * sin(local_phase * 1.0 + q_radius * 7.0);
    } else if (grammar_mode == 2) {
        q = rot(spiral_amount * (1.45 * log(q_radius + 0.045) + 0.15 * local_phase)) * q;
        q += 0.018 * vec2(cos(q_angle * 5.0 + local_phase), sin(q_angle * 5.0 - local_phase));
    } else if (grammar_mode == 3) {
        q = abs(q);
        q -= 0.028 * vec2(sin(local_phase + seed_phase), cos(local_phase * 1.0 - seed_phase));
        q *= detail_scale;
    } else if (grammar_mode == 4) {
        float nested = 0.5 + 0.5 * sin(log(q_radius + 0.035) * 5.5 + local_phase * 1.0);
        q = rot(0.34 * nested + spiral_amount * 0.22 * log(q_radius + 0.05)) * q;
        q *= 0.90 + 0.20 * nested;
    }

    float warp_a = sin(q.y * warp_frequency + local_phase * 1.0 + seed_phase * 0.20);
    float warp_b = cos(q.x * (warp_frequency * 0.84) - local_phase * 1.0 - seed_phase * 0.13);
    q += warp_strength * vec2(warp_a, warp_b);
    q = rot(0.035 * sin(local_phase + seed_phase)) * q;

    // Radial breathing makes the bloom feel alive without translating the nucleus.
    float rr = length(q);
    q *= 0.96 + breath_strength * cos(local_phase * 1.0 + rr * 4.0);

    vec2 z = q;
    float orbit = 10.0;
    float axis_trap = 10.0;
    float circle_trap = 10.0;
    float min_r2 = 10.0;
    float escaped_at = float(FB_MAX_ITERS);
    bool escaped = false;

    for (int i = 0; i < FB_MAX_ITERS; i++) {
        z = cdiv(cmul(z, z), vec2(1.0, 0.0)) + c;
        float zr = length(z);
        orbit = min(orbit, abs(z.x));
        orbit = min(orbit, abs(z.y));
        axis_trap = min(axis_trap, abs(z.x * z.y));
        circle_trap = min(circle_trap, abs(zr - 0.74));
        min_r2 = min(min_r2, dot(z, z));
        if (zr > 2.4 && !escaped) {
            escaped_at = float(i);
            escaped = true;
        }
        if (zr > 8.0) {
            break;
        }
    }

    float escape_soft = 1.0 - smoothstep(0.0, 2.5, escaped_at);
    float filament = exp(-42.0 * orbit);
    float branch_filament = exp(-58.0 * sqrt(max(axis_trap, 0.0)));
    float ring_filament = exp(-34.0 * circle_trap);

    float field = clamp(
        filament * 0.92 * branch_density + branch_filament * 0.52 * branch_density + ring_filament * 0.18,
        0.0,
        1.0
    );

    // Reject the filled interior and emphasize filamentary escape structure.
    float interior_guard = smoothstep(0.04, 0.22, length(q));
    field *= mix(0.42, 1.0, interior_guard);
    field *= mix(0.72, 1.16, escape_soft);

    float node_energy = pow(clamp(field, 0.0, 1.0), 2.2);
    float depth = exp(-layer_softness * rr * (0.65 + 0.10 * iter_bias));
    field *= depth;

    float organic_pulse = 0.82 + 0.18 * cos(local_phase * 1.0 + rr * 5.0);
    field *= organic_pulse;

    float chroma_wave = 0.5 + 0.5 * sin(color_phase + field * 5.7 + node_energy * 2.2);
    vec3 cold = mix(indigo_color.rgb, violet_color.rgb, clamp(field * 1.55, 0.0, 1.0));
    vec3 hot = mix(violet_color.rgb, cyan_color.rgb, clamp(field * 2.7 - 0.28, 0.0, 1.0));
    vec3 tertiary = mix(cyan_color.rgb, indigo_color.rgb, chroma_wave);
    vec3 colour = mix(mix(cold, hot, smoothstep(0.18, 0.76, field)), tertiary, color_diversity * 0.22);
    colour = mix(colour, highlight_color.rgb, node_energy * 0.78 * bloom_strength);

    float glow = pow(max(field, 0.0), 0.46) * 0.15 * bloom_strength;
    colour += highlight_color.rgb * glow;

    return vec4(colour * field, field + node_energy * 0.18);
}

void fragment() {
    vec2 uv = UV;
    vec2 p = (uv - vec2(0.5)) * vec2(540.0 / 672.0, 1.0);

    // Three-layer analytical zoom. No bitmap scrolling.
    float zoom_wave = 0.5 - 0.5 * cos(phase * zoom_cycles);
    float zoom_harm = 0.5 - 0.5 * cos(2.0 * phase * zoom_cycles);
    float zoom_path = zoom_wave;
    if (grammar_mode == 1) {
        zoom_path = 0.68 * zoom_wave + 0.32 * (0.5 - 0.5 * cos(3.0 * phase * zoom_cycles));
    } else if (grammar_mode == 2) {
        zoom_path = 0.54 * zoom_wave + 0.28 * zoom_harm + 0.18 * (0.5 + 0.5 * sin(phase * zoom_cycles));
    } else if (grammar_mode == 3) {
        zoom_path = 0.42 * zoom_wave + 0.58 * zoom_harm;
    } else if (grammar_mode == 4) {
        zoom_path = 0.76 * zoom_wave + 0.24 * (0.5 + 0.5 * sin(3.0 * phase * zoom_cycles + seed_phase));
    }
    // v1.8: zoom is a supporting motion, not the protagonist.
    // The recursive detail remains visible while the camera-like scale excursion stays restrained.
    float zoom_span = 0.24;
    if (grammar_mode == 1) {
        zoom_span = 0.34;
    } else if (grammar_mode == 2) {
        zoom_span = 0.40;
    } else if (grammar_mode == 3) {
        zoom_span = 0.16;
    } else if (grammar_mode == 4) {
        zoom_span = 0.52;
    }
    float zoom_activity = 1.0;
    if (grammar_mode == 3) {
        zoom_activity = 0.22;
    } else if (grammar_mode == 4) {
        zoom_activity = 0.55;
    } else if (grammar_mode == 2) {
        zoom_activity = 0.72;
    } else if (grammar_mode == 1) {
        zoom_activity = 0.84;
    }
    float zoom = exp((zoom_strength * zoom_activity) * zoom_span * (zoom_path - 0.5));

    vec3 accumulated = vec3(0.0);
    float accumulated_alpha = 0.0;

    float layer0_phase = phase + seed_phase * 0.06;
    float layer1_phase = phase * 2.0 + seed_phase * 0.10;
    float layer2_phase = phase * 3.0 + seed_phase * 0.16;

    vec2 p0 = rot(0.030 * sin(layer0_phase)) * p;
    vec2 p1 = rot(0.045 * sin(layer1_phase + 0.4)) * p;
    vec2 p2 = rot(0.065 * sin(layer2_phase - 0.7)) * p;

    // Deep roots: dim, broader and slower.
    vec4 f0 = fractal_field(p0 * zoom * 0.84 * (1.0 - layer_spread), layer0_phase, 0.92, 0.0);
    float a0 = f0.a * 0.42;
    accumulated += f0.rgb * vec3(0.82, 0.84, 1.0) * 0.80;
    accumulated_alpha += a0;

    // Hero bloom structure.
    vec4 f1 = fractal_field(p1 * zoom, layer1_phase, 1.0, 1.0);
    float a1 = f1.a * 0.94;
    accumulated += f1.rgb;
    accumulated_alpha += a1;

    // Active synapses: finer detail sampled at a slightly different phase/scale.
    vec4 f2 = fractal_field(p2 * zoom * 1.36 * (1.0 + layer_spread), layer2_phase, 1.16, 2.0);
    float a2 = f2.a * 0.62;
    accumulated += f2.rgb * 1.04;
    accumulated_alpha += a2;

    if (grammar_mode == 4) {
        vec2 nested_p = rot(phase + seed_phase * 0.05) * p * zoom * 1.95;
        vec4 f3 = fractal_field(nested_p, phase * 2.0 + seed_phase * 0.12, 1.0, 3.0);
        accumulated += f3.rgb * 0.42;
        accumulated_alpha += f3.a * 0.38;
    }

    // Central nucleus: luminous, restrained, never a filled disk.
    float r = length(p);
    float nucleus = exp(-r * 13.0);
    float nucleus_breath = 0.72 + 0.28 * cos(phase * 2.0 + seed_phase * 0.2);
    accumulated += highlight_color.rgb * nucleus * nucleus_breath * 0.075;
    accumulated_alpha += nucleus * 0.05;

    // Abyssal radial background.
    float vignette = 1.0 - smoothstep(0.20, 0.62, length(p));
    vec3 bg = background_color.rgb;
    bg += indigo_color.rgb * (0.045 * vignette);
    bg += violet_color.rgb * (0.012 * (1.0 - vignette));

    // Edge breathing prevents the whole Body from becoming equally bright.
    float edge_guard = 1.0 - smoothstep(0.43, 0.54, length(p));
    accumulated *= mix(0.62, 1.0, edge_guard);

    vec3 final_rgb = bg + accumulated;
    final_rgb += highlight_color.rgb * pow(clamp(accumulated_alpha, 0.0, 1.0), 3.0) * 0.045 * bloom_strength;

    COLOR = vec4(clamp(final_rgb, 0.0, 1.0), 1.0);
}
