class_name MechanicRegistry
extends RefCounted

static func create_mechanic(mechanic_id: String) -> ChallengeMechanic:
	match mechanic_id.to_lower():
		"key":
			return KeyMechanic.new()

		"parking":
			return ParkingMechanic.new()

		"pilot":
			return PilotMechanic.new()

		"parking_v2":
			return ParkingMechanicV2.new()

		"hit_v1":
			return HitMechanic.new()

		"catch_v1":
			return CatchMechanic.new()

		"find_v1":
			return FindMechanic.new()

		"choose_v1":
			return ChooseMechanic.new()
		
		"count_v1":
			return CountMechanic.new()

		_:
			return null