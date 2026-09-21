shader_type canvas_item;

// C11-C.1 — Geometric Waves v1 prototype.
// Presentation-only. No simulation state, RNG stream, or RenderedFrameStream access.
// All temporal motion is periodic in phase so phase(0) == phase(T) and phase'(0) == phase'(T).

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
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
uniform float layer_depth = 0.0;
uniform vec4 dominant_color : source_color = vec4(0.0, 0.82, 0.94, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.95, 0.08, 0.52, 1.0);
uniform vec4 highlight_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float polar_polygon_radius(float angle, float sides) {
    float segment = C11C_TAU / max(sides, 3.0);
    float local_angle = mod(angle + 0.5 * segment, segment) - 0.5 * segment;
    return cos(C11C_PI / sides) / max(cos(local_angle), 0.001);
}

float line_from_zero(float value, float width) {
    float w = max(width, 0.0005);
    float aa = max(fwidth(value) * 1.5, 0.0005);
    return 1.0 - smoothstep(w, w + aa, abs(value));
}

float contour_line(float value, float width) {
    float aa = max(fwidth(value) * 1.5, 0.0005);
    return 1.0 - smoothstep(width, width + aa, abs(value));
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;

    // A restrained breathing transform replaces ornamental constant rotation.
    float breathing_rotation = 0.11 * sin(phase + seed_phase * 0.37);
    float rs = sin(breathing_rotation);
    float rc = cos(breathing_rotation);
    p = vec2(p.x * rc - p.y * rs, p.x * rs + p.y * rc);
    float static_rotation = shape_rotation;
    float ssr = sin(static_rotation);
    float ccr = cos(static_rotation);
    p = vec2(p.x * ccr - p.y * ssr, p.x * ssr + p.y * ccr);

    // Three depth scales share the same mathematical vocabulary.
    float scales[3];
    scales[0] = 0.78;
    scales[1] = 1.00;
    scales[2] = 1.27;

    vec3 accumulated = vec3(0.0);
    float accumulated_alpha = 0.0;

    for (int i = 0; i < 3; i++) {
        float depth = float(i);
        float scale = scales[i] * (1.0 + layer_spread * (depth - 1.0) + 0.018 * sin(phase * 2.0 + seed_phase + depth));
        vec2 q = p / scale;

        float a = atan(q.y, q.x);
        float r = length(q);

        // Circle <-> polygon morph. The target shape itself is continuously perturbed
        // by harmonic radial waves rather than being redrawn as a rigid primitive.
        float polygon_r = polar_polygon_radius(a + 0.035 * sin(phase + seed_phase), polygon_sides);
        float radial_wave = radial_wave_amplitude * sin(6.0 * a + phase)
                          + 0.5 * radial_wave_amplitude * sin(10.0 * a - 2.0 * phase + seed_phase);
        float target_r = mix(0.34 + radial_wave, 0.34 * polygon_r + radial_wave, morph);

        float polygon_contour = contour_line(r - target_r, 0.0048);
        float second_contour = contour_line(r - (target_r + 0.052 + 0.012 * sin(phase * 2.0 + depth)), 0.0038);

        // Deformed orthogonal wave grid.
        vec2 grid_p = q;
        float grid_rot = 0.23 * sin(phase * 0.5 + depth + seed_phase * 0.2);
        float gs = sin(grid_rot);
        float gc = cos(grid_rot);
        grid_p = vec2(grid_p.x * gc - grid_p.y * gs, grid_p.x * gs + grid_p.y * gc);

        float gx = sin(wave_frequency * (grid_p.x + 0.032 * sin(phase + grid_p.y * 3.0)));
        float gy = sin((wave_frequency * wave_ratio) * (grid_p.y + 0.028 * sin(phase * 0.75 - grid_p.x * 4.0)));
        float grid_x = line_from_zero(gx, line_width * (1.0 + 0.16 * depth));
        float grid_y = line_from_zero(gy, line_width * (1.0 + 0.16 * depth));
        float grid = max(grid_x, grid_y) * 0.62;

        // Lissajous/interference contours create the transform bridge toward a mesh.
        float liss = sin(liss_x_frequency * q.x + phase)
                   + sin(liss_y_frequency * q.y - 2.0 * phase + seed_phase);
        float liss_lines = contour_line(liss, 0.065) * 0.48;

        float inter_a = sin(24.0 * interference_scale * (q.x * 0.89 + q.y * 0.46) + phase);
        float inter_b = sin(21.0 * interference_scale * (q.x * -0.52 + q.y * 0.84) - 1.5 * phase + seed_phase);
        float interference = line_from_zero(inter_a * inter_b, 0.055) * 0.34;

        float intersections = clamp((grid_x * grid_y * 1.8) + (polygon_contour * grid * 1.3), 0.0, 1.0);
        intersections = pow(intersections, 0.72);

        float edge_fade = 1.0 - smoothstep(0.37, 0.52, r);
        float depth_alpha = mix(0.30, 0.13, depth);

        float dominant_weight = clamp(
            polygon_contour * 0.95
            + second_contour * 0.42
            + grid * 0.82
            + interference * 0.65,
            0.0,
            1.0
        );

        float secondary_weight = clamp(liss_lines + (1.0 - dominant_weight) * 0.12, 0.0, 0.75);
        float highlight_weight = clamp(intersections * 1.65 + polygon_contour * 0.20, 0.0, 1.0);

        vec3 layer_color = mix(dominant_color.rgb, secondary_color.rgb, secondary_weight);
        layer_color = mix(layer_color, highlight_color.rgb, highlight_weight);

        float layer_alpha = (dominant_weight * 0.72 + secondary_weight * 0.32 + highlight_weight * glow_strength)
                          * edge_fade * depth_alpha;

        accumulated += layer_color * layer_alpha;
        accumulated_alpha += layer_alpha;
    }

    // Soft central convergence gives the composition a visual anchor without a sprite.
    float core = exp(-length(p) * 8.5);
    float core_rhythm = 0.72 + 0.28 * cos(phase * 2.0);
    accumulated += highlight_color.rgb * core * core_rhythm * 0.11;
    accumulated_alpha += core * 0.08;

    // Abyssal mathematical background / vignette.
    float vignette = smoothstep(0.80, 0.08, length(p));
    vec3 bg = vec3(0.018, 0.026, 0.055);
    bg += dominant_color.rgb * (0.035 * vignette);
    bg += secondary_color.rgb * (0.012 * (1.0 - vignette));

    vec3 final_rgb = bg + accumulated;
    final_rgb += highlight_color.rgb * pow(clamp(accumulated_alpha, 0.0, 1.0), 3.0) * 0.035 * glow_strength;

    COLOR = vec4(clamp(final_rgb, 0.0, 1.0), 1.0);
}
