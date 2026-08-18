class_name MechanicRegistry
extends RefCounted

## Factoría y Registro de Mecánicas: Aisla la resolución dinámica de tipos de mecánica
static func create_mechanic(mechanic_id: String) -> ChallengeMechanic:
	match mechanic_id.to_lower():
		"key":
			return KeyMechanic.new()
		"parking":
			return ParkingMechanic.new()
		_:
			return null