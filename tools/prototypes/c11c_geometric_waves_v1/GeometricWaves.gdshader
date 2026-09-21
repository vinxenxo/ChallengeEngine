shader_type canvas_item;

// C11-C.1 v1.5 — Geometric Waves as a family of wave phenomena.
// Presentation-only. No simulation state, RNG stream, or RenderedFrameStream access.
// Five deterministic grammar modes replace the previous circle-wobble default.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform int grammar_mode = 0;
uniform int palette_mode = 0;
uniform float morph = 0.5;
uniform float wave_frequency = 18.0;
uniform float line_width = 0.008;
uniform float glow_strength = 0.62;
uniform float polygon_sides = 6.0;
uniform float wave_ratio = 0.83;
uniform float shape_rotation = 0.0;
uniform float layer_spread = 0.030;
uniform float radial_wave_amplitude = 0.024;
uniform float liss_x_frequency = 8.0;
uniform float liss_y_frequency = 5.0;
uniform float interference_scale = 1.0;
uniform float hero_scale = 0.96;
uniform float perspective_strength = 0.72;
uniform float depth_strength = 0.72;
uniform float secondary_phase = 0.0;
uniform float color_phase = 0.0;
uniform float stroke_scale = 1.0;

uniform vec4 dominant_color : source_color = vec4(0.0, 0.82, 0.94, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.95, 0.08, 0.52, 1.0);
uniform vec4 highlight_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float line_from_zero(float value, float width) {
    float w = max(width * stroke_scale, 0.0005);
    float aa = max(fwidth(value) * 1.5, 0.0005);
    return 1.0 - smoothstep(w, w + aa, abs(value));
}

float contour_line(float value, float width) {
    float w = max(width * stroke_scale, 0.0005);
    float aa = max(fwidth(value) * 1.5, 0.0005);
    return 1.0 - smoothstep(w, w + aa, abs(value));
}

vec2 rotate2(vec2 p, float a) {
    float s = sin(a);
    float c = cos(a);
    return vec2(p.x * c - p.y * s, p.x * s + p.y * c);
}

vec4 field_harmonic_membrane(vec2 q, float local_phase, float layer) {
    float fx = wave_frequency * mix(0.78, 1.24, 0.50 + 0.50 * sin(seed_phase + secondary_phase));
    float fy = fx * wave_ratio;
    float view = 1.0 / max(0.58, 1.0 - q.y * perspective_strength * 0.60);
    vec2 s = vec2(q.x * view, q.y);

    float h = 0.56 * sin(fx * s.x + local_phase)
            + 0.44 * cos(fy * s.y - local_phase * 0.73 + seed_phase);
    h += 0.22 * sin((fx * 0.43) * (s.x + s.y) + local_phase * 1.31);

    // Optical projection of a height field: vertical displacement + perspective shear.
    vec2 d = s + vec2(h * 0.042 * perspective_strength, h * 0.024 * perspective_strength);

    float gx = sin((fx * 0.98) * (d.x + h * 0.032) + local_phase);
    float gy = sin((fy * 1.04) * (d.y + h * 0.026) - local_phase * 0.63 + seed_phase);
    float grid_x = line_from_zero(gx, 0.052);
    float grid_y = line_from_zero(gy, 0.052);

    float contour = contour_line(sin(h * 7.4 + local_phase * 0.28), 0.075) * 0.86;
    float ridges = contour_line(h, 0.13) * 0.34;
    float nodes = pow(clamp(grid_x * grid_y * 2.6, 0.0, 1.0), 0.72);
    float depth = 0.52 + 0.48 * h;

    float energy = clamp(grid_x * 0.62 + grid_y * 0.62 + contour * 0.65 + ridges, 0.0, 1.0);
    float highlight = clamp(nodes * 1.5 + contour * 0.20, 0.0, 1.0);
    return vec4(energy, highlight, depth, 1.0);
}

vec4 field_interference_plane(vec2 q, float local_phase, float layer) {
    vec2 r = rotate2(q, shape_rotation + 0.10 * sin(local_phase * 0.5 + seed_phase));
    float f1 = wave_frequency * 0.82;
    float f2 = wave_frequency * wave_ratio * 0.96;

    float a = sin(f1 * (r.x + 0.065 * sin(r.y * 5.0 + local_phase)) + local_phase);
    float b = sin(f2 * (r.y + 0.075 * sin(r.x * 4.0 - local_phase * 0.77)) - local_phase * 1.17 + seed_phase);
    float c = sin((r.x + r.y) * interference_scale * 15.0 + local_phase * 0.37 + secondary_phase);

    float rails_a = line_from_zero(a, 0.048);
    float rails_b = line_from_zero(b, 0.048);
    float nodes = pow(clamp(abs(a * b), 0.0, 1.0), 2.6);
    float moire = contour_line(a * b + 0.25 * c, 0.11) * 0.58;
    float diagonal = line_from_zero(c, 0.055) * 0.30;

    float energy = clamp(rails_a * 0.72 + rails_b * 0.72 + moire + diagonal, 0.0, 1.0);
    float highlight = clamp(nodes * 1.35 + rails_a * rails_b * 0.75, 0.0, 1.0);
    float depth = 0.56 + 0.44 * sin(r.x * 2.8 + r.y * 2.3 + local_phase);
    return vec4(energy, highlight, depth, 1.0);
}

vec4 field_parametric_ribbon(vec2 q, float local_phase, float layer) {
    float x = q.x * 2.15;
    float center = 0.18 * sin(2.35 * x + local_phase)
                 + 0.075 * sin(5.10 * x - local_phase * 1.41 + seed_phase);
    float width = 0.15 + 0.045 * sin(1.50 * x - local_phase * 0.62 + secondary_phase);
    float folded = 0.035 * sin(8.0 * x + local_phase * 1.7) * cos(x * 1.7);
    center += folded;

    float dy = abs(q.y - center);
    float outer = contour_line(dy - width, 0.010);
    float inner = contour_line(dy - width * 0.55, 0.008);

    float ribbon_u = (q.y - center) / max(width, 0.025);
    float cross = line_from_zero(sin(ribbon_u * 6.2 + x * 2.8 + local_phase), 0.058);
    float ribs = line_from_zero(sin(x * 11.0 + ribbon_u * 2.2 + local_phase * 0.65), 0.052);
    float depth = 0.5 + 0.5 * sin(x * 1.7 + local_phase * 0.42);

    float energy = clamp(outer * 0.98 + inner * 0.52 + cross * 0.32 + ribs * 0.22, 0.0, 1.0);
    float highlight = clamp(outer * 0.78 + inner * 0.28 + cross * 0.48, 0.0, 1.0);
    return vec4(energy, highlight, depth, 1.0);
}

vec4 field_lattice_wave(vec2 q, float local_phase, float layer) {
    vec2 r = rotate2(q, 0.18 * sin(local_phase * 0.37 + seed_phase));
    float h = 0.22 * sin(r.x * 8.0 + local_phase)
            + 0.18 * cos(r.y * 7.0 - local_phase * 0.82 + seed_phase);
    vec2 d = r + vec2(h * 0.10, -h * 0.08);
    float gx = sin((wave_frequency * 0.92) * d.x + 0.85 * sin(d.y * 5.0 + local_phase));
    float gy = sin((wave_frequency * wave_ratio * 0.86) * d.y + 0.85 * sin(d.x * 4.0 - local_phase));
    float mesh_x = line_from_zero(gx, 0.048);
    float mesh_y = line_from_zero(gy, 0.048);
    float diagonal = line_from_zero(sin((d.x + d.y) * 14.0 + local_phase), 0.052) * 0.25;
    float nodes = pow(clamp(mesh_x * mesh_y * 2.2, 0.0, 1.0), 0.70);
    float depth = 0.5 + 0.5 * h * 2.0;

    float energy = clamp(mesh_x * 0.68 + mesh_y * 0.68 + diagonal, 0.0, 1.0);
    float highlight = clamp(nodes * 1.55 + diagonal * 0.55, 0.0, 1.0);
    return vec4(energy, highlight, depth, 1.0);
}

vec4 field_orbital_wave(vec2 q, float local_phase, float layer) {
    float eccentricity = 0.22 + 0.10 * sin(seed_phase + 1.7);
    vec2 ep = vec2(q.x / (1.0 + eccentricity), q.y);
    float a = atan(ep.y, ep.x);
    float r = length(ep);
    float spiral = r + 0.055 * sin(3.0 * a - local_phase * 0.73);
    float wave = sin((wave_frequency * 0.70) * spiral - 2.6 * a + local_phase);
    float wave2 = sin((wave_frequency * 0.46) * (r * 1.26) + 4.0 * a - local_phase * 1.35 + seed_phase);
    float rails = line_from_zero(wave, 0.055);
    float secondary = line_from_zero(wave2, 0.058) * 0.62;
    float spiral_core = contour_line(sin(a * 5.0 + r * 13.0 - local_phase), 0.10) * 0.44;
    float node = rails * secondary;
    float energy = clamp(rails * 0.84 + secondary * 0.56 + spiral_core, 0.0, 1.0);
    float highlight = clamp(node * 1.8 + rails * 0.14, 0.0, 1.0);
    float depth = 0.5 + 0.5 * cos(a * 3.0 - local_phase * 0.3);
    return vec4(energy, highlight, depth, 1.0);
}

vec4 evaluate_field(vec2 q, float local_phase, float layer) {
    if (grammar_mode == 0) {
        return field_harmonic_membrane(q, local_phase, layer);
    }
    if (grammar_mode == 1) {
        return field_interference_plane(q, local_phase, layer);
    }
    if (grammar_mode == 2) {
        return field_parametric_ribbon(q, local_phase, layer);
    }
    if (grammar_mode == 3) {
        return field_lattice_wave(q, local_phase, layer);
    }
    return field_orbital_wave(q, local_phase, layer);
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    p /= max(hero_scale, 0.72);

    p = rotate2(p, shape_rotation + 0.035 * sin(seed_phase));

    vec3 accumulated = vec3(0.0);
    float accumulated_alpha = 0.0;
    float accumulated_highlight = 0.0;

    for (int i = 0; i < 3; i++) {
        float depth = float(i);
        float scale = 1.0 + layer_spread * (depth - 1.0);
        vec2 q = p / scale;
        float local_phase = phase * (1.0 + 0.13 * depth) + seed_phase * (0.31 + 0.17 * depth) + depth * secondary_phase;

        vec4 field = evaluate_field(q, local_phase, depth);
        float radial = length(q);
        float edge_fade = 1.0 - smoothstep(0.37, 0.55, radial);
        float depth_alpha = mix(0.20, 0.08, depth);
        depth_alpha *= mix(0.72, 1.0, depth_strength);

        float palette_mix = 0.30
            + 0.34 * sin(color_phase + depth * 0.8 + field.z * 1.2)
            + 0.22 * field.z;
        palette_mix = clamp(palette_mix, 0.06, 0.94);

        vec3 layer_color = mix(dominant_color.rgb, secondary_color.rgb, palette_mix);
        layer_color = mix(layer_color, highlight_color.rgb, field.y * 0.90);

        float alpha = field.x * edge_fade * depth_alpha;
        accumulated += layer_color * alpha;
        accumulated_alpha += alpha;
        accumulated_highlight += field.y * alpha;
    }

    float convergence = exp(-length(p) * 9.5);
    accumulated += highlight_color.rgb * convergence * (0.04 + 0.04 * cos(phase * 2.0 + seed_phase));
    accumulated_alpha += convergence * 0.035;

    float vignette = smoothstep(0.80, 0.08, length(p));
    vec3 bg = vec3(0.018, 0.024, 0.052);
    bg += dominant_color.rgb * (0.028 * vignette);
    bg += secondary_color.rgb * (0.009 * (1.0 - vignette));

    float controlled_glow = clamp(glow_strength, 0.0, 1.0);
    vec3 final_rgb = bg + accumulated;
    final_rgb += highlight_color.rgb
        * pow(clamp(accumulated_highlight, 0.0, 1.0), 2.4)
        * (0.025 + 0.05 * controlled_glow);

    COLOR = vec4(clamp(final_rgb, 0.0, 1.0), 1.0);
}
