class_name MechanicRegistry
extends RefCounted

## Factoría y Registro de Mecánicas: Aisla la resolución dinámica de tipos de mecánica
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
		_:
			return null
