shader_type canvas_item;

// C11-C.5 v1.7 — Invisible Forces visual grammar engine.
// Presentation-only. Multiple analytic field topologies; no simulation access.

uniform float phase = 0.0;
uniform float seed_phase = 0.0;
uniform int grammar_mode = 0;
uniform float trace_count = 68.0;
uniform float curvature = 0.86;
uniform float glow_strength = 0.72;
uniform float field_rotation = 0.0;
uniform vec2 storm_offset = vec2(0.0);
uniform float pulse_speed = 1.0;
uniform float field_twist = 1.0;
uniform float pulse_width = 1.0;
uniform float storm_scale = 1.0;
uniform float lens_strength = 0.65;
uniform float basin_depth = 0.72;
uniform float pole_separation = 0.24;
uniform float quadrupole_skew = 1.0;
uniform vec4 deep_color : source_color = vec4(0.25, 0.02, 0.04, 1.0);
uniform vec4 primary_color : source_color = vec4(0.70, 0.08, 0.05, 1.0);
uniform vec4 secondary_color : source_color = vec4(0.96, 0.27, 0.05, 1.0);
uniform vec4 highlight_color : source_color = vec4(1.0, 0.75, 0.20, 1.0);

const float IF_TAU = 6.28318530717958647692;
const float BODY_ASPECT = 540.0 / 672.0;

float line_from_zero(float x, float width) {
    float aa = max(fwidth(x) * 1.55, 0.0010);
    return 1.0 - smoothstep(width, width + aa, abs(x));
}

float wrapped_angle(float a) {
    return atan(sin(a), cos(a));
}

float dipole_scalar(vec2 p) {
    vec2 a = p - vec2(-pole_separation, 0.0);
    vec2 b = p - vec2(pole_separation, 0.0);
    float va = 0.10 / (length(a) + 0.055);
    float vb = 0.10 / (length(b) + 0.055);
    float bridge = 0.08 * p.y / (dot(p, p) + 0.05);
    return tanh((va - vb + bridge) * 1.62);
}

float saddle_scalar(vec2 p, float t) {
    float x = p.x;
    float y = p.y;
    float base = x * y * (10.0 * curvature);
    base += 0.035 * basin_depth * sin(5.0 * x + t) * cos(4.0 * y - 0.7 * t);
    return tanh(base);
}

float quadrupole_scalar(vec2 p, float t) {
    // v1.8: polynomial quadrupole avoids the atan/derivative path that can crash some Windows
    // compatibility drivers (seen as STATUS_CPP_EH_EXCEPTION / 0xC06D007F on seed 4).
    float x = p.x * max(quadrupole_skew, 0.72);
    float y = p.y;
    float denom = x * x + y * y + 0.045;
    float harmonic = (x * x - y * y) / denom;
    float cross = (2.0 * x * y) / denom;
    float q = harmonic + 0.075 * sin(t * 0.42) * cross;
    return tanh(q * 1.55);
}

float lens_scalar(vec2 p, float t) {
    // Gravitational-lens topology: parallel equipotentials bend around a central mass.
    float r2 = dot(p, p) + 0.028;
    float deflect = lens_strength * 0.085 / r2;
    float warped_y = p.y + p.y * deflect;
    float warped_x = p.x - p.x * deflect * 0.34;
    float ripple = 0.020 * sin(warped_x * 18.0 + t * 0.34);
    return tanh((warped_y + ripple) * 8.0);
}

float basin_scalar(vec2 p, float t) {
    float x = p.x * 1.34;
    float y = p.y * 0.78;
    float h = 0.50 * (x * x + y * y);
    h += basin_depth * (0.025 * sin(4.0 * x + t) + 0.018 * cos(5.0 * y - 0.8 * t));
    h += basin_depth * 0.012 * sin(3.0 * x + 4.0 * y + t * 0.55);
    return tanh((h - 0.075) * 7.0);
}

float field_scalar(vec2 p, float t) {
    if (grammar_mode == 0) {
        return dipole_scalar(p);
    }
    if (grammar_mode == 2) {
        return saddle_scalar(p, t);
    }
    if (grammar_mode == 3) {
        return quadrupole_scalar(p, t);
    }
    if (grammar_mode == 4) {
        return lens_scalar(p, t);
    }
    return basin_scalar(p, t);
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
    float t = phase * pulse_speed + 0.12 * sin(seed_phase);

    vec3 rgb = vec3(0.039, 0.020, 0.020);
    float trace_energy = 0.0;

    // Vortex is represented as logarithmic flow rails rather than circles.
    if (grammar_mode == 1) {
        float vortex_coord = wrapped_angle(a + field_twist * log(r + 0.045) * 1.55 - 0.16 * sin(t));
        for (int i = 0; i < 96; i++) {
            if (float(i) < trace_count) {
                float fi = float(i);
                float level = IF_TAU * fi / max(trace_count, 1.0) + 0.10 * sin(fi + seed_phase);
                float rail = 1.0 - smoothstep(0.009, 0.009 + max(fwidth(vortex_coord), 0.0012), abs(wrapped_angle(vortex_coord - level)));
                float pulse_pos = fract(a / IF_TAU + t * 0.035 + r * 1.7 + fi * 0.013);
                float pulse = exp(-abs(fract(pulse_pos + 0.5) - 0.5) * 34.0 * pulse_width);
                float active = rail * (0.20 + 0.80 * pulse);
                float valley = clamp(length(vec2(dFdx(vortex_coord), dFdy(vortex_coord))) * 0.45, 0.0, 1.0);
                vec3 c = mix(primary_color.rgb, secondary_color.rgb, 0.25 + 0.55 * (0.5 + 0.5 * sin(fi * 0.21 + seed_phase)));
                c = mix(c, highlight_color.rgb, pulse * (0.35 + 0.55 * valley));
                rgb += c * active * (0.30 + 0.42 * (1.0 - smoothstep(0.0, 0.55, r)));
                trace_energy += active;
            }
        }
    } else {
        float f = field_scalar(p, t);
        float gradient = clamp(length(vec2(dFdx(f), dFdy(f))) * 4.6, 0.0, 1.0);
        if (grammar_mode == 3) {
            gradient = clamp((abs(p.x) + abs(p.y)) * 1.65, 0.0, 1.0);
        }

        for (int i = 0; i < 96; i++) {
            if (float(i) < trace_count) {
                float fi = float(i);
                float u = fi / max(trace_count - 1.0, 1.0);
                float level = mix(-0.90, 0.90, u);
                float level_bias = 0.035 * sin(fi * 1.73 + seed_phase);
                float rail = line_from_zero(f - level - level_bias, 0.0062 + 0.0014 * (1.0 - gradient));

                float pulse_coord = fract(a / IF_TAU + t * (0.026 + 0.035 * gradient) + level * 0.11);
                float pulse = exp(-abs(fract(pulse_coord + 0.5) - 0.5) * (36.0 * pulse_width));
                float active = rail * (0.18 + 0.70 * pulse);

                vec3 c = mix(primary_color.rgb, secondary_color.rgb, 0.20 + 0.58 * u);
                c = mix(c, highlight_color.rgb, pulse * (0.34 + 0.52 * gradient));
                rgb += c * active * (0.28 + 0.52 * (1.0 - smoothstep(0.0, 0.58, r)));
                trace_energy += active;
            }
        }

        // A sparse set of equipotential guide contours gives the field measurable depth.
        float guide = 0.0;
        for (int j = 1; j <= 6; j++) {
            float lu = float(j) / 7.0;
            guide += line_from_zero(f - mix(-0.78, 0.78, lu), 0.0015) * 0.22;
        }
        rgb += deep_color.rgb * guide;
    }

    float central = exp(-r * 13.0);
    float storm = exp(-dot(p - storm_offset, p - storm_offset) * (32.0 / max(storm_scale, 0.4)));
    float pulse_front = 0.5 + 0.5 * sin(t * 1.6 - r * 10.0);

    rgb += deep_color.rgb * (0.030 + 0.035 * smoothstep(0.60, 0.04, r));
    rgb += secondary_color.rgb * storm * 0.028;
    rgb += highlight_color.rgb * central * (0.012 + 0.015 * pulse_front) * glow_strength;
    rgb += highlight_color.rgb * pow(clamp(trace_energy * 0.014, 0.0, 1.0), 1.7) * 0.08 * glow_strength;

    COLOR = vec4(clamp(rgb, 0.0, 1.0), 1.0);
}
