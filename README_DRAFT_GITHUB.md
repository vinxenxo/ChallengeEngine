# 🌟 Deterministic Engine v2.0

A high-performance, stateless deterministic engine built with Godot 4 and GDScript.

## 🧠 Core Principles
- **Absolute Determinism**: No global RNG state. All randomness is derived from `(seed, stream_id, index)` tuples.
- **Domain Isolation**: Structural logic and cosmetic presentation are strictly separated.
- **Immutable Baseline**: Legacy challenges (CHALLENGE_001.json, CHALLENGE_002.json) are preserved as mathematical fixtures.

## 🛠️ Features
- **MechanicRNGContext** and **PresentationRNGContext** for stateless RNG.
- **StructuralRNG** and **CosmeticRNG** for domain-specific randomness.
- **PonyTail Optimization**: Simplicity and efficiency without sacrificing correctness.

## 📦 Installation
1. Clone the repository.
2. Open in Godot 4.
3. Run the project.

## 📚 Documentation
- [Godot 4 Documentation](https://docs.godotengine.org/en/stable/)
- [GDScript Language Guide](https://docs.godotengine.org/en/stable/getting_started/step_by_step/gdscript_basics.html)

## 📦 License
This project is licensed under the MIT License.

## 📩 Contributions
Welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## 📄 Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [releases](https://github.com/yourusername/deterministic-engine/releases) page.

## 📝 Authors
- **Your Name** - *Initial work* - [yourusername](https://github.com/yourusername)

## 📌 Acknowledgments
- This project was inspired by the [PonyTail Principle](https://www.youtube.com/watch?v=Km6b21l8s1w) and the [Godot 4 documentation](https://docs.godotengine.org/en/stable/).