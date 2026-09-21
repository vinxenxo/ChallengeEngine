shader_type canvas_item;

// C11-C.5 — Invisible Forces v1. Analytic vector-field artwork.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform float trace_count = 32.0;
uniform float curvature = 0.86;
uniform float glow_strength = 0.84;
uniform float field_rotation = 0.0;
uniform vec2 storm_offset = vec2(0.0);
uniform float pulse_speed = 1.0;
uniform float field_twist = 1.0;
uniform float pulse_width = 1.0;
uniform float storm_scale = 1.0;
uniform vec4 deep_color : source_color = vec4(0.28, 0.03, 0.10, 1.0);
uniform vec4 primary_color : source_color = vec4(0.70, 0.15, 0.11, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.95, 0.32, 0.12, 1.0);
uniform vec4 highlight_color : source_color = vec4(1.0, 0.80, 0.35, 1.0);

const float C11C_PI = 3.14159265358979323846;
const float C11C_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float line_from_zero(float x, float width) {
    float aa = max(fwidth(x) * 1.6, 0.0010);
    return 1.0 - smoothstep(width, width + aa, abs(x));
}

float wrapped_angle(float a) {
    return atan(sin(a), cos(a));
}

float streamline(float a, float r, float base_angle, float t) {
    float radial = clamp((r - 0.06) / 0.40, 0.0, 1.0);
    float gravity = 0.62 / max(r + 0.045, 0.05);
    float warp = curvature * field_twist * (0.20 * sin(2.0*a - t) + 0.10 * sin(5.0*a + 1.4*t));
    float target = base_angle + 0.54 * radial + 0.08 * gravity + warp * (0.4 + 0.6*radial);
    return wrapped_angle(a - target);
}

void fragment() {
    vec2 p = UV - vec2(0.5);
    p.x *= BODY_ASPECT;
    float rs = sin(field_rotation);
    float rc = cos(field_rotation);
    p = vec2(p.x * rc - p.y * rs, p.x * rs + p.y * rc);
    p -= storm_offset * storm_scale;
    float r = length(p);
    float a = atan(p.y, p.x);

    float force_phase = phase * pulse_speed + 0.11 * sin(seed_phase);
    float outward_front = 0.5 + 0.5 * sin(force_phase * 1.15);
    float wind = 0.5 + 0.5 * sin(force_phase * 0.7 + a*2.0);

    vec3 rgb = vec3(0.012, 0.008, 0.012);
    float trace_energy = 0.0;

    // Potential contours: gravitational topography.
    float potential = r + 0.020 * sin(5.0*a - force_phase) / max(r + 0.12, 0.12);
    float contours = 0.0;
    for (int i = 1; i <= 8; i++) {
        float radius = 0.055 + 0.052 * float(i) + 0.008 * sin(force_phase + float(i));
        contours += line_from_zero(potential - radius, 0.0017 + 0.00025 * float(i));
    }

    // Streamline family. Each base angle is a deterministic field line.
    for (int i = 0; i < 96; i++) {
        if (float(i) < trace_count) {
            float fi = float(i);
            float base_angle = C11C_TAU * fi / trace_count + 0.10 * sin(fi * 2.1 + seed_phase);
            float d = streamline(a, r, base_angle, force_phase);
            float radial_gate = smoothstep(0.035, 0.075, r) * (1.0 - smoothstep(0.47, 0.51, r));
            float line = line_from_zero(d, 0.010 + 0.0025*(1.0-radial_gate));

            float phase_band = 0.5 + 0.5 * sin(force_phase * (0.95 + 0.01*fi) - fi*0.4 + r*11.0);
            float active = line * radial_gate * (0.22 + 0.78*phase_band);
            float pulse = exp(-abs(r - (0.09 + 0.32*mod(force_phase/C11C_TAU + fi*0.031 + 0.04*sin(seed_phase), 1.0))) * 95.0 * pulse_width);
            active += line * radial_gate * pulse * 0.28;

            vec3 c = mix(primary_color.rgb, secondary_color.rgb, 0.4 + 0.4*wind);
            c = mix(c, highlight_color.rgb, pow(line, 4.0) * (0.18 + 0.38*outward_front));
            rgb += c * active * (0.42 + 0.40*(1.0-r));
            trace_energy += active;
        }
    }

    float pulse_radius = 0.14 + 0.22 * (0.5 + 0.5*sin(force_phase));
    float pulse_ring = line_from_zero(r - pulse_radius, 0.0032);
    pulse_ring *= smoothstep(0.02, 0.10, r) * (1.0 - smoothstep(0.44, 0.50, r));

    float pole = exp(-r * 15.0);
    float node_wave = 0.5 + 0.5 * cos(12.0*a - force_phase*1.4);
    float energy_node = pole * pow(max(node_wave, 0.0), 20.0);

    vec3 bg = vec3(0.015, 0.009, 0.014);
    bg += deep_color.rgb * (0.020 + 0.022*smoothstep(0.55,0.04,r));
    rgb += bg;
    rgb += secondary_color.rgb * pulse_ring * 0.56;
    rgb += highlight_color.rgb * energy_node * 0.16 * glow_strength;
    rgb += highlight_color.rgb * pow(clamp(trace_energy * 0.035, 0.0, 1.0), 2.2) * 0.08 * glow_strength;
    rgb += deep_color.rgb * contours * 0.24;

    COLOR = vec4(clamp(rgb, 0.0, 1.0), 1.0);
}
