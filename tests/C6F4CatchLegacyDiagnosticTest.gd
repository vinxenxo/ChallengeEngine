extends SceneTree

const ORACLE = preload("res://core/execution/ChallengeLegacyRuntimeOracle.gd")

func _init() -> void:
    print("")
    print("============================================================")
    print(" C6-F4.4 CATCH LEGACY ORACLE DIAGNOSTIC")
    print("============================================================")
    print("")

    var legacy_config: Dictionary = {
        "challenge_id": "CHALLENGE_006",
        "mechanic": "catch_v1",
        "generation": {
            "seed": 884422,
            "rng_version": "2.0"
        },
        "video": {
            "fps": 60,
            "hook_duration": 2.0,
            "game_duration": 7.0,
            "cta_duration": 2.0
        },
        "difficulty": {
            "catch": {
                "catcher_origin": [540.0, 1700.0],
                "catcher_direction": [0.0, -1.0],
                "catcher_speed_base": 6.0,
                "target_origin": [540.0, 400.0],
                "target_direction": [0.0, 1.0],
                "target_speed_base": 2.5,
                "catch_radius": 45.0
            }
        },
        "content": {
            "hook": "¡Intercepta el objetivo en movimiento!",
            "cta": "¡Desafío superado!"
        }
    }

    print("[TEST] Running exact CHALLENGE_006 legacy oracle path...")
    print("")

    var oracle_result: Dictionary = ORACLE.run(legacy_config)

    print("")
    print("============================================================")
    print(" ORACLE FINAL RESULT")
    print("============================================================")

    print("valid=%s" % str(oracle_result.get("valid", false)))
    print("error_code=%s" % str(oracle_result.get("error_code", "")))
    print("message=%s" % str(oracle_result.get("message", "")))

    if oracle_result.has("result") and oracle_result.result != null:
        var sim_result: SimulationResult = oracle_result.result

        print("winning_frame=%d" % sim_result.winning_frame)
        print("minimum_distance=%s" % str(sim_result.minimum_distance))
        print("score=%s" % str(sim_result.score))
        print("frames=%d" % sim_result.frames.size())
        print(
            "close_calls=%s"
            % str(sim_result.metadata.get("close_calls", "MISSING"))
        )
        print("self_scored=%s" % str(sim_result.is_self_scored))
        print(
            "attempts=%s"
            % str(sim_result.metadata.get("attempts", "MISSING"))
        )
        print(
            "seed_used=%s"
            % str(sim_result.metadata.get("seed_used", "MISSING"))
        )

    print("")
    quit()
