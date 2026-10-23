# C11-D V2B — correccion del guard de version del harness

Fecha: 2026-10-23
Estado: CORRECCION_DEL_HARNESS_APLICADA_PENDIENTE_DE_TEST
Alcance: exclusivamente el harness de composicion de fuentes; no autoriza produccion ni render.

## Causa
Engine.get_version_info().string no contiene el sufijo Mono como parte garantizada de su formato. La comprobacion anterior intentaba detectar mono dentro de esa cadena y fallaba aunque se hubiera arrancado el ejecutable Mono.

## Correccion
Se verifica la version mediante los campos major=4, minor=7, patch=1, status=stable y build=official. La presencia de CSharpScript mediante ClassDB.class_exists se utiliza para comprobar la capacidad Mono del runtime.

## Integridad
Runtime SHA256 anterior: 5B8BBDA9A63F758C39EB1D511634DE246C38EDAF1162A8F75BBD38EC2305359B
Runtime SHA256 nuevo: 267BD25FB9545CF5DE838EC29A4AB6F09329A02704FC605CB0FA5B1E23AF9694
Runner SHA256 conservado: 5C69F08194213B7BCF48FE7F52BD17E8EC29A2D6E275C4C73787E7FA20B174FF
Contrato SHA256 conservado: D3265F1BA91DC664E85BBB0DC87EA6B145F0FED34FFA4552412C8FA70C19B2AB
Manifiesto congelado C11-C SHA256: E405D08E4D166B1AD95953558F4A088E73EEA9527E6E89244BEB4096EAC4B953

## Bloqueos conservados
renderer=OFF
media_created=false
production_calls=0
runtime_implementation_authorized_for_production=false
render_test_authorized=false
C11-C permanece inmutable.
El resultado de composicion sigue pendiente hasta ejecutar y superar las pruebas.